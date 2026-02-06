const ContactPage = () => {
  return (
    <div className="min-h-screen py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold mb-8 font-unbounded">Контакты</h1>
        <div className="max-w-3xl space-y-6">
          <div className="bg-white/10 rounded-2xl p-6 border border-white">
            <h2 className="text-2xl font-semibold mb-4 font-unbounded">Свяжитесь с нами</h2>
            <div className="space-y-4">
              <p className="text-lg">
                <strong>Email:</strong> info@antistress-shop.ru
              </p>
              <p className="text-lg">
                <strong>Телефон:</strong> +7 (XXX) XXX-XX-XX
              </p>
              <p className="text-lg">
                <strong>Адрес:</strong> г. Москва, ул. Примерная, д. 1
              </p>
              <p className="text-lg">
                <strong>Режим работы:</strong> Пн-Пт: 10:00 - 20:00, Сб-Вс: 11:00 - 18:00
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ContactPage
