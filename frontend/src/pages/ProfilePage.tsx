import { Link, useNavigate } from 'react-router-dom'
import { useMe, logout } from '@/api/auth'
import LoadingSpinner from '@/components/common/LoadingSpinner'
import ErrorMessage from '@/components/common/ErrorMessage'
import { LogOut, Mail, User } from 'lucide-react'

const ProfilePage = () => {
  const navigate = useNavigate()
  const { data: user, isLoading, isError, error } = useMe()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  if (isLoading) {
    return (
      <div className="max-w-xl mx-auto py-12 flex justify-center">
        <LoadingSpinner />
      </div>
    )
  }

  if (isError || !user) {
    return (
      <div className="max-w-xl mx-auto py-12">
        <ErrorMessage message={(error as Error)?.message || 'Не удалось загрузить профиль'} />
        <p className="text-black/70 mt-4">
          <Link to="/login" className="font-unbounded font-semibold text-black underline">
            Войти
          </Link>
        </p>
      </div>
    )
  }

  return (
    <div className="max-w-xl mx-auto py-8">
      <h1 className="text-3xl font-bold font-unbounded text-black mb-8">
        Профиль
      </h1>
      <div className="rounded-2xl border-2 border-black/10 bg-white/80 p-6 space-y-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-black text-white flex items-center justify-center">
            <User size={24} />
          </div>
          <div>
            <p className="font-unbounded font-semibold text-black text-lg">{user.name}</p>
            {user.email && (
              <p className="flex items-center gap-2 text-black/70 text-sm">
                <Mail size={14} />
                {user.email}
              </p>
            )}
          </div>
        </div>
        <button
          type="button"
          onClick={handleLogout}
          className="flex items-center gap-2 font-unbounded text-sm font-semibold text-black/70 hover:text-black border border-black/20 rounded-xl px-4 py-2.5 transition-colors"
        >
          <LogOut size={18} />
          Выйти
        </button>
      </div>
    </div>
  )
}

export default ProfilePage
