import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { ShoppingCart, User, Search, Menu, X, LogOut, Settings, Package } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import NavLink from '../navigation/NavLink'
import NavGroup from '../navigation/NavGroup'
import { useAuthStore } from '@/store/useAuthStore'

const Header = () => {
  const { isAuthenticated, user, logout } = useAuthStore()
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false)
  const [isSearchOpen, setIsSearchOpen] = useState(false)
  const navigate = useNavigate()

  const navItems = [
    { to: '/', label: 'Главная' },
    { to: '/catalog', label: 'Каталог' },
    { to: '/workshop', label: 'Мастерская' },
    { to: '/about', label: 'О компании' },
    { to: '/contact', label: 'Контакты' },
  ]

  const handleLogout = () => {
    logout()
    setIsUserMenuOpen(false)
    navigate('/')
  }

  return (
    <header className="bg-black text-white sticky top-0 z-50">
      <div className="container mx-auto px-4 lg:px-8">
        <nav className="flex items-center justify-between h-20">
          {/* Logo - Left */}
          <Link
            to="/"
            className="flex-shrink-0 flex items-center h-14"
          >
            <motion.img
              src="/logo.svg"
              alt="Logo"
              className="h-full w-auto max-w-[180px] object-contain brightness-0 invert cursor-pointer"
              whileHover={{ 
                scale: 1.1,
                rotate: [0, -5, 5, -5, 0],
                transition: { duration: 0.5 }
              }}
              whileTap={{ scale: 0.95 }}
              onError={(e) => {
                // Fallback если логотип не найден - показываем текст
                const target = e.target as HTMLImageElement
                target.style.display = 'none'
                const fallback = target.nextElementSibling as HTMLElement
                if (fallback) {
                  fallback.style.display = 'block'
                }
              }}
            />
            <span className="text-white font-unbounded text-xl font-bold hidden">
              Shop
            </span>
          </Link>

          {/* Desktop Navigation - Right with grouped buttons */}
          <div className="hidden lg:flex items-center">
            <NavGroup items={navItems.slice(1)} />
          </div>

          {/* Right side actions - Utility buttons */}
          <div className="flex items-center space-x-3">
            {/* Search */}
            <div className="relative">
              <button
                onClick={() => setIsSearchOpen(!isSearchOpen)}
                className="p-2 text-white hover:bg-white hover:text-black transition-colors border border-white rounded-2xl"
                aria-label="Search"
              >
                <Search size={18} />
              </button>
              
              <AnimatePresence>
                {isSearchOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="absolute right-0 top-full mt-2 w-80 bg-white rounded-2xl border border-black p-4"
                  >
                    <input
                      type="text"
                      placeholder="Поиск товаров..."
                      className="w-full px-4 py-2 border border-black focus:outline-none focus:ring-2 focus:ring-black bg-white text-black rounded-xl"
                      autoFocus
                    />
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Cart */}
            <Link
              to="/cart"
              className="relative p-2 text-white hover:bg-white hover:text-black transition-colors border border-white rounded-2xl"
              aria-label="Shopping cart"
            >
              <ShoppingCart size={18} />
              <span className="absolute -top-1 -right-1 bg-white text-black text-xs w-5 h-5 flex items-center justify-center border border-black font-bold rounded-full">
                0
              </span>
            </Link>

            {/* Auth button - Login */}
            {!isAuthenticated && (
              <NavLink to="/login" variant="minimal" className="font-unbounded rounded-2xl border border-white">
                ВОЙТИ
              </NavLink>
            )}

            {/* User menu */}
            {isAuthenticated && (
              <div className="relative">
                <button
                  onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                  className="p-2 text-white hover:bg-white hover:text-black transition-colors border border-white rounded-2xl uppercase text-sm font-semibold"
                  aria-label="User menu"
                >
                  <User size={18} />
                </button>

                <AnimatePresence>
                  {isUserMenuOpen && (
                    <>
                      <div
                        className="fixed inset-0 z-40"
                        onClick={() => setIsUserMenuOpen(false)}
                      />
                      <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="absolute right-0 top-full mt-2 w-56 bg-white border border-black py-2 z-50 rounded-2xl"
                      >
                        <Link
                          to="/profile"
                          onClick={() => setIsUserMenuOpen(false)}
                          className="flex items-center space-x-3 px-4 py-2 hover:bg-black hover:text-white transition-colors uppercase text-sm font-semibold"
                        >
                          <User size={18} />
                          <span>PROFILE</span>
                        </Link>
                        <Link
                          to="/profile/orders"
                          onClick={() => setIsUserMenuOpen(false)}
                          className="flex items-center space-x-3 px-4 py-2 hover:bg-black hover:text-white transition-colors uppercase text-sm font-semibold"
                        >
                          <Package size={18} />
                          <span>ORDERS</span>
                        </Link>
                        {user?.role === 'admin' && (
                          <Link
                            to="/admin"
                            onClick={() => setIsUserMenuOpen(false)}
                            className="flex items-center space-x-3 px-4 py-2 hover:bg-black hover:text-white transition-colors uppercase text-sm font-semibold"
                          >
                            <Settings size={18} />
                            <span>ADMIN</span>
                          </Link>
                        )}
                        <div className="border-t border-black my-2" />
                        <button
                          onClick={handleLogout}
                          className="w-full flex items-center space-x-3 px-4 py-2 hover:bg-black hover:text-white transition-colors text-red-600 uppercase text-sm font-semibold"
                        >
                          <LogOut size={18} />
                          <span>LOGOUT</span>
                        </button>
                      </motion.div>
                    </>
                  )}
                </AnimatePresence>
              </div>
            )}

            {/* Mobile menu button */}
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="lg:hidden p-2 text-white hover:bg-white hover:text-black transition-colors border border-white rounded-2xl"
              aria-label="Toggle menu"
            >
              {isMobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>
        </nav>

        {/* Mobile Navigation Menu */}
        <AnimatePresence>
          {isMobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="lg:hidden border-t border-white py-4"
            >
              <div className="flex flex-col space-y-2">
                {navItems.map((item) => (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    variant="minimal"
                    onClick={() => setIsMobileMenuOpen(false)}
                    className="w-full text-left font-unbounded"
                  >
                    {item.label.toUpperCase()}
                  </NavLink>
                ))}
                {!isAuthenticated && (
                  <>
                    <div className="border-t border-white my-2" />
                    <NavLink
                      to="/login"
                      variant="minimal"
                      onClick={() => setIsMobileMenuOpen(false)}
                      className="w-full text-left font-unbounded"
                    >
                      ВОЙТИ
                    </NavLink>
                  </>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </header>
  )
}

export default Header
