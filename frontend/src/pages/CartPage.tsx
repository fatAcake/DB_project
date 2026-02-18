import { Link } from 'react-router-dom'
import { ShoppingCart, Trash2, Minus, Plus, ArrowRight } from 'lucide-react'
import { useCartStore } from '@/store/useCartStore'
import { useLogAction } from '@/hooks/useLogAction'

const CartPage = () => {
  const { items, removeItem, updateQuantity, getTotalPrice } = useCartStore()
  const { logAction } = useLogAction()
  const total = getTotalPrice()

  if (items.length === 0) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-black/5 mb-6">
          <ShoppingCart size={40} className="text-black/50" />
        </div>
        <h1 className="text-2xl font-unbounded font-bold text-black mb-2">
          Корзина пуста
        </h1>
        <p className="text-black/70 mb-8">
          Добавьте товары из каталога, чтобы оформить заказ.
        </p>
        <Link
          to="/catalog"
          className="inline-flex items-center gap-2 font-unbounded font-semibold bg-black text-white rounded-2xl px-6 py-3 hover:bg-black/90 transition-colors"
        >
          Перейти в каталог
          <ArrowRight size={18} />
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto py-8">
      <h1 className="text-3xl font-bold font-unbounded text-black mb-8">
        Корзина
      </h1>

      <div className="space-y-4 mb-8">
        {items.map(({ product, quantity }) => (
          <div
            key={product.id}
            className="flex flex-col sm:flex-row gap-4 p-4 bg-white/80 dark:bg-gray-900/50 border border-black/10 rounded-2xl"
          >
            <Link
              to={`/product/${product.id}`}
              className="flex-shrink-0 w-full sm:w-24 h-24 rounded-xl overflow-hidden bg-gray-200"
            >
              <img
                src={product.image || '/placeholder-product.jpg'}
                alt={product.name}
                className="w-full h-full object-cover"
                onError={(e) => {
                  const target = e.target as HTMLImageElement
                  target.src = '/placeholder-product.jpg'
                }}
              />
            </Link>
            <div className="flex-1 min-w-0">
              <Link
                to={`/product/${product.id}`}
                className="font-unbounded font-semibold text-black hover:underline line-clamp-2"
              >
                {product.name}
              </Link>
              <p className="text-black/70 text-sm mt-0.5">{product.category}</p>
              <p className="font-unbounded font-bold text-black mt-1">
                {product.price} ₽
              </p>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex items-center border-2 border-black/20 rounded-xl overflow-hidden">
                <button
                  type="button"
                  onClick={() => {
                    updateQuantity(product.id, quantity - 1)
                    logAction('cart', 'update_quantity', `${product.id}:${quantity - 1}`)
                  }}
                  className="p-2 hover:bg-black/5 transition-colors"
                  aria-label="Уменьшить"
                >
                  <Minus size={18} />
                </button>
                <span className="w-8 text-center font-unbounded font-semibold text-sm">
                  {quantity}
                </span>
                <button
                  type="button"
                  onClick={() => {
                    updateQuantity(product.id, quantity + 1)
                    logAction('cart', 'update_quantity', `${product.id}:${quantity + 1}`)
                  }}
                  className="p-2 hover:bg-black/5 transition-colors"
                  aria-label="Увеличить"
                >
                  <Plus size={18} />
                </button>
              </div>
              <span className="font-unbounded font-bold text-black min-w-[4rem] text-right">
                {product.price * quantity} ₽
              </span>
              <button
                type="button"
                onClick={() => {
                  logAction('cart', 'remove_item', String(product.id))
                  removeItem(product.id)
                }}
                className="p-2 text-red-600 hover:bg-red-50 rounded-xl transition-colors"
                aria-label="Удалить"
              >
                <Trash2 size={18} />
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6 p-6 bg-black text-white rounded-2xl">
        <div>
          <p className="text-white/80 text-sm font-unbounded uppercase tracking-wider">
            Итого
          </p>
          <p className="text-3xl font-bold font-unbounded">{total} ₽</p>
        </div>
        <button
          type="button"
          className="font-unbounded font-semibold bg-white text-black rounded-2xl px-8 py-3.5 hover:bg-white/90 transition-colors inline-flex items-center justify-center gap-2"
        >
          Оформить заказ
          <ArrowRight size={20} />
        </button>
      </div>

      <p className="text-center text-black/60 text-sm mt-6">
        <Link to="/catalog" className="hover:underline">
          Продолжить покупки
        </Link>
      </p>
    </div>
  )
}

export default CartPage
