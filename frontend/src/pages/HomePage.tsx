import ProductCarousel from '@/components/products/ProductCarousel'

const HomePage = () => {
  return (
    <div className="min-h-screen">
      <section className="py-16 lg:py-24">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto text-center mb-12">
            <h1 className="text-5xl lg:text-6xl font-bold font-unbounded">
              Антистресс игрушки
            </h1>
          </div>
          <ProductCarousel />
        </div>
      </section>
    </div>
  )
}

export default HomePage
