import { useState } from 'react'
import { Menu, X } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import NavLink from './NavLink'
import { useAuthStore } from '@/store/useAuthStore'

const MobileMenu = () => {
  const [isOpen, setIsOpen] = useState(false)
  const { isAuthenticated } = useAuthStore()

  const navItems = [
    { to: '/', label: 'Главная' },
    { to: '/catalog', label: 'Каталог' },
  ]

  return (
    <div className="md:hidden">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="p-2 rounded-md text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
        aria-label="Toggle menu"
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, x: -100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-800 shadow-lg"
          >
            <div className="flex flex-col h-full pt-16">
              <nav className="flex-1 px-4 space-y-2">
                {navItems.map((item) => (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    variant="sidebar"
                    onClick={() => setIsOpen(false)}
                  >
                    {item.label}
                  </NavLink>
                ))}
              </nav>
              <div className="p-4 border-t border-gray-200 dark:border-gray-700">
                {isAuthenticated ? (
                  <NavLink
                    to="/profile"
                    variant="sidebar"
                    onClick={() => setIsOpen(false)}
                  >
                    Профиль
                  </NavLink>
                ) : (
                  <div className="space-y-2">
                    <NavLink
                      to="/login"
                      variant="sidebar"
                      onClick={() => setIsOpen(false)}
                    >
                      Войти
                    </NavLink>
                    <NavLink
                      to="/register"
                      variant="sidebar"
                      onClick={() => setIsOpen(false)}
                    >
                      Регистрация
                    </NavLink>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40"
          onClick={() => setIsOpen(false)}
        />
      )}
    </div>
  )
}

export default MobileMenu
