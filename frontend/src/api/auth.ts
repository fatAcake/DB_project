import { useMutation, useQuery } from '@tanstack/react-query'
import api from './axios'

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

export const useLogin = () => {
  return useMutation({
    mutationFn: async (credentials: LoginCredentials) => {
      const { data } = await api.post('/auth/login', credentials)
      return data
    },
    onSuccess: (data) => {
      if (data.token) {
        localStorage.setItem('token', data.token)
      }
    },
  })
}

export const useRegister = () => {
  return useMutation({
    mutationFn: async (registerData: RegisterData) => {
      const { data } = await api.post('/auth/register', registerData)
      return data
    },
  })
}

export const useMe = () => {
  return useQuery({
    queryKey: ['me'],
    queryFn: async () => {
      const { data } = await api.get<User>('/auth/me')
      return data
    },
  })
}
