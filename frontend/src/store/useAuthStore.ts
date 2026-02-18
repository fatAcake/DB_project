import { create } from 'zustand'

export type UserRole = 'buyer' | 'seller' | 'admin'

export interface AuthUser {
  id: number
  email: string
  name: string
  surname?: string
  patronymic?: string
  role?: UserRole
}

interface AuthState {
  isAuthenticated: boolean
  user: AuthUser | null
  setUser: (user: AuthUser | null) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  isAuthenticated: false,
  user: null,
  setUser: (user) => set({ user, isAuthenticated: !!user }),
  logout: () => {
    localStorage.removeItem('token')
    set({ user: null, isAuthenticated: false })
  },
}))
