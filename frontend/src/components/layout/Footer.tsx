import { Mail, Phone, MapPin } from 'lucide-react'

const Footer = () => {
  return (
    <footer className="bg-black text-white py-12 border-t border-gray-800">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Контактная информация */}
          <div>
            <h3 className="text-xl font-bold font-unbounded mb-4">Контакты</h3>
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <Phone className="w-5 h-5 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-gray-300">Телефон</p>
                  <a href="tel:+79991234567" className="text-white hover:text-gray-300 transition-colors">
                    +7 (999) 123-45-67
                  </a>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <Mail className="w-5 h-5 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-gray-300">Email</p>
                  <a href="mailto:info@antistress-toys.ru" className="text-white hover:text-gray-300 transition-colors">
                    info@antistress-toys.ru
                  </a>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <MapPin className="w-5 h-5 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-gray-300">Адрес</p>
                  <p className="text-white">г. Новосибирск. ул Советская 64/1</p>
                </div>
              </div>
            </div>
          </div>

          {/* О компании */}
          <div>
            <h3 className="text-xl font-bold font-unbounded mb-4">О нас</h3>
            <p className="text-gray-300 leading-relaxed">
              Магазин антистресс игрушек, напечатанных на 3D принтере. 
              Мы создаем уникальные изделия для снятия напряжения и релаксации.
            </p>
          </div>

          {/* Часы работы */}
          <div>
            <h3 className="text-xl font-bold font-unbounded mb-4">Режим работы</h3>
            <div className="space-y-2 text-gray-300">
              <p>Понедельник - Пятница: 10:00 - 20:00</p>
              <p>Суббота: 11:00 - 19:00</p>
              <p>Воскресенье: 12:00 - 18:00</p>
            </div>
          </div>
        </div>

        {/* Копирайт */}
        <div className="mt-8 pt-8 border-t border-gray-800 text-center text-gray-400">
          <p>&copy; {new Date().getFullYear()} Антистресс игрушки. Все права защищены.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
