/**
 * Авторизация. На бэкенде нет отдельного /auth — регистрация через POST /users.
 * Токен и user_id храним в localStorage для совместимости с текущим UI.
 */
import { useMutation, useQuery } from '@tanstack/react-query'
import api from './axios'
import type { ApiUser } from '@/types/api'

const USER_ID_KEY = 'user_id'
const TOKEN_KEY = 'token'

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  name: string
}

export interface User {
  id: number
  email: string
  name: string
}

function apiUserToUser(u: ApiUser): User {
  return {
    id: u.id,
    email: u.email ?? '',
    name: ([u.first_name, u.last_name].filter(Boolean).join(' ') || u.email) ?? 'Пользователь',
  }
}

/** Регистрация через POST /users (first_name, last_name, email, role_id=1) */
export const useRegister = () => {
  return useMutation({
    mutationFn: async (data: RegisterData) => {
      const namePart = data.name.trim() || 'Пользователь'
      const { data: user } = await api.post<ApiUser>('/users', {
        first_name: namePart,
        last_name: '—',
        father_name: '',
        email: data.email,
        hash_password: data.password,
        role_id: 1,
      })
      return apiUserToUser(user)
    },
    onSuccess: (user) => {
      localStorage.setItem(USER_ID_KEY, String(user.id))
      localStorage.setItem(TOKEN_KEY, 'registered')
    },
  })
}

/** Вход: бэкенд не отдаёт отдельный login — проверяем только наличие пользователя по email */
export const useLogin = () => {
  return useMutation({
    mutationFn: async (credentials: LoginCredentials) => {
      const { data: list } = await api.get<ApiUser[]>('/users')
      const user = (list || []).find((u) => u.email === credentials.email)
      if (!user) throw new Error('Пользователь не найден')
      return apiUserToUser(user)
    },
    onSuccess: (user) => {
      localStorage.setItem(USER_ID_KEY, String(user.id))
      localStorage.setItem(TOKEN_KEY, 'logged')
    },
  })
}

export const useMe = () => {
  const userId = typeof window !== 'undefined' ? localStorage.getItem(USER_ID_KEY) : null
  return useQuery({
    queryKey: ['me', userId],
    queryFn: async () => {
      const { data } = await api.get<ApiUser>(`/users/${userId}`)
      return apiUserToUser(data)
    },
    enabled: !!userId,
  })
}

export function getStoredUserId(): number | null {
  const id = localStorage.getItem(USER_ID_KEY)
  return id ? parseInt(id, 10) : null
}

export function logout() {
  localStorage.removeItem(USER_ID_KEY)
  localStorage.removeItem(TOKEN_KEY)
}
