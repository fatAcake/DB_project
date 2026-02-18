import { useQuery } from '@tanstack/react-query'
import api from './axios'
import type { ApiProduct } from '@/types/api'
import { apiProductToProduct } from './mappers'

export const useProducts = () => {
  return useQuery({
    queryKey: ['products'],
    queryFn: async () => {
      const { data } = await api.get<ApiProduct[]>('/products')
      return (data || []).map((p) => apiProductToProduct(p))
    },
  })
}

export const useProduct = (id: number | undefined) => {
  return useQuery({
    queryKey: ['product', id],
    queryFn: async () => {
      const { data } = await api.get<ApiProduct>(`/products/${id}`)
      return apiProductToProduct(data)
    },
    enabled: !!id && id > 0,
  })
}
