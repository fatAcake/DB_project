import { useEffect } from 'react'
import { Outlet, useLocation } from 'react-router-dom'
import Header from './Header'
import Footer from './Footer'
import Sidebar from './Sidebar'
import FeedbackWidget from './FeedbackWidget'
import { useLogAction } from '@/hooks/useLogAction'

const Layout = () => {
  const location = useLocation()
  const { logAction } = useLogAction()

  useEffect(() => {
    logAction('frontend', 'view_page', location.pathname || '/')
  }, [location.pathname, logAction])

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-auto">
          <div className="container mx-auto px-4 py-6">
            <Outlet />
          </div>
        </main>
      </div>
      <Footer />
      <FeedbackWidget />
    </div>
  )
}

export default Layout
