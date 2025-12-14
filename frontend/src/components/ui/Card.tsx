import { ReactNode } from 'react'

interface CardProps {
  children: ReactNode
  className?: string
  onClick?: () => void
  hoverable?: boolean
}

export default function Card({ children, className = '', onClick, hoverable = false }: CardProps) {
  const hoverStyles = hoverable 
    ? 'cursor-pointer hover:shadow-lg hover:-translate-y-1 hover:border-primary/30 dark:hover:border-primary/30 active:scale-[0.98] transition-all duration-200' 
    : ''
  
  return (
    <div 
      className={`glass-card p-4 ${hoverStyles} ${className}`}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={onClick ? (e) => e.key === 'Enter' && onClick() : undefined}
    >
      {children}
    </div>
  )
}
