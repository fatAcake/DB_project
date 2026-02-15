import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { ShoppingCart, Grid3X3, LayoutGrid } from 'lucide-react'
import { useProducts } from '@/api/products'
import { useCartStore } from '@/store/useCartStore'
import { Product } from '@/types'
import { cn } from '@/utils/cn'
import LoadingSpinner from '@/components/common/LoadingSpinner'
import ErrorMessage from '@/components/common/ErrorMessage'

const CATEGORY_ALL = 'Все'

const ProductCard = ({
  product,
  onAddToCart,
}: {
  product: Product
  onAddToCart: (e: React.MouseEvent) => void
}) => (
  <article className="group flex flex-col">
    <Link
      to={`/product/${product.id}`}
      className="block bg-gray-900 border border-gray-700 rounded-2xl overflow-hidden hover:bg-gray-800 hover:border-gray-600 transition-all duration-300 group/card"
    >
      <div className="aspect-square relative overflow-hidden bg-gray-800">
        <img
          src={product.image || '/placeholder-product.jpg'}
          alt={product.name}
          className="w-full h-full object-cover group-hover/card:scale-105 transition-transform duration-500"
          onError={(e) => {
            const target = e.target as HTMLImageElement
            target.src = '/placeholder-product.jpg'
          }}
        />
        <span className="absolute top-3 left-3 text-[10px] font-unbounded font-semibold uppercase tracking-wider bg-black/70 text-white px-2.5 py-1 rounded-lg">
          {product.category}
        </span>
      </div>
    </Link>
    <div className="mt-4 flex flex-col gap-2">
      <Link
        to={`/product/${product.id}`}
        className="font-unbounded font-semibold text-lg text-black hover:underline line-clamp-2"
      >
        {product.name}
      </Link>
      <div className="flex items-center justify-between gap-3">
        <span className="font-unbounded font-bold text-xl text-black">
          {product.price} ₽
        </span>
        <button
          type="button"
          onClick={onAddToCart}
          className="flex items-center gap-2 font-unbounded text-sm font-semibold bg-black text-white rounded-xl px-4 py-2.5 hover:bg-black/90 active:scale-[0.98] transition-all"
        >
          <ShoppingCart size={16} />
          В корзину
        </button>
      </div>
    </div>
  </article>
)

const CatalogPage = () => {
  const [category, setCategory] = useState(CATEGORY_ALL)
  const [viewMode, setViewMode] = useState<'grid' | 'compact'>('grid')
  const addToCart = useCartStore((s) => s.addItem)
  const { data: products = [], isLoading, isError, error } = useProducts()

  const categories = useMemo(
    () => [CATEGORY_ALL, ...Array.from(new Set(products.map((p) => p.category)))],
    [products]
  )

  const filteredProducts = useMemo(() => {
    if (category === CATEGORY_ALL) return products
    return products.filter((p) => p.category === category)
  }, [category, products])

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto flex justify-center py-20">
        <LoadingSpinner />
      </div>
    )
  }

  if (isError) {
    return (
      <div className="max-w-7xl mx-auto py-12">
        <ErrorMessage message={(error as Error)?.message || 'Не удалось загрузить каталог'} />
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Заголовок */}
      <header className="text-center mb-10 lg:mb-14">
        <h1 className="text-4xl lg:text-5xl font-bold font-unbounded text-black mb-3">
          Каталог
        </h1>
        <p className="text-black/70 max-w-xl mx-auto font-medium">
          Антистресс-игрушки и фиджеты для снятия напряжения и концентрации
        </p>
      </header>

      {/* Фильтр по категориям + вид сетки */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div className="flex flex-wrap gap-2">
          {categories.map((cat) => (
            <button
              key={cat}
              type="button"
              onClick={() => setCategory(cat)}
              className={cn(
                'font-unbounded text-sm font-semibold rounded-2xl px-4 py-2 transition-all',
                category === cat
                  ? 'bg-black text-white'
                  : 'bg-black/5 text-black hover:bg-black/10'
              )}
            >
              {cat}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-1 border border-black/20 rounded-2xl p-1 w-fit">
          <button
            type="button"
            onClick={() => setViewMode('grid')}
            className={cn(
              'p-2 rounded-xl transition-colors',
              viewMode === 'grid' ? 'bg-black text-white' : 'text-black/70 hover:bg-black/5'
            )}
            aria-label="Сетка"
          >
            <LayoutGrid size={20} />
          </button>
          <button
            type="button"
            onClick={() => setViewMode('compact')}
            className={cn(
              'p-2 rounded-xl transition-colors',
              viewMode === 'compact' ? 'bg-black text-white' : 'text-black/70 hover:bg-black/5'
            )}
            aria-label="Компактный вид"
          >
            <Grid3X3 size={20} />
          </button>
        </div>
      </div>

      {/* Сетка товаров */}
      <div
        className={cn(
          'gap-6 lg:gap-8',
          viewMode === 'grid'
            ? 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'
            : 'grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4'
        )}
      >
        {filteredProducts.map((product) => (
          <ProductCard
            key={product.id}
            product={product}
            onAddToCart={(e) => {
              e.preventDefault()
              addToCart(product, 1)
            }}
          />
        ))}
      </div>

      {filteredProducts.length === 0 && (
        <div className="text-center py-16">
          <p className="text-black/70 font-unbounded">
            В этой категории пока нет товаров.
          </p>
        </div>
      )}
    </div>
  )
}

export default CatalogPage
