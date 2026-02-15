import { useQuery } from '@tanstack/react-query'
import api from './axios'
import type { Product } from '@/types'
import type { ApiProduct } from '@/types/api'
import { apiProductToProduct } from './mappers'

export const getProductImageUrl = (imageId: string) => `/api/files_products/${imageId}`

export const useProducts = () => {
  return useQuery({
    queryKey: ['products'],
    queryFn: async () => {
      try {
        const { data } = await api.get<ApiProduct[]>('/products')
        return (data || []).map((p) => apiProductToProduct(p))
      } catch (err: unknown) {
        if ((err as { response?: { status?: number } })?.response?.status === 404) {
          return []
        }
        throw err
      }
    },
  })
}

export const useProduct = (id: number | undefined) => {
  return useQuery({
    queryKey: ['product', id],
    queryFn: async (): Promise<Product> => {
      const { data } = await api.get<ApiProduct>(`/products/${id}`)
      return apiProductToProduct(data)
    },
    enabled: !!id && id > 0,
  })
}

/** Количество на складе по product_id */
export const useProductQuantity = (productId: number | undefined) => {
  return useQuery({
    queryKey: ['quantity_products', productId],
    queryFn: async () => {
      const { data } = await api.get<{ count: number }>(`/quantity_products/products/${productId}`)
      return data?.count ?? 0
    },
    enabled: !!productId && productId > 0,
  })
}

/** Список id изображений продукта (для подстановки первого в карточку) */
export const useProductImageIds = (productId: number | undefined) => {
  return useQuery({
    queryKey: ['files_products', productId],
    queryFn: async () => {
      const { data } = await api.get<{ id?: string; _id?: string }[]>(
        `/files_products/${productId}/images`
      )
      return (data || []).map((i) => i.id ?? i._id ?? '').filter(Boolean)
    },
    enabled: !!productId && productId > 0,
  })
}
