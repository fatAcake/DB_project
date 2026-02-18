import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import api from './axios'
import type { ApiFeedback } from '@/types/api'

export interface CreateFeedbackInput {
  message: string
  user_id: number
}

export const useCreateFeedback = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (input: CreateFeedbackInput) => {
      const { data } = await api.post<ApiFeedback>('/feedback', input)
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['feedback'] })
    },
  })
}

export const useFeedbacks = () => {
  return useQuery({
    queryKey: ['feedback'],
    queryFn: async () => {
      const { data } = await api.get<ApiFeedback[]>('/feedback')
      return data || []
    },
  })
}
