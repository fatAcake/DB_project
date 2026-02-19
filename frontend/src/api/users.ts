import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import api from './axios'
import type { ApiUser } from '@/types/api'
import type { AuthUser } from '@/store/useAuthStore'

/** Бэкенд ожидает first_name, last_name, father_name, email, role_id, опционально hash_password */
export interface RegisterInput {
  first_name: string
  last_name: string
  father_name?: string
  email: string
  hash_password?: string
  role_id: number
}

/** Преобразует пользователя API в формат авторизации фронта. Роль по role_name (если есть) или по role_id. */
export function apiUserToAuthUser(u: ApiUser): AuthUser {
  const role =
    u.role_name === 'admin'
      ? 'admin'
      : u.role_name === 'seller'
        ? 'seller'
        : u.role_name === 'buyer'
          ? 'buyer'
          : u.role_id === 1
            ? 'buyer'
            : u.role_id === 2
              ? 'seller'
              : 'admin'
  return {
    id: u.id,
    email: u.email ?? '',
    name: [u.first_name, u.last_name].filter(Boolean).join(' '),
    surname: u.last_name,
    patronymic: u.father_name,
    role,
  }
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

/** Верификация пользователя по коду (бэкенд: GET /users/{id}/verification) */
export const useVerifyUser = () => {
  return useMutation({
    mutationFn: async ({ userId, code }: { userId: number; code: string }) => {
      await api.get(`/users/${userId}/verification`, {
        params: { verification_code: code },
      })
    },
  })
}

/** Запрос на отправку кода смены пароля на email (бэкенд: POST /users/{id}/password/send-code) */
export interface SendPasswordCodeInput {
  current_password?: string
}

export const useSendPasswordCode = () => {
  return useMutation({
    mutationFn: async ({
      userId,
      current_password,
    }: { userId: number } & SendPasswordCodeInput) => {
      await api.post(`/users/${userId}/password/send-code`, {
        current_password: current_password || undefined,
      })
    },
  })
}

/** Смена пароля по коду из письма (бэкенд: POST /users/{id}/password/change) */
export interface ChangePasswordInput {
  code: number
  new_password: string
}

export const useChangePassword = () => {
  return useMutation({
    mutationFn: async ({
      userId,
      code,
      new_password,
    }: { userId: number } & ChangePasswordInput) => {
      await api.post(`/users/${userId}/password/change`, { code, new_password })
    },
  })
}
