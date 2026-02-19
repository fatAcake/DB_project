// Типы ответов бэкенда (соответствуют API)

export interface ApiProduct {
  id: number
  description: string
  price: number
  count?: number | string
}

export interface ApiFeedback {
  id: number
  message: string
  user_id: number
}

export interface ApiBlueprint {
  id: number
  name: string
  description?: string
}

export interface ApiUser {
  id: number
  first_name: string
  last_name: string
  father_name?: string
  email?: string
  is_acive: boolean
  role_id: number
  role_name?: string
  created_at: string
  updated_at?: string
}

export interface ApiProductImageInfo {
  id: string
  product_id_sql: number
  filename: string
  content_type: string
  created_at: string
  image_size?: number
}

export interface ApiQuantityProduct {
  id: number
  count: number
  product_id: number
}

export interface ApiTransaction {
  id: number
  sum: number
  user_id: number
  card_data: Record<string, unknown>
  created_at: string
  updated_at?: string
}
