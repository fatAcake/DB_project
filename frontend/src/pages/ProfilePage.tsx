import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Lock, User, Mail, KeyRound, ArrowRight, CheckCircle, Shield } from 'lucide-react'
import { useAuthStore } from '@/store/useAuthStore'

/** Для демо: код 123456 считается верным. В проде — проверка на бэкенде */
const DEMO_CODE = '123456'

const ProfilePage = () => {
  const { user, isAuthenticated } = useAuthStore()
  const navigate = useNavigate()

  const [passwordStep, setPasswordStep] = useState<'current' | 'code' | 'done'>('current')
  const [currentPassword, setCurrentPassword] = useState('')
  const [code, setCode] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [codeSent, setCodeSent] = useState(false)
  const [resendCooldown, setResendCooldown] = useState(0)
  const [error, setError] = useState('')

  if (!isAuthenticated || !user) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-black/5 mb-6">
          <User size={40} className="text-black/50" />
        </div>
        <h1 className="text-2xl font-unbounded font-bold text-black mb-2">
          Войдите в аккаунт
        </h1>
        <p className="text-black/70 mb-8">
          Чтобы просматривать профиль, авторизуйтесь.
        </p>
        <button
          type="button"
          onClick={() => navigate('/login')}
          className="inline-flex items-center gap-2 font-unbounded font-semibold bg-black text-white rounded-2xl px-6 py-3 hover:bg-black/90 transition-colors"
        >
          Войти
          <ArrowRight size={18} />
        </button>
      </div>
    )
  }

  const handleRequestCode = (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    if (!currentPassword.trim()) {
      setError('Введите текущий пароль')
      return
    }
    // TODO: API — отправить код на email пользователя
    setCodeSent(true)
    setPasswordStep('code')
    setResendCooldown(60)
    const id = setInterval(() => {
      setResendCooldown((s) => {
        if (s <= 1) {
          clearInterval(id)
          return 0
        }
        return s - 1
      })
    }, 1000)
  }

  const handleChangePassword = (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    const trimmedCode = code.replace(/\D/g, '')
    if (trimmedCode.length !== 6) {
      setError('Введите 6-значный код')
      return
    }
    if (trimmedCode !== DEMO_CODE) {
      setError('Неверный код подтверждения')
      return
    }
    if (newPassword.length < 8) {
      setError('Пароль не менее 8 символов')
      return
    }
    if (newPassword !== confirmPassword) {
      setError('Пароли не совпадают')
      return
    }
    // TODO: API — сменить пароль с проверкой кода
    setPasswordStep('done')
    setCurrentPassword('')
    setCode('')
    setNewPassword('')
    setConfirmPassword('')
  }

  const handleResendCode = () => {
    if (resendCooldown > 0) return
    setResendCooldown(60)
    const id = setInterval(() => {
      setResendCooldown((s) => {
        if (s <= 1) {
          clearInterval(id)
          return 0
        }
        return s - 1
      })
    }, 1000)
    // TODO: API — повторная отправка кода
  }

  return (
    <div className="max-w-2xl mx-auto py-8">
      <h1 className="text-3xl font-unbounded font-bold text-black mb-2">
        Профиль
      </h1>
      <p className="text-black/60 text-sm mb-8">
        Данные аккаунта и настройки безопасности
      </p>

      {/* Карточка пользователя */}
      <div className="rounded-2xl border-2 border-black/10 bg-white/90 p-6 mb-8">
        <div className="flex items-center gap-4">
          <span className="w-16 h-16 rounded-2xl bg-black text-white flex items-center justify-center font-unbounded font-bold text-2xl">
            {user.name.charAt(0).toUpperCase()}
          </span>
          <div>
            <p className="font-unbounded font-semibold text-black text-lg">
              {user.surname ? `${user.surname} ${user.name}` : user.name}
              {user.patronymic ? ` ${user.patronymic}` : ''}
            </p>
            <p className="flex items-center gap-2 text-black/70 text-sm mt-0.5">
              <Mail size={16} />
              {user.email}
            </p>
          </div>
        </div>
      </div>

      {/* Изменение пароля */}
      <div className="rounded-2xl border-2 border-black/10 bg-white/90 overflow-hidden">
        <div className="flex items-center gap-3 px-6 py-4 bg-black/5 border-b border-black/10">
          <KeyRound size={22} className="text-black/70" />
          <h2 className="font-unbounded font-semibold text-black">
            Изменить пароль
          </h2>
        </div>
        <div className="p-6">
          {passwordStep === 'done' && (
            <div className="flex items-center gap-3 p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 mb-6">
              <CheckCircle size={24} />
              <span className="font-medium">Пароль успешно изменён.</span>
            </div>
          )}

          {passwordStep === 'current' && (
            <form onSubmit={handleRequestCode} className="space-y-4">
              <p className="text-black/70 text-sm">
                Введите текущий пароль. Мы отправим код подтверждения на вашу почту.
              </p>
              <div>
                <label htmlFor="profile-current-password" className="block text-sm font-medium text-black/70 mb-1.5">
                  Текущий пароль
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-black/40" />
                  <input
                    id="profile-current-password"
                    type="password"
                    value={currentPassword}
                    onChange={(e) => setCurrentPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full pl-10 pr-4 py-3 rounded-xl border-2 border-black/15 focus:border-black focus:outline-none font-unbounded text-sm"
                  />
                </div>
              </div>
              {error && <p className="text-red-600 text-sm">{error}</p>}
              <button
                type="submit"
                className="font-unbounded font-semibold bg-black text-white rounded-xl px-6 py-2.5 hover:bg-black/90 transition-colors flex items-center gap-2"
              >
                <Shield size={18} />
                Получить код на почту
              </button>
            </form>
          )}

          {passwordStep === 'code' && (
            <form onSubmit={handleChangePassword} className="space-y-4">
              <p className="text-black/70 text-sm">
                Код отправлен на <strong>{user.email}</strong>. Введите его и новый пароль.
              </p>
              <div>
                <label htmlFor="profile-code" className="block text-sm font-medium text-black/70 mb-1.5">
                  Код подтверждения (6 цифр)
                </label>
                <input
                  id="profile-code"
                  type="text"
                  inputMode="numeric"
                  maxLength={6}
                  value={code}
                  onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
                  placeholder="123456"
                  className="w-full px-4 py-3 rounded-xl border-2 border-black/15 focus:border-black focus:outline-none font-unbounded text-sm tracking-widest text-center"
                />
              </div>
              <div>
                <label htmlFor="profile-new-password" className="block text-sm font-medium text-black/70 mb-1.5">
                  Новый пароль
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-black/40" />
                  <input
                    id="profile-new-password"
                    type="password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    minLength={8}
                    placeholder="Не менее 8 символов"
                    className="w-full pl-10 pr-4 py-3 rounded-xl border-2 border-black/15 focus:border-black focus:outline-none font-unbounded text-sm"
                  />
                </div>
              </div>
              <div>
                <label htmlFor="profile-confirm-password" className="block text-sm font-medium text-black/70 mb-1.5">
                  Повторите новый пароль
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-black/40" />
                  <input
                    id="profile-confirm-password"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full pl-10 pr-4 py-3 rounded-xl border-2 border-black/15 focus:border-black focus:outline-none font-unbounded text-sm"
                  />
                </div>
              </div>
              {error && <p className="text-red-600 text-sm">{error}</p>}
              <div className="flex flex-wrap items-center gap-3">
                <button
                  type="submit"
                  className="font-unbounded font-semibold bg-black text-white rounded-xl px-6 py-2.5 hover:bg-black/90 transition-colors"
                >
                  Изменить пароль
                </button>
                <button
                  type="button"
                  onClick={handleResendCode}
                  disabled={resendCooldown > 0}
                  className="font-unbounded text-sm text-black/70 hover:text-black disabled:opacity-50"
                >
                  {resendCooldown > 0
                    ? `Отправить повторно (${resendCooldown} с)`
                    : 'Отправить код повторно'}
                </button>
              </div>
            </form>
          )}

          {passwordStep === 'done' && (
            <button
              type="button"
              onClick={() => setPasswordStep('current')}
              className="font-unbounded font-semibold text-black/70 hover:text-black"
            >
              Изменить пароль снова
            </button>
          )}
        </div>
      </div>

      <p className="mt-6 text-black/50 text-sm">
        <Link to="/profile/orders" className="font-unbounded font-semibold text-black underline hover:no-underline">
          Мои заказы
        </Link>
      </p>
    </div>
  )
}

export default ProfilePage
