import type { CartItem, Order } from '@/types'
import { getProductById } from '@/data/mockProducts'

const item = (id: number, qty: number): CartItem | null => {
  const p = getProductById(id)
  return p ? { product: p, quantity: qty } : null
}

const items = (...entries: [number, number][]): CartItem[] =>
  entries.map(([id, qty]) => item(id, qty)).filter((x): x is CartItem => x != null)

/** Моковые заказы текущего пользователя (userId = 1) */
export const mockOrders: Order[] = [
  {
    id: 1001,
    userId: 1,
    items: items([1, 2], [4, 1]),
    total: 599 * 2 + 699,
    status: 'delivered',
    createdAt: '2025-01-15T10:30:00Z',
  },
  {
    id: 1002,
    userId: 1,
    items: items([2, 1], [3, 3]),
    total: 799 + 499 * 3,
    status: 'shipped',
    createdAt: '2025-02-01T14:00:00Z',
  },
  {
    id: 1003,
    userId: 1,
    items: items([5, 1], [6, 2]),
    total: 899 + 549 * 2,
    status: 'processing',
    createdAt: '2025-02-10T09:15:00Z',
  },
  {
    id: 1004,
    userId: 1,
    items: items([8, 1]),
    total: 749,
    status: 'pending',
    createdAt: '2025-02-12T16:45:00Z',
  },
]

const statusLabels: Record<Order['status'], string> = {
  pending: 'Ожидает обработки',
  processing: 'В обработке',
  shipped: 'Отправлен',
  delivered: 'Доставлен',
}

export const getOrderStatusLabel = (status: Order['status']) => statusLabels[status]

export const getOrdersByUserId = (userId: number): Order[] =>
  mockOrders.filter((o) => o.userId === userId).sort(
    (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  )
