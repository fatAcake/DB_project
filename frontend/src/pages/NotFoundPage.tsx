import { Link } from 'react-router-dom'
import { Home, ShoppingBag } from 'lucide-react'

const NotFoundPage = () => {
  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center py-16 px-4">
      <div className="max-w-lg w-full text-center">
        <p className="font-unbounded text-[8rem] sm:text-[10rem] lg:text-[12rem] font-bold leading-none text-black/10 select-none">
          404
        </p>

        <div className="-mt-16 sm:-mt-20 lg:-mt-24 relative">
          <h1 className="text-2xl sm:text-3xl font-bold font-unbounded text-black mb-3">
            Страница укатилась, как шарик антистресс
          </h1>
          <p className="text-black/70 mb-8 max-w-md mx-auto">
            Такой страницы нет — но не стрессуйте. Вернитесь на главную или загляните в каталог: там точно найдётся что-то успокаивающее.
          </p>

          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link
              to="/"
              className="inline-flex items-center justify-center gap-2 font-unbounded font-semibold bg-black text-white rounded-2xl px-6 py-3.5 hover:bg-black/90 transition-colors"
            >
              <Home size={20} />
              На главную
            </Link>
            <Link
              to="/catalog"
              className="inline-flex items-center justify-center gap-2 font-unbounded font-semibold border-2 border-black text-black rounded-2xl px-6 py-3.5 hover:bg-black hover:text-white transition-colors"
            >
              <ShoppingBag size={20} />
              В каталог
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default NotFoundPage
