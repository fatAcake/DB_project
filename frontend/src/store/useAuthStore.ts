import { create } from 'zustand'

interface AuthState {
  isAuthenticated: boolean
  user: null | { id: number; email: string; name: string; role?: 'user' | 'admin' }
  setUser: (user: { id: number; email: string; name: string; role?: 'user' | 'admin' } | null) => void
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
