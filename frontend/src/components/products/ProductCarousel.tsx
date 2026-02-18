import { Swiper, SwiperSlide } from 'swiper/react'
import { Navigation, Pagination } from 'swiper/modules'
import { Link } from 'react-router-dom'
import { useProducts } from '@/api/products'
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

const ProductCarousel = () => {
  const { data: displayProducts = [] } = useProducts()

  if (displayProducts.length === 0) return null

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
