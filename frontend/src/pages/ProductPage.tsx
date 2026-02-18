import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { ArrowLeft, ShoppingCart, Package, Minus, Plus } from 'lucide-react'
import { useProduct } from '@/api/products'
import { useCartStore } from '@/store/useCartStore'
import { useLogAction } from '@/hooks/useLogAction'
import LoadingSpinner from '@/components/common/LoadingSpinner'
import ErrorMessage from '@/components/common/ErrorMessage'

const ProductPage = () => {
  const { id } = useParams<{ id: string }>()
  const [quantity, setQuantity] = useState(1)
  const addToCart = useCartStore((s) => s.addItem)
  const { logAction } = useLogAction()
  const productId = id ? parseInt(id, 10) : undefined
  const { data: product, isLoading, isError, error } = useProduct(productId)

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto py-12 flex justify-center">
        <LoadingSpinner />
      </div>
    )
  }
  if (isError || !product) {
    return (
      <div className="max-w-4xl mx-auto py-12 text-center">
        <h1 className="text-2xl font-unbounded font-bold text-black mb-4">
          {isError ? (error instanceof Error ? error.message : 'Ошибка загрузки') : 'Товар не найден'}
        </h1>
        {isError && <ErrorMessage message={error instanceof Error ? error.message : 'Ошибка'} />}
        <Link
          to="/catalog"
          className="inline-flex items-center gap-2 font-unbounded text-black border-2 border-black rounded-2xl px-5 py-2.5 hover:bg-black hover:text-white transition-colors mt-4"
        >
          <ArrowLeft size={18} />
          В каталог
        </Link>
      </div>
    )
  }

  const incrementQty = () => setQuantity((q) => Math.min(q + 1, 99))
  const decrementQty = () => setQuantity((q) => Math.max(q - 1, 1))

  const handleAddToCart = () => {
    addToCart(product, quantity)
    logAction('cart', 'add_item', String(product.id))
  }

  return (
    <div className="max-w-6xl mx-auto py-8 lg:py-12">
      <Link
        to="/catalog"
        className="inline-flex items-center gap-2 text-black/80 hover:text-black font-unbounded text-sm mb-6 transition-colors"
      >
        <ArrowLeft size={18} />
        Назад в каталог
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-start">
        {/* Изображение */}
        <div className="bg-gray-900 border border-gray-700 rounded-2xl overflow-hidden aspect-square max-h-[500px] lg:max-h-none">
          <img
            src={product.image || '/placeholder-product.jpg'}
            alt={product.name}
            className="w-full h-full object-cover"
            onError={(e) => {
              const target = e.target as HTMLImageElement
              target.src = '/placeholder-product.jpg'
            }}
          />
        </div>

        {/* Инфо */}
        <div className="flex flex-col">
          <span className="text-sm font-unbounded text-black/70 uppercase tracking-wider mb-2">
            {product.category}
          </span>
          <h1 className="text-3xl lg:text-4xl font-bold font-unbounded text-black mb-4">
            {product.name}
          </h1>

          <div className="flex items-baseline gap-3 mb-6">
            <span className="text-3xl font-bold font-unbounded text-black">
              {product.price} ₽
            </span>
            {product.inStock ? (
              <span className="inline-flex items-center gap-1.5 text-sm text-green-700 bg-green-100 px-2.5 py-1 rounded-xl font-medium">
                <Package size={14} />
                В наличии
              </span>
            ) : (
              <span className="text-sm text-red-600 font-medium">
                Нет в наличии
              </span>
            )}
          </div>

          <p className="text-black/80 leading-relaxed mb-8">
            {product.description}
          </p>

          <div className="flex flex-wrap items-center gap-4 mb-8">
            <div className="flex items-center border-2 border-black rounded-2xl overflow-hidden">
              <button
                type="button"
                onClick={decrementQty}
                className="p-3 hover:bg-black/5 transition-colors disabled:opacity-50"
                aria-label="Уменьшить"
              >
                <Minus size={20} />
              </button>
              <span className="w-12 text-center font-unbounded font-semibold text-lg">
                {quantity}
              </span>
              <button
                type="button"
                onClick={incrementQty}
                className="p-3 hover:bg-black/5 transition-colors disabled:opacity-50"
                aria-label="Увеличить"
              >
                <Plus size={20} />
              </button>
            </div>
            <button
              type="button"
              onClick={handleAddToCart}
              disabled={!product.inStock}
              className="flex items-center gap-2 font-unbounded font-semibold bg-black text-white rounded-2xl px-6 py-3.5 hover:bg-black/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <ShoppingCart size={20} />
              В корзину
            </button>
          </div>

          <p className="text-sm text-black/60">
            Доставка по всей России. Оплата при получении или онлайн.
          </p>
        </div>
      </div>
    </div>
  )
}

export default ProductPage
