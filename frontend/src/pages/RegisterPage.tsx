import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Mail, Lock, User, ArrowRight, CheckCircle } from 'lucide-react'
import { useRegister } from '@/api/auth'

const steps = [
  { num: 1, label: 'Регистрация', active: true },
  { num: 2, label: 'Настройка профиля', active: false },
  { num: 3, label: 'Первый заказ', active: false },
]

const RegisterPage = () => {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const register = useRegister()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    register.mutate(
      { name, email, password },
      {
        onSuccess: () => navigate('/'),
        onError: () => {},
      }
    )
  }

  return (
    <div
      className="min-h-screen w-full flex items-center justify-center py-12 px-4"
      style={{
        backgroundImage: `
          linear-gradient(rgba(0,0,0,0.06) 1px, transparent 1px),
          linear-gradient(90deg, rgba(0,0,0,0.06) 1px, transparent 1px),
          linear-gradient(180deg, #e8e6ec 0%, #ddd8e4 50%, #e2dee8 100%)
        `,
        backgroundSize: '40px 40px, 40px 40px, 100% 100%',
      }}
    >
      <div className="w-full max-w-5xl">
        <div className="rounded-3xl overflow-hidden shadow-2xl bg-white flex flex-col lg:flex-row min-h-[560px]">
          {/* Левая колонка — градиент и шаги */}
          <div
            className="relative lg:w-[42%] p-10 lg:p-12 flex flex-col justify-center text-white overflow-hidden"
            style={{
              background:
                'linear-gradient(160deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%)',
            }}
          >
            <div
              className="absolute inset-0 opacity-30"
              style={{
                background:
                  'radial-gradient(ellipse 80% 50% at 20% 80%, rgba(147, 112, 219, 0.4), transparent), radial-gradient(ellipse 60% 60% at 80% 20%, rgba(100, 149, 237, 0.25), transparent)',
              }}
            />
            <div className="relative">
              <h2 className="font-unbounded text-2xl lg:text-3xl font-bold leading-tight mb-3">
                Начните с нами
              </h2>
              <p className="text-white/80 text-sm mb-8">
                Пройдите несколько шагов, чтобы создать аккаунт.
              </p>
              <div className="space-y-3">
                {steps.map(({ num, label, active }) => (
                  <div
                    key={num}
                    className={`flex items-center gap-4 rounded-2xl px-4 py-3 transition-colors ${
                      active ? 'bg-white/15' : 'bg-white/5'
                    }`}
                  >
                    <span
                      className={`w-9 h-9 rounded-full flex items-center justify-center font-unbounded font-bold text-sm ${
                        active ? 'bg-white text-black' : 'bg-white/20 text-white'
                      }`}
                    >
                      {num}
                    </span>
                    <span className="font-unbounded font-medium text-sm">
                      {label}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Правая колонка — форма */}
          <div className="flex-1 p-8 lg:p-12 flex flex-col justify-center">
            <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-black text-white mb-6">
              <CheckCircle size={24} />
            </div>
            <h1 className="font-unbounded text-2xl lg:text-3xl font-bold text-black mb-1">
              Регистрация
            </h1>
            <p className="text-black/60 text-sm mb-8">
              Введите данные, чтобы создать аккаунт
            </p>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label htmlFor="reg-name" className="block text-sm font-medium text-black/70 mb-1.5">
                  Имя
                </label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-black/40" />
                  <input
                    id="reg-name"
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                    placeholder="Как к вам обращаться"
                    className="w-full pl-10 pr-4 py-3 rounded-xl border-2 border-black/15 focus:border-black focus:outline-none font-unbounded text-sm transition-colors"
                  />
                </div>
              </div>
              <div>
                <label htmlFor="reg-email" className="block text-sm font-medium text-black/70 mb-1.5">
                  Email
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-black/40" />
                  <input
                    id="reg-email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    placeholder="example@mail.ru"
                    className="w-full pl-10 pr-4 py-3 rounded-xl border-2 border-black/15 focus:border-black focus:outline-none font-unbounded text-sm transition-colors"
                  />
                </div>
              </div>
              <div>
                <label htmlFor="reg-password" className="block text-sm font-medium text-black/70 mb-1.5">
                  Пароль
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-black/40" />
                  <input
                    id="reg-password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    minLength={8}
                    placeholder="Не менее 8 символов"
                    className="w-full pl-10 pr-4 py-3 rounded-xl border-2 border-black/15 focus:border-black focus:outline-none font-unbounded text-sm transition-colors"
                  />
                </div>
                <p className="mt-1 text-xs text-black/50">Минимум 8 символов</p>
              </div>
              {register.isError && (
                <p className="text-sm text-red-600">
                  {(register.error as Error)?.message || 'Ошибка регистрации'}
                </p>
              )}
              <button
                type="submit"
                disabled={register.isPending}
                className="w-full font-unbounded font-semibold bg-black text-white rounded-2xl py-3.5 hover:bg-black/90 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
              >
                {register.isPending ? 'Создание…' : 'Создать аккаунт'}
                <ArrowRight size={20} />
              </button>
            </form>

            <p className="mt-6 text-center text-black/60 text-sm">
              Уже есть аккаунт?{' '}
              <Link to="/login" className="font-unbounded font-semibold text-black underline hover:no-underline">
                Войти
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RegisterPage
