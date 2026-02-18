import { Link, useNavigate } from 'react-router-dom'
import { Package, ArrowRight, Calendar } from 'lucide-react'
import { useAuthStore } from '@/store/useAuthStore'
import { useTransactionsByUserId } from '@/api/transactions'
import type { ApiTransaction } from '@/types/api'
import LoadingSpinner from '@/components/common/LoadingSpinner'
import ErrorMessage from '@/components/common/ErrorMessage'

const formatDate = (iso: string) => {
  const d = new Date(iso)
  return d.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const OrderCard = ({ order }: { order: ApiTransaction }) => (
  <div className="rounded-2xl border-2 border-black/10 bg-white/90 overflow-hidden">
    <div className="w-full flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-5 text-left">
      <span className="font-unbounded font-bold text-black">
        Заказ №{order.id}
      </span>
      <div className="flex items-center gap-4 sm:gap-6">
        <span className="flex items-center gap-1.5 text-black/70 text-sm">
          <Calendar size={16} />
          {formatDate(order.created_at)}
        </span>
        <span className="font-unbounded font-bold text-black">
          {order.sum.toLocaleString('ru-RU')} ₽
        </span>
      </div>
    </div>
  </div>
)

const ProfileOrdersPage = () => {
  const { user, isAuthenticated } = useAuthStore()
  const navigate = useNavigate()
  const { data: orders = [], isLoading, isError, error } = useTransactionsByUserId(user?.id)

  if (!isAuthenticated || !user) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-black/5 mb-6">
          <Package size={40} className="text-black/50" />
        </div>
        <h1 className="text-2xl font-unbounded font-bold text-black mb-2">
          Войдите в аккаунт
        </h1>
        <p className="text-black/70 mb-8">
          Чтобы просматривать историю заказов, авторизуйтесь.
        </p>
        <button
          type="button"
          onClick={() => navigate('/login')}
          className="inline-flex items-center gap-2 font-unbounded font-semibold bg-black text-white rounded-2xl px-6 py-3 hover:bg-black/90 transition-colors"
        >
          Войти
          <ArrowRight size={18} />
        </button>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="max-w-xl mx-auto py-16 flex justify-center">
        <LoadingSpinner />
      </div>
    )
  }
  if (isError) {
    return (
      <div className="max-w-xl mx-auto py-8">
        <ErrorMessage message={error instanceof Error ? error.message : 'Не удалось загрузить заказы'} />
      </div>
    )
  }

  if (orders.length === 0) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-black/5 mb-6">
          <Package size={40} className="text-black/50" />
        </div>
        <h1 className="text-2xl font-unbounded font-bold text-black mb-2">
          Пока нет заказов
        </h1>
        <p className="text-black/70 mb-8">
          Оформленные заказы появятся здесь.
        </p>
        <Link
          to="/catalog"
          className="inline-flex items-center gap-2 font-unbounded font-semibold bg-black text-white rounded-2xl px-6 py-3 hover:bg-black/90 transition-colors"
        >
          Перейти в каталог
          <ArrowRight size={18} />
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto py-8">
      <h1 className="text-3xl font-unbounded font-bold text-black mb-2">
        Мои заказы
      </h1>
      <p className="text-black/60 text-sm mb-8">
        История транзакций (оплат)
      </p>
      <div className="space-y-4">
        {orders.map((order) => (
          <OrderCard key={order.id} order={order} />
        ))}
      </div>
    </div>
  )
}

export default ProfileOrdersPage
