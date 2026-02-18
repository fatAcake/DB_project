import { Link } from 'react-router-dom'
import {
  Printer,
  Download,
  FileOutput,
  Box,
  ArrowRight,
  Layers,
  Wrench,
} from 'lucide-react'

const steps = [
  {
    icon: Download,
    title: 'Скачайте модель',
    text: 'STL-файлы наших антистресс-игрушек. Бесплатно для личного использования.',
  },
  {
    icon: Printer,
    title: 'Настройте печать',
    text: 'Откройте в слайсере, выберите материал и параметры под ваш принтер.',
  },
  {
    icon: Box,
    title: 'Напечатайте',
    text: 'Запустите печать и через несколько часов получите свою игрушку.',
  },
]

const comingSoonItems = [
  { name: 'Антистресс-кубик', format: 'STL', size: '~2 MB' },
  { name: 'Спиннер-звезда', format: 'STL', size: '~1.5 MB' },
  { name: 'Поп-ит фиджет', format: 'STL', size: '~3 MB' },
]

const WorkshopPage = () => {
  return (
    <div className="min-h-screen">
      {/* Hero */}
      <section className="relative py-16 lg:py-24 overflow-hidden">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <p className="font-unbounded text-sm uppercase tracking-[0.2em] text-black/50 mb-3">
            Мастерская
          </p>
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold font-unbounded text-black leading-tight mb-5">
            Печатайте сами
          </h1>
          <p className="text-lg lg:text-xl text-black/75 max-w-2xl mx-auto leading-relaxed">
            Модели для 3D-печати антистресс-игрушек. Скачивайте STL, настраивайте под свой принтер и создавайте фиджеты своими руками.
          </p>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-black/15 to-transparent" />
      </section>

      {/* Как это работает */}
      <section className="py-14 lg:py-20">
        <div className="max-w-5xl mx-auto px-4">
          <p className="font-unbounded text-sm uppercase tracking-[0.2em] text-black/50 mb-2">
            Три шага
          </p>
          <h2 className="text-2xl lg:text-3xl font-bold font-unbounded text-black mb-10">
            Как это работает
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
            {steps.map(({ icon: Icon, title, text }, i) => (
              <div
                key={title}
                className="relative rounded-2xl border-2 border-black/10 bg-white/70 p-6 lg:p-8 hover:border-black/20 transition-all duration-300"
              >
                <span className="absolute -top-3 -left-1 w-8 h-8 rounded-full bg-black text-white flex items-center justify-center font-unbounded font-bold text-sm">
                  {i + 1}
                </span>
                <div className="w-12 h-12 rounded-xl bg-black text-white flex items-center justify-center mb-4">
                  <Icon size={24} />
                </div>
                <h3 className="font-unbounded font-bold text-lg text-black mb-2">
                  {title}
                </h3>
                <p className="text-black/70 text-sm leading-relaxed">{text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Чёрный блок — приглашение */}
      <section className="rounded-2xl mx-4 lg:mx-8 bg-black text-white py-12 lg:py-16">
        <div className="max-w-4xl mx-auto px-4 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-8">
          <div className="flex items-start gap-4">
            <div className="w-14 h-14 rounded-2xl bg-white/10 flex items-center justify-center flex-shrink-0">
              <Layers size={28} />
            </div>
            <div>
              <h2 className="font-unbounded text-2xl lg:text-3xl font-bold mb-2">
                Модели для 3D-печати
              </h2>
              <p className="text-white/80">
                Мы готовим к публикации STL-файлы наших популярных игрушек. Скоро здесь появятся первые модели — бесплатно для некоммерческого использования.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Карточки «скоро» */}
      <section className="py-14 lg:py-20">
        <div className="max-w-5xl mx-auto px-4">
          <p className="font-unbounded text-sm uppercase tracking-[0.2em] text-black/50 mb-2">
            Уже в работе
          </p>
          <h2 className="text-2xl lg:text-3xl font-bold font-unbounded text-black mb-8">
            Чертежи и модели
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {comingSoonItems.map(({ name, format, size }) => (
              <div
                key={name}
                className="group flex items-center gap-4 p-5 rounded-2xl border-2 border-black/10 bg-white/60 hover:border-black/20 hover:bg-white/80 transition-all"
              >
                <div className="w-12 h-12 rounded-xl bg-black/5 flex items-center justify-center group-hover:bg-black/10 transition-colors">
                  <FileOutput size={24} className="text-black/70" />
                </div>
                <div className="min-w-0 flex-1">
                  <h3 className="font-unbounded font-semibold text-black truncate">
                    {name}
                  </h3>
                  <p className="text-sm text-black/55">
                    {format} · {size}
                  </p>
                </div>
                <span className="font-unbounded text-xs font-semibold text-black/50 bg-black/5 px-2.5 py-1 rounded-lg">
                  Скоро
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-12 lg:py-16">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-black/5 mb-5">
            <Wrench size={28} className="text-black/70" />
          </div>
          <h2 className="text-xl lg:text-2xl font-bold font-unbounded text-black mb-3">
            Пока модели готовятся — загляните в каталог
          </h2>
          <p className="text-black/65 mb-6">
            Готовые антистресс-игрушки с доставкой. Не хотите печатать сами? Мы уже напечатали.
          </p>
          <Link
            to="/catalog"
            className="inline-flex items-center gap-2 font-unbounded font-semibold bg-black text-white rounded-2xl px-6 py-3.5 hover:bg-black/90 transition-colors"
          >
            Смотреть каталог
            <ArrowRight size={20} />
          </Link>
        </div>
      </section>
    </div>
  )
}

export default WorkshopPage
