import { useState } from 'react'
import { MessageCircle, Send, X } from 'lucide-react'

const FeedbackWidget = () => {
  const [open, setOpen] = useState(false)
  const [sent, setSent] = useState(false)
  const [message, setMessage] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setSent(true)
    setMessage('')
    setTimeout(() => {
      setSent(false)
      setOpen(false)
    }, 2000)
  }

  return (
    <div className="fixed bottom-6 right-6 z-40 flex flex-col items-end gap-3">
      {open && (
        <div className="w-[320px] sm:w-[360px] rounded-2xl border-2 border-black/15 bg-white shadow-xl overflow-hidden">
          {sent ? (
            <div className="p-6 text-center">
              <p className="font-unbounded font-semibold text-black">
                Спасибо! Мы ответим вам скоро.
              </p>
            </div>
          ) : (
            <>
              <div className="flex items-center justify-between px-4 py-3 bg-black text-white">
                <span className="font-unbounded font-semibold text-sm">
                  Обратная связь
                </span>
                <button
                  type="button"
                  onClick={() => setOpen(false)}
                  className="p-1 rounded-lg hover:bg-white/10 transition-colors"
                  aria-label="Закрыть"
                >
                  <X size={18} />
                </button>
              </div>
              <form onSubmit={handleSubmit} className="p-4 space-y-3">
                <textarea
                  name="message"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Напишите ваше сообщение..."
                  required
                  rows={4}
                  className="w-full px-3 py-2 rounded-xl border border-black/20 text-sm focus:border-black focus:outline-none resize-none"
                />
                <button
                  type="submit"
                  className="w-full flex items-center justify-center gap-2 font-unbounded font-semibold text-sm bg-black text-white rounded-xl py-2.5 hover:bg-black/90 transition-colors"
                >
                  <Send size={16} />
                  Отправить
                </button>
              </form>
            </>
          )}
        </div>
      )}
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="flex items-center justify-center w-12 h-12 rounded-2xl bg-black text-white shadow-lg hover:bg-black/90 transition-colors"
        aria-label="Обратная связь"
      >
        <MessageCircle size={22} />
      </button>
    </div>
  )
}

export default FeedbackWidget
