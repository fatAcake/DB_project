import { useQuery } from '@tanstack/react-query'
import api from './axios'
import { Product } from '@/types'

export const useProducts = () => {
  return useQuery({
    queryKey: ['products'],
    queryFn: async () => {
      const { data } = await api.get<Product[]>('/products')
      return data
    },
  })
}

export const useProduct = (id: number) => {
  return useQuery({
    queryKey: ['product', id],
    queryFn: async () => {
      const { data } = await api.get<Product>(`/products/${id}`)
      return data
    },
    enabled: !!id,
  })
}
