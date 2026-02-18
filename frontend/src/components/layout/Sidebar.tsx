import { Link, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useAuthStore } from '@/store/useAuthStore'
import { useLogAction } from '@/hooks/useLogAction'
import NavLink from '../navigation/NavLink'
import type { LucideIcon } from 'lucide-react'
import {
  Home,
  ShoppingBag,
  User,
  Settings,
  Package,
  BarChart3,
  Hammer,
  Info,
  Mail,
  ChevronLeft,
  PanelLeftClose,
  PanelLeft,
  LogIn,
  UserPlus,
  LogOut,
} from 'lucide-react'

const SIDEBAR_WIDTH = 280
const SIDEBAR_COLLAPSED_WIDTH = 72

const Sidebar = () => {
  const { isAuthenticated, user, logout } = useAuthStore()
  const { logAction } = useLogAction()
  const navigate = useNavigate()
  const [collapsed, setCollapsed] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)
  const [isDesktop, setIsDesktop] = useState(false)

  useEffect(() => {
    const mq = window.matchMedia('(min-width: 1024px)')
    setIsDesktop(mq.matches)
    const handler = () => setIsDesktop(mq.matches)
    mq.addEventListener('change', handler)
    return () => mq.removeEventListener('change', handler)
  }, [])

  const mainNavItems = [
    { to: '/', label: 'Главная', icon: Home },
    { to: '/catalog', label: 'Каталог', icon: ShoppingBag },
    { to: '/workshop', label: 'Мастерская', icon: Hammer },
    { to: '/about', label: 'О компании', icon: Info },
    { to: '/contact', label: 'Контакты', icon: Mail },
  ]

  const userNavItems = isAuthenticated
    ? [
        { to: '/profile', label: 'Профиль', icon: User },
        { to: '/profile/orders', label: 'Мои заказы', icon: Package },
        { to: '/profile/settings', label: 'Настройки', icon: Settings },
      ]
    : []

  const adminNavItems =
    user?.role === 'admin'
      ? [{ to: '/admin', label: 'Админ', icon: BarChart3 }]
      : []

  const NavBlock = ({
    title,
    items,
  }: {
    title: string
    items: { to: string; label: string; icon: LucideIcon }[]
  }) => (
    <div className="space-y-2">
      <h2 className="text-[10px] font-unbounded font-semibold text-white/60 uppercase tracking-widest px-3 mb-2">
        {title}
      </h2>
      <ul className="space-y-1">
        {items.map((item) => {
          const Icon = item.icon
          return (
            <li key={item.to}>
              <NavLink
                to={item.to}
                variant="sidebarDark"
                className="flex items-center gap-3 w-full"
              >
                <span className="flex-shrink-0">
                  <Icon size={20} />
                </span>
                <span className="truncate">{item.label}</span>
              </NavLink>
            </li>
          )
        })}
      </ul>
    </div>
  )

  const sidebarContent = (
    <nav className="flex flex-col h-full py-6 px-3">
      <div className="flex-1 space-y-8 overflow-y-auto">
        <NavBlock title="Навигация" items={mainNavItems} />
        {isAuthenticated && (
          <>
            <div className="space-y-2">
              <h2 className="text-[10px] font-unbounded font-semibold text-white/60 uppercase tracking-widest px-3 mb-2">
                Профиль
              </h2>
              <div className="flex items-center gap-3 px-3 py-2 rounded-2xl bg-white/10">
                <span className="flex-shrink-0 w-9 h-9 rounded-xl bg-white text-black flex items-center justify-center font-unbounded font-bold text-sm">
                  {user?.name?.charAt(0)?.toUpperCase() ?? '?'}
                </span>
                <span className="truncate text-sm font-medium text-white">
                  {user?.name}
                </span>
              </div>
              <button
                type="button"
                onClick={() => { logAction('auth', 'logout', '200'); logout(); navigate('/'); }}
                className="flex items-center gap-3 w-full px-3 py-2 rounded-2xl text-white/90 hover:bg-white/10 hover:text-white transition-colors"
              >
                <LogOut size={20} />
                <span>Выйти</span>
              </button>
            </div>
            {userNavItems.length > 0 && (
              <NavBlock title="Личный кабинет" items={userNavItems} />
            )}
          </>
        )}
        {isAuthenticated && adminNavItems.length > 0 && (
          <NavBlock title="Админ" items={adminNavItems} />
        )}
        {!isAuthenticated && (
          <div className="space-y-2">
            <h2 className="text-[10px] font-unbounded font-semibold text-white/60 uppercase tracking-widest px-3 mb-2">
              Вход
            </h2>
            <ul className="space-y-1">
              <li>
                <NavLink
                  to="/login"
                  variant="sidebarDark"
                  className="flex items-center gap-3"
                >
                  <LogIn size={20} />
                  <span>Войти</span>
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/register"
                  variant="sidebarDark"
                  className="flex items-center gap-3"
                >
                  <UserPlus size={20} />
                  <span>Регистрация</span>
                </NavLink>
              </li>
            </ul>
          </div>
        )}
      </div>
      <div className="pt-4 mt-4 border-t border-white/20">
        <Link
          to="/"
          className="flex items-center gap-3 px-3 py-2 rounded-2xl text-white/80 hover:bg-white/10 hover:text-white transition-colors"
        >
          <span className="text-lg font-unbounded font-bold">Shop</span>
        </Link>
      </div>
    </nav>
  )

  return (
    <>
      {/* Кнопка открытия сайдбара на мобильных — показываем только на lg-, т.к. сайдбар скрыт */}
      <button
        onClick={() => setMobileOpen(true)}
        className="fixed left-4 bottom-6 z-40 lg:hidden w-12 h-12 rounded-2xl bg-black border-2 border-white text-white flex items-center justify-center shadow-lg"
        aria-label="Открыть меню"
      >
        <PanelLeft size={22} />
      </button>

      {/* Оверлей для мобильного меню */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 z-40 lg:hidden"
            onClick={() => setMobileOpen(false)}
          />
        )}
      </AnimatePresence>

      {/* Боковая панель: десктоп — слева, мобильный — выезжающая */}
      <motion.aside
        initial={false}
        animate={{
          width: collapsed ? SIDEBAR_COLLAPSED_WIDTH : SIDEBAR_WIDTH,
          x: isDesktop ? 0 : mobileOpen ? 0 : -SIDEBAR_WIDTH - 20,
        }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        className="fixed left-0 top-20 bottom-0 z-50 bg-black border-r border-white/20 flex flex-col shadow-xl flex"
      >
        {/* Десктоп: кнопка свернуть — в развёрнутом виде справа сверху */}
        {!collapsed && (
          <div className="hidden lg:flex absolute top-2 right-2">
            <button
              onClick={() => setCollapsed(true)}
              className="p-2 rounded-2xl text-white/70 hover:bg-white/10 hover:text-white transition-colors"
              aria-label="Свернуть меню"
            >
              <PanelLeftClose size={20} />
            </button>
          </div>
        )}

        {/* Мобильный: кнопка закрыть */}
        <div className="flex lg:hidden absolute top-3 right-3">
          <button
            onClick={() => setMobileOpen(false)}
            className="p-2 rounded-2xl text-white hover:bg-white/10 transition-colors"
            aria-label="Закрыть меню"
          >
            <ChevronLeft size={24} />
          </button>
        </div>

        {collapsed ? (
          <nav className="flex flex-col items-center pt-4 pb-6 px-2 space-y-2">
            <button
              onClick={() => setCollapsed(false)}
              className="p-3 rounded-2xl text-white/70 hover:bg-white/10 hover:text-white transition-colors"
              aria-label="Развернуть меню"
            >
              <PanelLeft size={22} />
            </button>
            {mainNavItems.slice(0, 6).map((item) => {
              const Icon = item.icon
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  variant="sidebarDark"
                  className="p-3 rounded-2xl"
                >
                  <Icon size={22} />
                </NavLink>
              )
            })}
          </nav>
        ) : (
          sidebarContent
        )}
      </motion.aside>

      {/* Спейсер: отступ слева под сайдбар на десктопе */}
      <div
        className="hidden lg:block flex-shrink-0 transition-[width] duration-300 ease-out"
        style={{ width: collapsed ? SIDEBAR_COLLAPSED_WIDTH : SIDEBAR_WIDTH }}
      />
    </>
  )
}

export default Sidebar
