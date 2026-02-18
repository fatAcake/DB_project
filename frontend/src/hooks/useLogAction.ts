import { useCallback } from 'react'
import { useAuthStore } from '@/store/useAuthStore'
import { useCreateLog } from '@/api/logs'

/**
 * Хук для записи действия пользователя в таблицу logs.
 * Вызывается только для авторизованных пользователей (user_id обязателен на бэкенде).
 */
export const useLogAction = () => {
  const user = useAuthStore((s) => s.user)
  const createLog = useCreateLog()

  const logAction = useCallback(
    (system: string, action: string, response: string) => {
      if (!user) return
      createLog.mutate({
        user_id: user.id,
        system,
        action,
        response,
      })
    },
    [user?.id, createLog.mutate]
  )

  return { logAction }
}
