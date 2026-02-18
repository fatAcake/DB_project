import { create } from 'zustand'
import { CartItem } from '@/types'
import { getProductById } from '@/data/mockProducts'

interface CartState {
  items: CartItem[]
  addItem: (productId: number, quantity?: number) => void
  removeItem: (productId: number) => void
  updateQuantity: (productId: number, quantity: number) => void
  getItemCount: () => number
  getTotalPrice: () => number
}

const getInitialItems = (): CartItem[] => {
  const p1 = getProductById(1)
  const p2 = getProductById(2)
  const p4 = getProductById(4)
  if (!p1 || !p2 || !p4) return []
  return [
    { product: p1, quantity: 2 },
    { product: p2, quantity: 1 },
    { product: p4, quantity: 1 },
  ]
}

export const useCartStore = create<CartState>((set, get) => ({
  items: getInitialItems(),

  addItem: (productId, quantity = 1) => {
    const product = getProductById(productId)
    if (!product) return
    set((state) => {
      const existing = state.items.find((i) => i.product.id === productId)
      const next = existing
        ? state.items.map((i) =>
            i.product.id === productId
              ? { ...i, quantity: i.quantity + quantity }
              : i
          )
        : [...state.items, { product, quantity }]
      return { items: next }
    })
  },

  removeItem: (productId) => {
    set((state) => ({
      items: state.items.filter((i) => i.product.id !== productId),
    }))
  },

  updateQuantity: (productId, quantity) => {
    if (quantity < 1) {
      get().removeItem(productId)
      return
    }
    set((state) => ({
      items: state.items.map((i) =>
        i.product.id === productId ? { ...i, quantity } : i
      ),
    }))
  },

  getItemCount: () => get().items.reduce((sum, i) => sum + i.quantity, 0),

  getTotalPrice: () =>
    get().items.reduce((sum, i) => sum + i.product.price * i.quantity, 0),
}))
