from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import crud, models, schemas, services
from ..database import get_db
from ..config import get_settings # For upload limits if needed here

# Note: We are nesting message routes under chat routes conceptually,
# but defining them in a separate router for modularity.
# The chat_id will be passed as a path parameter.
router = APIRouter(
    tags=["Messages"],
    responses={404: {"description": "Not found"}},
)

@router.post("/chats/{chat_id}/messages/", response_model=schemas.Message, status_code=status.HTTP_201_CREATED)
async def create_new_message_for_chat(
    chat_id: int, 
    message_text: str = Form(...),
    files: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    """Creates a new message (with optional files) within a specific chat session."""
    db_chat = crud.get_chat(db, chat_id=chat_id)
    if db_chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")

    processed_files_metadata = []
    if files:
        if len(files) > get_settings().max_files_per_prompt: # Max 5 files
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Too many files. Maximum {get_settings().max_files_per_prompt} files allowed per prompt."
            )
        for upload_file in files:
            # Size check removed from here. 
            # services.prepare_file_metadata_for_db will handle all size checks, 
            # including those for Gemini Files API vs inline.
            
            file_meta = await services.prepare_file_metadata_for_db(upload_file, db)
            processed_files_metadata.append(file_meta)

    # 1. Save the user's message and its associated files
    user_message_schema = schemas.MessageCreate(role="user", content=message_text)
    user_db_message = crud.create_chat_message_with_files(
        db=db, 
        message_data=user_message_schema, 
        chat_id=chat_id, 
        file_metadatas=processed_files_metadata
    )

    # 2. Retrieve chat history EXCLUDING the just-added user message for the AI context
    # The AI will see the current user message via user_message_content and current_message_files args
    chat_history_for_ai = crud.get_messages_for_chat(db=db, chat_id=chat_id, limit=50, exclude_message_id=user_db_message.id)
    
    # The user_db_message.files should be populated by create_chat_message_with_files
    # If not, we might need to re-fetch user_db_message or ensure the relationship is loaded.
    
    # Convert models.FileMetadata to schemas.FileMetadataInfo for the service call
    current_msg_files_for_service: List[schemas.FileMetadataInfo] = []
    if user_db_message.files:
        for file_metadata in user_db_message.files:
            current_msg_files_for_service.append(schemas.FileMetadataInfo.from_orm(file_metadata))

    # 3. Generate AI response
    # Pass the user_db_message.files (converted to schema) as current_message_files
    ai_response_content = services.generate_ai_response(
        chat_history=chat_history_for_ai, 
        user_message_content=user_db_message.content, # Use content from saved user message
        current_message_files=current_msg_files_for_service, 
        db=db
    )

    # 4. Create and save the AI's message
    ai_message_schema = schemas.MessageCreate(role="model", content=ai_response_content)
    # AI messages typically don't have uploaded files from the user perspective
    ai_db_message = crud.create_chat_message_with_files(db=db, message_data=ai_message_schema, chat_id=chat_id, file_metadatas=[])

    # 5. Return the AI's message (which will include its .files list, empty in this case)
    return ai_db_message

# Remove or update the old /messages-with-file/ endpoint as it's now merged with /messages/
# For example, deprecate it or make it an alias if needed for backward compatibility temporarily.
# For this task, I will assume it's removed or commented out.

# @router.post("/chats/{chat_id}/messages-with-file/", response_model=schemas.Message, status_code=status.HTTP_201_CREATED)
# async def create_new_message_with_file(
#     chat_id: int, 
#     message: str = Form(...),
#     files: Optional[List[UploadFile]] = File(None),
#     db: Session = Depends(get_db)
# ):
#     """Creates a new message with an optional file attachment within a specific chat session."""
#     # Check if chat exists first
#     db_chat = crud.get_chat(db, chat_id=chat_id)
#     if db_chat is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")

#     # Process multiple files if provided (limit to 5 per prompt)
#     file_paths: List[str] = []
#     if files:
#         for upload_file in files[:5]:
#             path = await services.save_uploaded_file(upload_file)
#             file_paths.append(path)

#     # 1. Save the user's message (attach first file path for backward compatibility)
#     first_file = file_paths[0] if file_paths else None
#     user_message_schema = schemas.MessageCreate(role="user", content=message, file_path=first_file)
#     user_db_message = crud.create_chat_message(db=db, message=user_message_schema, chat_id=chat_id)

#     # 2. Save additional file attachments as separate messages
#     for extra_path in file_paths[1:]:
#         extra_message_schema = schemas.MessageCreate(role="user", content="", file_path=extra_path)
#         crud.create_chat_message(db=db, message=extra_message_schema, chat_id=chat_id)

#     # 3. Retrieve chat history (including the new user message)
#     chat_history = crud.get_messages_for_chat(db=db, chat_id=chat_id, limit=50)

#     # 4. Generate AI response with files if provided
#     ai_response_content = services.generate_ai_response(
#         chat_history=chat_history, 
#         user_message_content=message,
#         file_paths=file_paths,
#         db=db
#     )

#     # 5. Create and save the AI's message
#     ai_message_schema = schemas.MessageCreate(role="model", content=ai_response_content)
#     ai_db_message = crud.create_chat_message(db=db, message=ai_message_schema, chat_id=chat_id)

#     # 6. Return the AI's message
#     return ai_db_message

@router.get("/chats/{chat_id}/messages/", response_model=List[schemas.Message])
def read_messages_for_chat(chat_id: int, skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    """Retrieves all messages for a specific chat session."""
    db_chat = crud.get_chat(db, chat_id=chat_id)
    if db_chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    messages = crud.get_messages_for_chat(db, chat_id=chat_id, skip=skip, limit=limit)
    return messages