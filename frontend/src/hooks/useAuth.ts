import { useAuthStore } from '@/store/useAuthStore'

/** Текущий пользователь и статус авторизации (из store; бэкенд не отдаёт /auth/me). */
export const useAuth = () => {
  const { isAuthenticated, user } = useAuthStore()
  return {
    user,
    isAuthenticated,
    isLoading: false,
  }
}
