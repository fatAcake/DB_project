import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Admin,
  Resource,
  ListGuesser,
  EditGuesser,
  ShowGuesser,
  Layout,
  defaultTheme,
} from 'react-admin'
import { useAuthStore } from '@/store/useAuthStore'
import { dataProvider } from '@/admin/dataProvider'
import People from '@mui/icons-material/People'
import Security from '@mui/icons-material/Security'

const AdminLayout = (props: React.ComponentProps<typeof Layout>) => (
  <Layout {...props} />
)

/**
 * Админ-панель на react-admin.
 * Доступна только пользователям с role.name === 'admin'.
 */
const AdminPage = () => {
  const navigate = useNavigate()
  const { user, isAuthenticated } = useAuthStore()

  const isAdmin = isAuthenticated && user?.role === 'admin'

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login', { replace: true })
      return
    }
    if (!isAdmin) {
      navigate('/', { replace: true })
    }
  }, [isAuthenticated, isAdmin, navigate])

  if (!isAuthenticated || !isAdmin) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <p className="text-gray-600">Проверка доступа...</p>
      </div>
    )
  }

  return (
    <Admin
      basename="/admin"
      dataProvider={dataProvider}
      layout={AdminLayout}
      theme={{
        ...defaultTheme,
        palette: {
          mode: 'light',
          primary: { main: '#1a1a2e' },
          secondary: { main: '#0f3460' },
        },
      }}
      title="Админ-панель"
    >
      <Resource
        name="users"
        list={ListGuesser}
        edit={EditGuesser}
        show={ShowGuesser}
        options={{ label: 'Пользователи' }}
        icon={People}
      />
      <Resource
        name="roles"
        list={ListGuesser}
        edit={EditGuesser}
        show={ShowGuesser}
        options={{ label: 'Роли' }}
        icon={Security}
      />
    </Admin>
  )
}

export default AdminPage
