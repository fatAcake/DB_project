const WorkshopPage = () => {
  return (
    <div className="min-h-screen py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold mb-8 font-unbounded">Мастерская</h1>
        <p className="text-lg mb-6">
          Добро пожаловать в нашу мастерскую! Здесь вы найдете чертежи и модели для 3D печати антистресс игрушек.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Здесь будут карточки с чертежами */}
          <div className="bg-white/10 rounded-2xl p-6 border border-white">
            <h2 className="text-xl font-semibold mb-4 font-unbounded">Чертежи скоро появятся</h2>
            <p className="text-gray-300">
              Мы работаем над добавлением чертежей для 3D печати. Скоро здесь будут доступны модели наших антистресс игрушек.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default WorkshopPage
