from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from typing import Optional

from ..models import MessageFile
from .file_crud import get_file_metadata_by_id

logger = logging.getLogger(__name__)

async def link_file_to_message_async(
    db: AsyncSession, 
    message_id: int, 
    file_id: str
) -> Optional[MessageFile]:
    """
    Link a file to a message asynchronously
    
    Args:
        db: Async database session
        message_id: Message ID to link the file to
        file_id: File ID to link
        
    Returns:
        MessageFile object or None if file not found
    """
    try:
        # Check if file exists
        file_metadata = await db.run_sync(lambda sess: get_file_metadata_by_id(sess, file_id))
        if not file_metadata:
            logger.warning(f"File {file_id} not found when trying to link to message {message_id}")
            return None
            
        # Create MessageFile object
        message_file = MessageFile(
            message_id=message_id,
            file_id=file_id
        )
        
        db.add(message_file)
        await db.commit()
        await db.refresh(message_file)
        
        return message_file
    except Exception as e:
        await db.rollback()
        logger.error(f"Error linking file {file_id} to message {message_id}: {e}")
        raise

def link_file_to_message(
    db: Session, 
    message_id: int, 
    file_id: str
) -> Optional[MessageFile]:
    """
    Link a file to a message synchronously
    
    Args:
        db: Database session
        message_id: Message ID to link the file to
        file_id: File ID to link
        
    Returns:
        MessageFile object or None if file not found
    """
    try:
        # Check if file exists
        file_metadata = get_file_metadata_by_id(db, file_id)
        if not file_metadata:
            logger.warning(f"File {file_id} not found when trying to link to message {message_id}")
            return None
            
        # Create MessageFile object
        message_file = MessageFile(
            message_id=message_id,
            file_id=file_id
        )
        
        db.add(message_file)
        db.commit()
        db.refresh(message_file)
        
        return message_file
    except Exception as e:
        db.rollback()
        logger.error(f"Error linking file {file_id} to message {message_id}: {e}")
        raise 