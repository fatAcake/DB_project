import { Link } from 'react-router-dom'
import {
  Sparkles,
  Printer,
  Leaf,
  Heart,
  ArrowRight,
  Quote,
} from 'lucide-react'

const values = [
  {
    icon: Printer,
    title: '3D-печать',
    text: 'Каждое изделие создаётся на 3D-принтере — уникальные формы, прочные материалы, точная детализация.',
  },
  {
    icon: Leaf,
    title: 'Экологичность',
    text: 'Используем безопасные материалы и ответственный подход к производству.',
  },
  {
    icon: Heart,
    title: 'Забота о деталях',
    text: 'Внимание к каждой игрушке: от идеи до упаковки. Делаем так, чтобы вам было приятно держать в руках.',
  },
  {
    icon: Sparkles,
    title: 'Снятие стресса',
    text: 'Наша цель — помочь вам расслабиться и находить маленькие радости в повседневности.',
  },
]

const AboutPage = () => {
  return (
    <div className="min-h-screen">
      {/* Hero — визитка */}
      <section className="relative py-20 lg:py-28 overflow-hidden">
        <div className="max-w-5xl mx-auto px-4 text-center">
          <p className="font-unbounded text-sm uppercase tracking-[0.3em] text-black/60 mb-4">
            О компании
          </p>
          <h1 className="text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-bold font-unbounded text-black leading-tight mb-6">
            Антистресс игрушки
          </h1>
          <p className="text-xl lg:text-2xl text-black/80 max-w-2xl mx-auto font-medium leading-relaxed">
            Уникальные фиджеты и антистресс-игрушки, напечатанные на 3D-принтере.
            Создаём вещи, которые помогают снять напряжение и вернуть спокойствие.
          </p>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-black/20 to-transparent" />
      </section>

      {/* Миссия — чёрный блок */}
      <section className="bg-black text-white py-16 lg:py-24 rounded-2xl mx-4 lg:mx-8">
        <div className="max-w-4xl mx-auto px-4">
          <div className="flex items-start gap-4 mb-8">
            <Quote className="w-10 h-10 text-white/40 flex-shrink-0 mt-1" />
            <div>
              <h2 className="font-unbounded text-2xl lg:text-3xl font-bold mb-6">
                Наша миссия
              </h2>
              <p className="text-lg lg:text-xl text-white/90 leading-relaxed">
                Помогать людям справляться со стрессом и находить моменты радости
                с помощью качественных, приятных на ощупь изделий. Мы верим, что
                маленькие тактильные радости делают день лучше — и создаём их
                с заботой.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Ценности — карточки */}
      <section className="py-16 lg:py-24">
        <div className="max-w-6xl mx-auto px-4">
          <p className="font-unbounded text-sm uppercase tracking-[0.2em] text-black/50 mb-2">
            Что для нас важно
          </p>
          <h2 className="text-3xl lg:text-4xl font-bold font-unbounded text-black mb-12">
            Наши ценности
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {values.map(({ icon: Icon, title, text }) => (
              <div
                key={title}
                className="group p-6 lg:p-8 rounded-2xl border-2 border-black/10 bg-white/60 hover:border-black/25 hover:bg-white/80 transition-all duration-300"
              >
                <div className="w-12 h-12 rounded-xl bg-black text-white flex items-center justify-center mb-4 group-hover:scale-105 transition-transform">
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

      {/* История / подход */}
      <section className="py-16 lg:py-24 bg-black/5 rounded-2xl mx-4 lg:mx-8">
        <div className="max-w-5xl mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
            <div>
              <p className="font-unbounded text-sm uppercase tracking-[0.2em] text-black/50 mb-2">
                Как мы работаем
              </p>
              <h2 className="text-3xl lg:text-4xl font-bold font-unbounded text-black mb-6">
                От идеи до ваших рук
              </h2>
              <p className="text-black/80 leading-relaxed mb-4">
                Мы специализируемся на создании антистресс-игрушек и фиджетов
                с помощью 3D-печати. Каждое изделие проектируется и изготавливается
                с вниманием к форме, материалу и тактильным ощущениям.
              </p>
              <p className="text-black/80 leading-relaxed">
                Наш ассортимент — от классических спиннеров и кубиков до уникальных
                форм, которые вы не найдёте в обычных магазинах. Мы за экологичный
                подход и долговечность: игрушки созданы, чтобы служить вам долго.
              </p>
            </div>
            <div className="rounded-2xl bg-black text-white p-8 lg:p-10 font-unbounded">
              <p className="text-4xl lg:text-5xl font-bold leading-tight">
                Уникальные изделия для снятия напряжения и релаксации.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 lg:py-24">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-2xl lg:text-3xl font-bold font-unbounded text-black mb-4">
            Готовы найти свой антистресс?
          </h2>
          <p className="text-black/70 mb-8 max-w-xl mx-auto">
            Выберите игрушку в каталоге или напишите нам — мы поможем с выбором.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              to="/catalog"
              className="inline-flex items-center gap-2 font-unbounded font-semibold bg-black text-white rounded-2xl px-8 py-4 hover:bg-black/90 transition-colors"
            >
              Смотреть каталог
              <ArrowRight size={20} />
            </Link>
            <Link
              to="/contact"
              className="inline-flex items-center gap-2 font-unbounded font-semibold border-2 border-black text-black rounded-2xl px-8 py-4 hover:bg-black hover:text-white transition-colors"
            >
              Связаться с нами
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}

export default AboutPage
