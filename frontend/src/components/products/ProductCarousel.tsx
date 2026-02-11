import { Swiper, SwiperSlide } from 'swiper/react'
import { Navigation, Pagination } from 'swiper/modules'
import { Link } from 'react-router-dom'
import { Product } from '@/types'
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

// Моковые данные для демонстрации
// Используем data URI для placeholder изображений, чтобы избежать ошибок загрузки
const createPlaceholderImage = (text: string) => {
  // Создаем простой SVG placeholder
  const svg = `
    <svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
      <rect width="400" height="400" fill="#1a1a1a"/>
      <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="24" fill="#ffffff" text-anchor="middle" dominant-baseline="middle">${text}</text>
    </svg>
  `
  return `data:image/svg+xml;base64,${btoa(unescape(encodeURIComponent(svg)))}`
}

const mockProducts: Product[] = [
  {
    id: 1,
    name: 'Антистресс кубик',
    price: 599,
    description: 'Классический антистресс кубик с вращающимися элементами. Идеально подходит для снятия напряжения.',
    image: createPlaceholderImage('Антистресс кубик'),
    category: 'Кубики',
    inStock: true,
  },
  {
    id: 2,
    name: 'Спиннер-звезда',
    price: 799,
    description: 'Красивый спиннер в форме звезды. Помогает сосредоточиться и расслабиться.',
    image: createPlaceholderImage('Спиннер-звезда'),
    category: 'Спиннеры',
    inStock: true,
  },
  {
    id: 3,
    name: 'Мяч-антистресс',
    price: 499,
    description: 'Мягкий мяч для снятия стресса. Приятная текстура и эргономичная форма.',
    image: createPlaceholderImage('Мяч-антистресс'),
    category: 'Мячи',
    inStock: true,
  },
  {
    id: 4,
    name: 'Поп-ит фиджет',
    price: 699,
    description: 'Популярный поп-ит с пузырьками. Удовлетворяющее нажатие и яркие цвета.',
    image: createPlaceholderImage('Поп-ит фиджет'),
    category: 'Поп-иты',
    inStock: true,
  },
  {
    id: 5,
    name: 'Трансформер-куб',
    price: 899,
    description: 'Многофункциональный трансформирующийся куб. Развивает моторику и снимает стресс.',
    image: createPlaceholderImage('Трансформер-куб'),
    category: 'Трансформеры',
    inStock: true,
  },
  {
    id: 6,
    name: 'Сенсорный слайм',
    price: 549,
    description: 'Приятный на ощупь слайм с различными текстурами. Отлично подходит для релаксации.',
    image: createPlaceholderImage('Сенсорный слайм'),
    category: 'Слаймы',
    inStock: true,
  },
  {
    id: 7,
    name: 'Вращающийся диск',
    price: 649,
    description: 'Плавно вращающийся диск с успокаивающим эффектом. Идеален для концентрации.',
    image: createPlaceholderImage('Вращающийся диск'),
    category: 'Диски',
    inStock: true,
  },
  {
    id: 8,
    name: 'Тактильный куб',
    price: 749,
    description: 'Куб с различными текстурами на каждой стороне. Развивает тактильные ощущения.',
    image: createPlaceholderImage('Тактильный куб'),
    category: 'Кубики',
    inStock: true,
  },
  {
    id: 9,
    name: 'Релакс-спиннер',
    price: 599,
    description: 'Классический спиннер с плавным вращением. Помогает снять напряжение.',
    image: createPlaceholderImage('Релакс-спиннер'),
    category: 'Спиннеры',
    inStock: true,
  },
]

const ProductCarousel = () => {
  // Временно используем только моковые данные, без запросов к бэкенду
  const displayProducts = mockProducts

  return (
    <div className="w-full">
      <Swiper
        modules={[Navigation, Pagination]}
        navigation
        pagination={{ clickable: true }}
        spaceBetween={24}
        slidesPerView={3}
        slidesPerGroup={3}
        breakpoints={{
          640: {
            slidesPerView: 3,
            slidesPerGroup: 3,
          },
          1024: {
            slidesPerView: 3,
            slidesPerGroup: 3,
          },
          1280: {
            slidesPerView: 3,
            slidesPerGroup: 3,
          },
        }}
        className="product-carousel !pb-12 !px-12"
      >
        {displayProducts.map((product) => (
          <SwiperSlide key={product.id} className="!h-auto">
            <div className="flex flex-col">
              <Link
                to={`/product/${product.id}`}
                className="block bg-gray-900 border border-gray-700 rounded-2xl overflow-hidden hover:bg-gray-800 hover:border-gray-600 transition-all duration-200 group"
              >
                <div className="aspect-square relative overflow-hidden bg-gray-800 rounded-2xl">
                  <img
                    src={product.image || '/placeholder-product.jpg'}
                    alt={product.name}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement
                      target.src = '/placeholder-product.jpg'
                    }}
                  />
                </div>
              </Link>
              <div className="mt-3 text-center">
                <h3 className="text-lg font-semibold mb-2 font-unbounded line-clamp-2 text-black">
                  {product.name}
                </h3>
                <div className="flex items-center justify-center">
                  <span className="text-xl font-bold font-unbounded text-black">
                    {product.price} ₽
                  </span>
                </div>
              </div>
            </div>
          </SwiperSlide>
        ))}
      </Swiper>
    </div>
  )
}

export default ProductCarousel
