import type { ReactNode } from 'react';
import { cn } from '../../utils/cn';

interface CardProps {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
  hover?: boolean;
}

export function Card({ children, className, onClick, hover }: CardProps) {
  return (
    <div
      onClick={onClick}
      className={cn(
        'bg-surface-card border border-surface-border rounded-xl p-5',
        hover && 'hover:border-brand-500/40 hover:bg-surface-hover cursor-pointer transition-all',
        className
      )}
    >
      {children}
    </div>
  );
}
