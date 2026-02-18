import { useQuery } from '@tanstack/react-query'
import api from './axios'
import type { ApiTransaction } from '@/types/api'

export const useTransactions = () => {
  return useQuery({
    queryKey: ['transactions'],
    queryFn: async () => {
      const { data } = await api.get<ApiTransaction[]>('/transactions')
      return data || []
    },
  })
}

export const useTransactionsByUserId = (userId: number | undefined) => {
  const query = useTransactions()
  const transactions =
    query.data && userId
      ? query.data.filter((t) => t.user_id === userId)
      : []
  return {
    ...query,
    data: transactions.sort(
      (a, b) =>
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    ),
  }
}
