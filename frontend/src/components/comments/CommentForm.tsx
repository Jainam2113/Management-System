import { useState, FormEvent } from 'react'
import { Button, Input } from '../ui'

interface CommentFormProps {
  onSubmit: (content: string, authorEmail: string) => void
  isLoading?: boolean
}

export default function CommentForm({ onSubmit, isLoading }: CommentFormProps) {
  const [content, setContent] = useState('')
  const [authorEmail, setAuthorEmail] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})

  const validate = () => {
    const newErrors: Record<string, string> = {}
    if (!content.trim()) {
      newErrors.content = 'Comment is required'
    }
    if (!authorEmail.trim()) {
      newErrors.authorEmail = 'Email is required'
    } else if (!authorEmail.includes('@')) {
      newErrors.authorEmail = 'Invalid email format'
    }
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (!validate()) return
    
    onSubmit(content, authorEmail)
    setContent('')
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <Input
        placeholder="Your email"
        type="email"
        value={authorEmail}
        onChange={(e) => setAuthorEmail(e.target.value)}
        error={errors.authorEmail}
      />
      <div>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className={`input min-h-[60px] resize-none ${errors.content ? 'border-red-500' : ''}`}
          placeholder="Add a comment..."
        />
        {errors.content && (
          <p className="mt-1 text-xs text-red-500">{errors.content}</p>
        )}
      </div>
      <div className="flex justify-end">
        <Button type="submit" size="sm" isLoading={isLoading}>
          Add Comment
        </Button>
      </div>
    </form>
  )
}
