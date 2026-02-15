import { useEffect } from 'react'
import { useAuthStore } from '@/store/useAuthStore'
import { useMe } from '@/api/auth'

export const useAuth = () => {
  const { setUser, isAuthenticated, user } = useAuthStore()
  const { data, isLoading } = useMe()

  useEffect(() => {
    if (data) {
      setUser(data)
    }
  }, [data, setUser])

  return {
    user,
    isAuthenticated,
    isLoading,
  }
}
