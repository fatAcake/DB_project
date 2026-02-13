import { Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import BackgroundAnimation from './components/layout/BackgroundAnimation'
import HomePage from './pages/HomePage'
import CatalogPage from './pages/CatalogPage'
import ProductPage from './pages/ProductPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import ProfilePage from './pages/ProfilePage'
import AdminPage from './pages/AdminPage'
import WorkshopPage from './pages/WorkshopPage'
import AboutPage from './pages/AboutPage'
import ContactPage from './pages/ContactPage'
import CartPage from './pages/CartPage'
import NotFoundPage from './pages/NotFoundPage'

function App() {
  return (
    <>
      {/* Фон рендерится здесь, чтобы fixed всегда был относительно viewport (не внутри Layout/Router) */}
      <div
        className="fixed inset-0 z-0 w-full h-full min-h-screen"
        style={{ isolation: 'isolate' }}
        aria-hidden
      >
        <BackgroundAnimation />
      </div>
      <div className="relative z-10 min-h-screen">
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/" element={<Layout />}>
            <Route index element={<HomePage />} />
            <Route path="catalog" element={<CatalogPage />} />
            <Route path="product/:id" element={<ProductPage />} />
            <Route path="workshop" element={<WorkshopPage />} />
            <Route path="about" element={<AboutPage />} />
            <Route path="contact" element={<ContactPage />} />
            <Route path="cart" element={<CartPage />} />
            <Route path="profile" element={<ProfilePage />} />
            <Route path="admin/*" element={<AdminPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </div>
    </>
  )
}

export default App
