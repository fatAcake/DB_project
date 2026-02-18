import { Link, useNavigate } from 'react-router-dom'
import { Package, ArrowRight, ChevronDown, ChevronUp, Calendar, Receipt } from 'lucide-react'
import { useAuthStore } from '@/store/useAuthStore'
import { getOrdersByUserId, getOrderStatusLabel } from '@/data/mockOrders'
import type { Order } from '@/types'
import { useState } from 'react'

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

const statusColors: Record<Order['status'], string> = {
  pending: 'bg-amber-100 text-amber-800 border-amber-200',
  processing: 'bg-blue-100 text-blue-800 border-blue-200',
  shipped: 'bg-violet-100 text-violet-800 border-violet-200',
  delivered: 'bg-emerald-100 text-emerald-800 border-emerald-200',
}

const OrderCard = ({ order }: { order: Order }) => {
  const [expanded, setExpanded] = useState(false)
  return (
    <div className="rounded-2xl border-2 border-black/10 bg-white/90 overflow-hidden">
      <button
        type="button"
        onClick={() => setExpanded((e) => !e)}
        className="w-full flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-5 text-left hover:bg-black/[0.03] transition-colors"
      >
        <div className="flex flex-wrap items-center gap-3">
          <span className="font-unbounded font-bold text-black">
            Заказ №{order.id}
          </span>
          <span
            className={`inline-flex items-center px-2.5 py-1 rounded-lg border text-xs font-semibold ${statusColors[order.status]}`}
          >
            {getOrderStatusLabel(order.status)}
          </span>
        </div>
        <div className="flex items-center gap-4 sm:gap-6">
          <span className="flex items-center gap-1.5 text-black/70 text-sm">
            <Calendar size={16} />
            {formatDate(order.createdAt)}
          </span>
          <span className="font-unbounded font-bold text-black">
            {order.total.toLocaleString('ru-RU')} ₽
          </span>
          <span className="text-black/50">
            {expanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
          </span>
        </div>
      </button>
      {expanded && (
        <div className="border-t border-black/10 bg-black/[0.02] p-5">
          <div className="flex items-center gap-2 mb-3">
            <Receipt size={18} className="text-black/50" />
            <span className="text-sm font-semibold text-black/70">Товары в заказе</span>
          </div>
          <ul className="space-y-3">
            {order.items.map(({ product, quantity }) => (
              <li
                key={product.id}
                className="flex items-center gap-4 p-3 rounded-xl bg-white border border-black/5"
              >
                <Link
                  to={`/product/${product.id}`}
                  className="flex-shrink-0 w-14 h-14 rounded-lg overflow-hidden bg-black/5"
                >
                  <img
                    src={product.image}
                    alt={product.name}
                    className="w-full h-full object-cover"
                  />
                </Link>
                <div className="flex-1 min-w-0">
                  <Link
                    to={`/product/${product.id}`}
                    className="font-unbounded font-semibold text-black hover:underline line-clamp-1"
                  >
                    {product.name}
                  </Link>
                  <p className="text-black/60 text-sm">
                    {quantity} × {product.price.toLocaleString('ru-RU')} ₽
                  </p>
                </div>
                <span className="font-unbounded font-bold text-black">
                  {(product.price * quantity).toLocaleString('ru-RU')} ₽
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

const ProfileOrdersPage = () => {
  const { user, isAuthenticated } = useAuthStore()
  const navigate = useNavigate()
  const orders = isAuthenticated && user ? getOrdersByUserId(user.id) : []

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
        Нажмите на заказ, чтобы увидеть состав
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
