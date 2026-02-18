import { Link, useLocation } from 'react-router-dom'
import { ReactNode, forwardRef, CSSProperties } from 'react'
import { cn } from '@/utils/cn'

interface NavLinkProps {
  to: string
  children: ReactNode
  className?: string
  variant?: 'header' | 'sidebar' | 'sidebarDark' | 'minimal'
  onClick?: () => void
  style?: CSSProperties
}

const NavLink = forwardRef<HTMLAnchorElement, NavLinkProps>(
  ({ to, children, className, variant = 'header', onClick, style }, ref) => {
    const location = useLocation()
    const isActive = location.pathname === to

    const baseStyles = 'transition-all duration-200 uppercase tracking-wide'
    
    const variants = {
      header: cn(
        'px-4 py-2 rounded-md font-medium',
        isActive
          ? 'bg-blue-600 text-white'
          : 'text-gray-700 hover:bg-blue-100 hover:text-blue-700 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white'
      ),
      sidebar: cn(
        'block px-4 py-3 rounded-lg font-medium',
        isActive
          ? 'bg-blue-600 text-white'
          : 'text-gray-700 hover:bg-blue-50 hover:text-blue-700 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white'
      ),
      sidebarDark: cn(
        'block px-4 py-3 rounded-2xl font-medium font-unbounded text-sm',
        isActive
          ? 'bg-white text-black'
          : 'text-white hover:bg-white hover:text-black'
      ),
      minimal: cn(
        'px-4 py-2 font-semibold text-sm whitespace-nowrap bg-transparent border border-transparent hover:bg-white hover:text-black rounded-xl transition-all'
      ),
    }

    return (
      <Link
        ref={ref}
        to={to}
        className={cn(baseStyles, variants[variant], className)}
        onClick={onClick}
        style={style}
      >
        {children}
      </Link>
    )
  }
)

NavLink.displayName = 'NavLink'

export default NavLink
