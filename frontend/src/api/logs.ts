import { useMutation } from '@tanstack/react-query'
import api from './axios'

export interface CreateLogInput {
  user_id: number
  system: string
  action: string
  response: string
  lead_time?: string
}

/** Отправка записи в таблицу логов (поля: user_id, system, action, response, lead_time опционально) */
export const useCreateLog = () => {
  return useMutation({
    mutationFn: async (input: CreateLogInput) => {
      const body: Record<string, unknown> = {
        user_id: input.user_id,
        system: input.system,
        action: input.action,
        response: input.response,
      }
      if (input.lead_time) body.lead_time = input.lead_time
      const { data } = await api.post('/logs', body)
      return data
    },
  })
}
