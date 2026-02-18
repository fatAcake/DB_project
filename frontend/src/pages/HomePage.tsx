import { Link } from 'react-router-dom'
import { ArrowRight, Sparkles } from 'lucide-react'
import ProductCarousel from '@/components/products/ProductCarousel'

const HomePage = () => {
  return (
    <div className="min-h-screen overflow-x-hidden">
      <section className="py-16 lg:py-24">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto text-center mb-10">
            <h1 className="text-5xl lg:text-6xl font-bold font-unbounded">
              Антистресс игрушки
            </h1>
          </div>
        </div>

        {/* Блок на всю ширину страницы (break-out из контейнера) */}
        <div
          className="w-screen relative left-1/2 right-1/2 -ml-[50vw] -mr-[50vw] mb-14 lg:mb-16 px-4 sm:px-6 lg:px-8"
          style={{ boxSizing: 'content-box' }}
        >
          <Link
            to="/catalog"
            className="group block w-full rounded-none lg:rounded-2xl bg-black text-white p-6 sm:p-8 lg:p-10 xl:p-12 border-0 border-y-2 border-black hover:border-black/80 transition-all duration-300"
          >
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6 lg:gap-10 xl:gap-12 max-w-6xl mx-auto">
              <div className="flex-1 min-w-0">
                <div className="inline-flex items-center gap-2 text-white/70 text-sm font-unbounded uppercase tracking-wider mb-3">
                  <Sparkles size={18} />
                  Уникальные фиджеты
                </div>
                <h2 className="text-2xl sm:text-3xl lg:text-4xl xl:text-[2.5rem] font-bold font-unbounded leading-tight mb-2 lg:mb-3">
                  Снять напряжение за минуту
                </h2>
                <p className="text-white/80 text-base sm:text-lg lg:text-xl max-w-2xl">
                  Спиннеры, кубики, поп-иты и другие антистресс-игрушки, напечатанные на 3D-принтере. Выберите то, что подходит вам.
                </p>
              </div>
              <span className="inline-flex items-center gap-2 font-unbounded font-semibold text-white text-lg lg:text-xl group-hover:gap-3 transition-all lg:flex-shrink-0">
                Смотреть каталог
                <ArrowRight size={24} />
              </span>
            </div>
          </Link>
        </div>

        <div className="container mx-auto px-4">
          <ProductCarousel />
        </div>
      </section>
    </div>
  )
}

export default HomePage
