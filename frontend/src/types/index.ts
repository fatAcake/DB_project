// Общие типы для приложения

export interface Product {
  id: number
  name: string
  price: number
  description: string
  image: string
  images?: string[]
  category: string
  inStock: boolean
  quantity?: number
}

export interface User {
  id: number
  email: string
  name: string
  role?: 'user' | 'admin'
}

export interface CartItem {
  product: Product
  quantity: number
}

export interface Order {
  id: number
  userId: number
  items: CartItem[]
  total: number
  status: 'pending' | 'processing' | 'shipped' | 'delivered'
  createdAt: string
}
