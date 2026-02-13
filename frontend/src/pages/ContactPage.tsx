import { Link } from 'react-router-dom'
import { Mail, Phone, MapPin, Clock, ArrowRight } from 'lucide-react'

const contacts = [
  {
    icon: Phone,
    label: 'Телефон',
    value: '+7 (999) 123-45-67',
    href: 'tel:+79991234567',
  },
  {
    icon: Mail,
    label: 'Email',
    value: 'info@antistress-toys.ru',
    href: 'mailto:info@antistress-toys.ru',
  },
  {
    icon: MapPin,
    label: 'Адрес',
    value: 'г. Новосибирск, ул. Советская, 64/1',
    href: null,
  },
  {
    icon: Clock,
    label: 'Режим работы',
    value: 'Пн–Пт: 10:00–20:00, Сб: 11:00–19:00, Вс: 12:00–18:00',
    href: null,
  },
]

const ContactPage = () => {
  return (
    <div className="min-h-screen">
      {/* Заголовок */}
      <section className="py-12 lg:py-16">
        <div className="max-w-2xl mx-auto px-4 text-center">
          <p className="font-unbounded text-sm uppercase tracking-[0.2em] text-black/50 mb-2">
            Связь
          </p>
          <h1 className="text-4xl lg:text-5xl font-bold font-unbounded text-black mb-4">
            Контакты
          </h1>
          <p className="text-black/70 text-lg">
            Позвоните, напишите или приезжайте — мы всегда рады ответить на ваши вопросы.
          </p>
        </div>
      </section>

      {/* Карточки контактов */}
      <section className="pb-12">
        <div className="max-w-4xl mx-auto px-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 lg:gap-6">
            {contacts.map(({ icon: Icon, label, value, href }) => (
              <div
                key={label}
                className="rounded-2xl border-2 border-black/10 bg-white/80 p-6 lg:p-8 hover:border-black/20 hover:bg-white transition-all duration-300"
              >
                <div className="w-12 h-12 rounded-xl bg-black text-white flex items-center justify-center mb-4">
                  <Icon size={24} />
                </div>
                <p className="font-unbounded text-xs uppercase tracking-wider text-black/50 mb-1">
                  {label}
                </p>
                {href ? (
                  <a
                    href={href}
                    className="font-unbounded font-semibold text-black text-lg hover:underline"
                  >
                    {value}
                  </a>
                ) : (
                  <p className="font-unbounded font-semibold text-black text-lg">
                    {value}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Чёрный блок — призыв написать */}
      <section className="rounded-2xl mx-4 lg:mx-8 bg-black text-white py-12 lg:py-16">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-2xl lg:text-3xl font-bold font-unbounded mb-3">
            Остались вопросы?
          </h2>
          <p className="text-white/80 mb-4">
            Напишите нам через форму обратной связи в правом нижнем углу страницы — ответим в течение рабочего дня.
          </p>
        </div>
      </section>

      {/* Дополнительно: быстрая ссылка на каталог */}
      <section className="py-12">
        <div className="max-w-xl mx-auto px-4 text-center">
          <p className="text-black/60 text-sm mb-2">
            Хотите выбрать игрушку?
          </p>
          <Link
            to="/catalog"
            className="font-unbounded font-semibold text-black hover:underline inline-flex items-center gap-1"
          >
            Перейти в каталог
            <ArrowRight size={16} />
          </Link>
        </div>
      </section>
    </div>
  )
}

export default ContactPage
