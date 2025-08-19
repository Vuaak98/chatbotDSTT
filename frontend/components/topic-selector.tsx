"use client"


import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { ChevronDown, BookOpen, Calculator } from "lucide-react"

interface TopicSelectorProps {
  onTopicSelect: (topic: string) => void
}

const EXAM_TYPES = [
  { id: "bangA", name: "Đề Thi Bảng A", description: "Trường top - Khó" },
  { id: "bangB", name: "Đề Thi Bảng B", description: "Cơ bản - Vừa" },
]

const PROBLEM_TYPES = [
  { id: "mt", name: "Ma Trận", description: "Phép toán ma trận, nghịch đảo" },
  { id: "hpt", name: "Hệ Phương Trình", description: "Giải hệ PT tuyến tính" },
  { id: "dt", name: "Định Thức", description: "Tính định thức ma trận" },
  { id: "tohop", name: "Tổ Hợp", description: "Tổ hợp và xác suất" },
  { id: "kgvt", name: "Không Gian Vector", description: "Vector và không gian" },
  { id: "gtr", name: "Giá Trị Riêng", description: "Eigenvalue và eigenvector" },
  { id: "dathuc", name: "Đa Thức", description: "Đa thức đặc trưng" },
]

export default function TopicSelector({ onTopicSelect }: TopicSelectorProps) {

  const handleExamClick = (topicId: string, topicName: string) => {
    // Remove "Đề Thi" prefix from name to avoid duplication
    const cleanName = topicName.replace(/^Đề Thi\s+/i, '').toLowerCase()
    onTopicSelect(`Cho tôi đề thi ${cleanName} năm 2024`)
  }

  const handleProblemClick = (topicId: string, topicName: string) => {
    onTopicSelect(`Cho tôi dạng bài về ${topicName.toLowerCase()}`)
  }

  return (
    <div className="flex gap-2">
      {/* Exam Type Dropdown */}
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="outline" size="sm" className="gap-2">
            <BookOpen className="h-4 w-4" />
            Đề Thi
            <ChevronDown className="h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="start" side="top" className="w-56">
          <DropdownMenuLabel>Chọn loại đề thi</DropdownMenuLabel>
          <DropdownMenuSeparator />
          {EXAM_TYPES.map((exam) => (
            <DropdownMenuItem
              key={exam.id}
              onClick={() => handleExamClick(exam.id, exam.name)}
              className="flex flex-col items-start gap-1 p-2"
            >
              <div className="font-medium text-sm">{exam.name}</div>
              <div className="text-xs text-muted-foreground">{exam.description}</div>
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>

      {/* Problem Type Dropdown */}
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="outline" size="sm" className="gap-2">
            <Calculator className="h-4 w-4" />
            Dạng Bài
            <ChevronDown className="h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="start" side="top" className="w-80 max-h-96 overflow-y-auto">
          <DropdownMenuLabel>Chọn dạng bài tập</DropdownMenuLabel>
          <DropdownMenuSeparator />
          <div className="grid grid-cols-2 gap-1 p-1">
            {PROBLEM_TYPES.map((problem) => (
              <DropdownMenuItem
                key={problem.id}
                onClick={() => handleProblemClick(problem.id, problem.name)}
                className="flex flex-col items-start gap-1 p-2 h-auto"
              >
                <div className="font-medium text-sm">{problem.name}</div>
                <div className="text-xs text-muted-foreground line-clamp-2">{problem.description}</div>
              </DropdownMenuItem>
            ))}
          </div>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}