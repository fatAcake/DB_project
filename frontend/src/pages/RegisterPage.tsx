import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Mail, Lock, User, ArrowRight, CheckCircle, FileText, ShoppingBag, Store, ShieldCheck } from 'lucide-react'
import type { UserRole } from '@/store/useAuthStore'

/** Для демо: код 123456 считается верным. В проде — проверка на бэкенде */
const DEMO_VERIFICATION_CODE = '123456'

const steps = [
  { num: 1, label: 'Регистрация', active: true },
  { num: 2, label: 'Настройка профиля', active: false },
  { num: 3, label: 'Первый заказ', active: false },
]

const RegisterPage = () => {
  const navigate = useNavigate()
  const [step, setStep] = useState<'form' | 'code'>('form')
  const [name, setName] = useState('')
  const [surname, setSurname] = useState('')
  const [patronymic, setPatronymic] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState<UserRole>('buyer')
  const [passportSeries, setPassportSeries] = useState('')
  const [passportNumber, setPassportNumber] = useState('')
  const [passportIssuedBy, setPassportIssuedBy] = useState('')
  const [passportIssueDate, setPassportIssueDate] = useState('')
  const [code, setCode] = useState('')
  const [codeError, setCodeError] = useState('')
  const [resendCooldown, setResendCooldown] = useState(0)

  const handleSubmitForm = (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: API — отправить данные и код на email
    setStep('code')
  }

  const handleConfirmCode = (e: React.FormEvent) => {
    e.preventDefault()
    setCodeError('')
    const trimmed = code.replace(/\D/g, '')
    if (trimmed.length !== 6) {
      setCodeError('Введите 6-значный код')
      return
    }
    if (trimmed !== DEMO_VERIFICATION_CODE) {
      setCodeError('Неверный код')
      return
    }
    // TODO: API — подтвердить регистрацию
    navigate('/')
  }

  const handleResendCode = () => {
    if (resendCooldown > 0) return
    setResendCooldown(60)
    const id = setInterval(() => {
      setResendCooldown((s) => (s <= 1 ? (clearInterval(id), 0) : s - 1))
    }, 1000)
    setCodeError('')
    // TODO: API — повторная отправка кода
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

          {/* Правая колонка — форма или подтверждение кода */}
          <div className="flex-1 p-8 lg:p-12 flex flex-col justify-center">
            {step === 'form' ? (
              <>
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-black text-white mb-6">
                  <CheckCircle size={24} />
                </div>
                <h1 className="font-unbounded text-2xl lg:text-3xl font-bold text-black mb-1">
                  Регистрация
                </h1>
                <p className="text-black/60 text-sm mb-8">
                  Введите данные, чтобы создать аккаунт
                </p>

                <form onSubmit={handleSubmitForm} className="space-y-5">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label htmlFor="reg-surname" className="block text-sm font-medium text-black/70 mb-1.5">
                    Фамилия
                  </label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-black/40" />
                    <input
                      id="reg-surname"
                      type="text"
                      value={surname}
                      onChange={(e) => setSurname(e.target.value)}
                      required
                      placeholder="Фамилия"
                      className="w-full pl-10 pr-4 py-3 rounded-xl border-2 border-black/15 focus:border-black focus:outline-none font-unbounded text-sm transition-colors"
                    />
                  </div>
                </div>
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
                      placeholder="Имя"
                      className="w-full pl-10 pr-4 py-3 rounded-xl border-2 border-black/15 focus:border-black focus:outline-none font-unbounded text-sm transition-colors"
                    />
                  </div>
                </div>
                <div>
                  <label htmlFor="reg-patronymic" className="block text-sm font-medium text-black/70 mb-1.5">
                    Отчество
                  </label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-black/40" />
                    <input
                      id="reg-patronymic"
                      type="text"
                      value={patronymic}
                      onChange={(e) => setPatronymic(e.target.value)}
                      placeholder="Отчество"
                      className="w-full pl-10 pr-4 py-3 rounded-xl border-2 border-black/15 focus:border-black focus:outline-none font-unbounded text-sm transition-colors"
                    />
                  </div>
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
              <div>
                <span className="block text-sm font-medium text-black/70 mb-2">
                  Регистрация как
                </span>
                <div className="flex gap-4">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      name="role"
                      checked={role === 'buyer'}
                      onChange={() => setRole('buyer')}
                      className="w-4 h-4 border-2 border-black/30 text-black focus:ring-black"
                    />
                    <ShoppingBag size={18} className="text-black/60" />
                    <span className="font-unbounded text-sm">Покупатель</span>
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      name="role"
                      checked={role === 'seller'}
                      onChange={() => setRole('seller')}
                      className="w-4 h-4 border-2 border-black/30 text-black focus:ring-black"
                    />
                    <Store size={18} className="text-black/60" />
                    <span className="font-unbounded text-sm">Продавец</span>
                  </label>
                </div>
              </div>
              {role === 'seller' && (
                <div className="space-y-4 p-4 rounded-2xl border-2 border-black/10 bg-black/[0.02]">
                  <div className="flex items-center gap-2 mb-2">
                    <FileText className="w-5 h-5 text-black/40" />
                    <span className="text-sm font-medium text-black/70">Паспортные данные</span>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label htmlFor="reg-passport-series" className="block text-xs font-medium text-black/60 mb-1">
                        Серия
                      </label>
                      <input
                        id="reg-passport-series"
                        type="text"
                        inputMode="numeric"
                        maxLength={4}
                        value={passportSeries}
                        onChange={(e) => setPassportSeries(e.target.value.replace(/\D/g, '').slice(0, 4))}
                        required
                        placeholder="1234"
                        className="w-full px-4 py-3 rounded-xl border-2 border-black/15 focus:border-black focus:outline-none font-unbounded text-sm transition-colors"
                      />
                    </div>
                    <div>
                      <label htmlFor="reg-passport-number" className="block text-xs font-medium text-black/60 mb-1">
                        Номер
                      </label>
                      <input
                        id="reg-passport-number"
                        type="text"
                        inputMode="numeric"
                        maxLength={6}
                        value={passportNumber}
                        onChange={(e) => setPassportNumber(e.target.value.replace(/\D/g, '').slice(0, 6))}
                        required
                        placeholder="567890"
                        className="w-full px-4 py-3 rounded-xl border-2 border-black/15 focus:border-black focus:outline-none font-unbounded text-sm transition-colors"
                      />
                    </div>
                  </div>
                  <div>
                    <label htmlFor="reg-passport-issued-by" className="block text-xs font-medium text-black/60 mb-1">
                      Кем выдан
                    </label>
                    <input
                      id="reg-passport-issued-by"
                      type="text"
                      value={passportIssuedBy}
                      onChange={(e) => setPassportIssuedBy(e.target.value)}
                      required
                      placeholder="ОУФМС России по г. Москве"
                      className="w-full px-4 py-3 rounded-xl border-2 border-black/15 focus:border-black focus:outline-none font-unbounded text-sm transition-colors"
                    />
                  </div>
                  <div>
                    <label htmlFor="reg-passport-issue-date" className="block text-xs font-medium text-black/60 mb-1">
                      Дата выдачи
                    </label>
                    <input
                      id="reg-passport-issue-date"
                      type="date"
                      value={passportIssueDate}
                      onChange={(e) => setPassportIssueDate(e.target.value)}
                      required
                      className="w-full px-4 py-3 rounded-xl border-2 border-black/15 focus:border-black focus:outline-none font-unbounded text-sm transition-colors"
                    />
                  </div>
                </div>
              )}
              <button
                type="submit"
                className="w-full font-unbounded font-semibold bg-black text-white rounded-2xl py-3.5 hover:bg-black/90 transition-colors flex items-center justify-center gap-2"
              >
                Создать аккаунт
                <ArrowRight size={20} />
              </button>
            </form>

                <p className="mt-6 text-center text-black/60 text-sm">
                  Уже есть аккаунт?{' '}
                  <Link to="/login" className="font-unbounded font-semibold text-black underline hover:no-underline">
                    Войти
                  </Link>
                </p>
              </>
            ) : (
              <>
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-black text-white mb-6">
                  <ShieldCheck size={24} />
                </div>
                <h1 className="font-unbounded text-2xl lg:text-3xl font-bold text-black mb-1">
                  Подтверждение email
                </h1>
                <p className="text-black/60 text-sm mb-6">
                  Мы отправили 6-значный код на <strong>{email}</strong>. Введите его ниже.
                </p>

                <form onSubmit={handleConfirmCode} className="space-y-5">
                  <div>
                    <label htmlFor="reg-code" className="block text-sm font-medium text-black/70 mb-1.5">
                      Код подтверждения
                    </label>
                    <input
                      id="reg-code"
                      type="text"
                      inputMode="numeric"
                      maxLength={6}
                      value={code}
                      onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
                      placeholder="123456"
                      className="w-full px-4 py-3 rounded-xl border-2 border-black/15 focus:border-black focus:outline-none font-unbounded text-sm tracking-widest text-center"
                    />
                  </div>
                  {codeError && <p className="text-red-600 text-sm">{codeError}</p>}
                  <button
                    type="submit"
                    className="w-full font-unbounded font-semibold bg-black text-white rounded-2xl py-3.5 hover:bg-black/90 transition-colors flex items-center justify-center gap-2"
                  >
                    Подтвердить
                    <ArrowRight size={20} />
                  </button>
                </form>
                <p className="mt-4 text-center text-black/60 text-sm">
                  Не пришёл код?{' '}
                  <button
                    type="button"
                    onClick={handleResendCode}
                    disabled={resendCooldown > 0}
                    className="font-unbounded font-semibold text-black underline hover:no-underline disabled:opacity-50"
                  >
                    {resendCooldown > 0 ? `Отправить повторно (${resendCooldown} с)` : 'Отправить повторно'}
                  </button>
                </p>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default RegisterPage
