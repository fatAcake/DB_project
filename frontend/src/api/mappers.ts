import type { Product } from '@/types'
import type { ApiProduct } from '@/types/api'

const PLACEHOLDER_IMAGE = '/placeholder-product.jpg'

/**
 * Преобразует продукт из API в формат фронтенда.
 * Изображение подставляется через imageUrl, если передан (например из /files_products).
 */
function toNumber(v: unknown): number {
  if (v == null) return 0
  if (typeof v === 'number' && !Number.isNaN(v)) return v
  const n = Number(v)
  return Number.isNaN(n) ? 0 : n
}

export function apiProductToProduct(
  p: ApiProduct,
  imageUrl: string | null = null
): Product {
  const name = p.description.length > 60 ? p.description.slice(0, 57) + '...' : p.description
  const count = toNumber(p.count)
  return {
    id: p.id,
    name,
    price: Number(p.price),
    description: p.description,
    image: imageUrl || PLACEHOLDER_IMAGE,
    category: 'Товар',
    inStock: count > 0,
    quantity: count,
  }
}
