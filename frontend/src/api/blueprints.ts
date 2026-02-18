import { useQuery } from '@tanstack/react-query'
import api from './axios'
import type { ApiBlueprint } from '@/types/api'

export const useBlueprints = () => {
  return useQuery({
    queryKey: ['blueprints'],
    queryFn: async () => {
      try {
        const { data } = await api.get<ApiBlueprint[]>('/blueprints')
        return data || []
      } catch (err: unknown) {
        if ((err as { response?: { status?: number } })?.response?.status === 404) {
          return []
        }
        throw err
      }
    },
  })
}

export const useBlueprint = (id: number | undefined) => {
  return useQuery({
    queryKey: ['blueprint', id],
    queryFn: async () => {
      const { data } = await api.get<ApiBlueprint>(`/blueprints/${id}`)
      return data
    },
    enabled: !!id && id > 0,
  })
}
