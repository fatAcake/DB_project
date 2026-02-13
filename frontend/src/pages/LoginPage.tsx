import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Mail, Lock, ArrowRight, Sparkles } from 'lucide-react'

const LoginPage = () => {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: интеграция с API авторизации
    navigate('/')
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
        <div className="rounded-3xl overflow-hidden shadow-2xl bg-white flex flex-col lg:flex-row min-h-[520px]">
          {/* Левая колонка — градиент и слоган */}
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
              <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-white/10 mb-8">
                <Sparkles size={28} />
              </div>
              <h2 className="font-unbounded text-2xl lg:text-3xl font-bold leading-tight mb-4">
                Превращайте идеи в уютные игрушки
              </h2>
              <p className="text-white/80 text-lg">
                Войдите в аккаунт, чтобы оформлять заказы и следить за новинками.
              </p>
            </div>
          </div>

          {/* Правая колонка — форма */}
          <div className="flex-1 p-8 lg:p-12 flex flex-col justify-center">
            <h1 className="font-unbounded text-2xl lg:text-3xl font-bold text-black mb-1">
              Вход
            </h1>
            <p className="text-black/60 text-sm mb-8">
              Добро пожаловать — введите данные для входа
            </p>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label htmlFor="login-email" className="block text-sm font-medium text-black/70 mb-1.5">
                  Email
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-black/40" />
                  <input
                    id="login-email"
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
                <label htmlFor="login-password" className="block text-sm font-medium text-black/70 mb-1.5">
                  Пароль
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-black/40" />
                  <input
                    id="login-password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    placeholder="••••••••"
                    className="w-full pl-10 pr-4 py-3 rounded-xl border-2 border-black/15 focus:border-black focus:outline-none font-unbounded text-sm transition-colors"
                  />
                </div>
              </div>
              <button
                type="submit"
                className="w-full font-unbounded font-semibold bg-black text-white rounded-2xl py-3.5 hover:bg-black/90 transition-colors flex items-center justify-center gap-2"
              >
                Войти
                <ArrowRight size={20} />
              </button>
            </form>

            <p className="mt-6 text-center text-black/60 text-sm">
              Нет аккаунта?{' '}
              <Link to="/register" className="font-unbounded font-semibold text-black underline hover:no-underline">
                Зарегистрироваться
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LoginPage
