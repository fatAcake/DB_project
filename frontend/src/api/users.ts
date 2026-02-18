import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import api from './axios'
import type { ApiUser } from '@/types/api'

/** Бэкенд ожидает first_name, last_name, father_name, email, role_id, опционально hash_password */
export interface RegisterInput {
  first_name: string
  last_name: string
  father_name?: string
  email: string
  hash_password?: string
  role_id: number
}

export const useRegisterUser = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (input: RegisterInput) => {
      const { data } = await api.post<ApiUser>('/users', input)
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })
}

export const useUsers = () => {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const { data } = await api.get<ApiUser[]>('/users')
      return data || []
    },
  })
}

export const useUser = (id: number | undefined) => {
  return useQuery({
    queryKey: ['user', id],
    queryFn: async () => {
      const { data } = await api.get<ApiUser>(`/users/${id}`)
      return data
    },
    enabled: !!id && id > 0,
  })
}
