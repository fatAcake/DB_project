import { useAuthStore } from '@/store/useAuthStore'
import NavLink from '../navigation/NavLink'
import { 
  Home, 
  ShoppingBag, 
  MessageSquare, 
  User, 
  Settings,
  Package,
  BarChart3
} from 'lucide-react'

const Sidebar = () => {
  const { isAuthenticated, user } = useAuthStore()

  const mainNavItems = [
    { to: '/', label: 'Главная', icon: Home },
    { to: '/catalog', label: 'Каталог', icon: ShoppingBag },
    { to: '/feedback', label: 'Обратная связь', icon: MessageSquare },
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
      ? [{ to: '/admin', label: 'Админ панель', icon: BarChart3 }]
      : []

  return (
    <aside className="hidden lg:block w-64 bg-gray-50 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700">
      <nav className="p-4 space-y-6">
        {/* Main Navigation */}
        <div>
          <h2 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3 px-4">
            Навигация
          </h2>
          <ul className="space-y-1">
            {mainNavItems.map((item) => {
              const Icon = item.icon
              return (
                <li key={item.to}>
                  <NavLink
                    to={item.to}
                    variant="sidebar"
                    className="flex items-center space-x-3"
                  >
                    <Icon size={20} />
                    <span>{item.label}</span>
                  </NavLink>
                </li>
              )
            })}
          </ul>
        </div>

        {/* User Navigation */}
        {isAuthenticated && userNavItems.length > 0 && (
          <div>
            <h2 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3 px-4">
              Личный кабинет
            </h2>
            <ul className="space-y-1">
              {userNavItems.map((item) => {
                const Icon = item.icon
                return (
                  <li key={item.to}>
                    <NavLink
                      to={item.to}
                      variant="sidebar"
                      className="flex items-center space-x-3"
                    >
                      <Icon size={20} />
                      <span>{item.label}</span>
                    </NavLink>
                  </li>
                )
              })}
            </ul>
          </div>
        )}

        {/* Admin Navigation */}
        {adminNavItems.length > 0 && (
          <div>
            <h2 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3 px-4">
              Администрирование
            </h2>
            <ul className="space-y-1">
              {adminNavItems.map((item) => {
                const Icon = item.icon
                return (
                  <li key={item.to}>
                    <NavLink
                      to={item.to}
                      variant="sidebar"
                      className="flex items-center space-x-3"
                    >
                      <Icon size={20} />
                      <span>{item.label}</span>
                    </NavLink>
                  </li>
                )
              })}
            </ul>
          </div>
        )}

        {/* Auth links for non-authenticated users */}
        {!isAuthenticated && (
          <div>
            <h2 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3 px-4">
              Вход
            </h2>
            <ul className="space-y-1">
              <li>
                <NavLink
                  to="/login"
                  variant="sidebar"
                  className="flex items-center space-x-3"
                >
                  <User size={20} />
                  <span>Войти</span>
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/register"
                  variant="sidebar"
                  className="flex items-center space-x-3"
                >
                  <User size={20} />
                  <span>Регистрация</span>
                </NavLink>
              </li>
            </ul>
          </div>
        )}
      </nav>
    </aside>
  )
}

export default Sidebar
