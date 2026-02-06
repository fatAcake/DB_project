import { useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useRef, useEffect, useState } from 'react'
import NavLink from './NavLink'

interface NavGroupProps {
  items: { to: string; label: string }[]
}

const NavGroup = ({ items }: NavGroupProps) => {
  const location = useLocation()
  const containerRef = useRef<HTMLDivElement>(null)
  const buttonRefs = useRef<(HTMLAnchorElement | null)[]>([])
  const [activeIndex, setActiveIndex] = useState(0)
  const [dimensions, setDimensions] = useState({ x: 0, width: 0 })

  // Находим активный индекс
  useEffect(() => {
    const index = items.findIndex((item) => {
      if (item.to === '/') {
        return location.pathname === '/'
      }
      // Точное совпадение или путь начинается с item.to и следующий символ - / или конец строки
      return location.pathname === item.to || 
             (location.pathname.startsWith(item.to) && 
              (location.pathname.length === item.to.length || location.pathname[item.to.length] === '/'))
    })
    setActiveIndex(index >= 0 ? index : -1)
  }, [location.pathname, items])

      useEffect(() => {
        const updateDimensions = () => {
          const activeButton = buttonRefs.current[activeIndex]
          const buttonsContainer = containerRef.current?.querySelector('.relative.flex') as HTMLElement

          if (activeButton && buttonsContainer && activeIndex >= 0) {
            // Используем offsetLeft для точного позиционирования относительно родителя
            const x = activeButton.offsetLeft
            const width = activeButton.offsetWidth
            
            setDimensions({
              x: x,
              width: width,
            })
          } else {
            setDimensions({ x: 0, width: 0 })
          }
        }

    // Небольшая задержка для корректного вычисления размеров после рендера
    const timeoutId = setTimeout(updateDimensions, 10)
    
    // Обновляем при изменении размера окна
    window.addEventListener('resize', updateDimensions)
    return () => {
      clearTimeout(timeoutId)
      window.removeEventListener('resize', updateDimensions)
    }
  }, [activeIndex, location.pathname, items])

  return (
    <div
      ref={containerRef}
      className="relative inline-flex border border-white p-1 rounded-2xl"
    >
      {/* Кнопки навигации */}
      <div className="relative flex gap-1">
        {items.map((item, index) => {
          const isActive = index === activeIndex && activeIndex >= 0
          return (
            <NavLink
              key={item.to}
              to={item.to}
              variant="minimal"
              className={`
                border-0 font-unbounded bg-transparent rounded-xl
                ${isActive ? 'text-black font-semibold' : 'text-white'}
                transition-colors duration-200
              `}
              style={{
                position: 'relative',
                zIndex: isActive ? 20 : 1,
                transform: 'translateZ(0)',
              }}
              ref={(el) => {
                buttonRefs.current[index] = el
              }}
            >
              {item.label.toUpperCase()}
            </NavLink>
          )
        })}
      </div>

      {/* Анимированный фон (облачко) - должен быть между кнопками и текстом */}
      {dimensions.width > 0 && activeIndex >= 0 && (
        <motion.div
          className="absolute bg-white top-1 bottom-1 pointer-events-none rounded-xl"
          style={{
            zIndex: 10,
            transform: 'translateZ(0)',
          }}
          initial={false}
          animate={{
            x: dimensions.x,
            width: dimensions.width,
          }}
          transition={{
            type: 'spring',
            stiffness: 300,
            damping: 30,
          }}
        />
      )}
    </div>
  )
}

export default NavGroup
