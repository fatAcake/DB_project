import { motion } from 'framer-motion'

const BackgroundAnimation = () => {
  return (
    <div
      className="absolute inset-0 w-full h-full min-h-screen overflow-hidden pointer-events-none"
      aria-hidden
      style={{ left: 0, right: 0, top: 0, bottom: 0 }}
    >
      {/* Градиентный фон — тёплые оттенки */}
      <div
        className="absolute inset-0 w-full h-full"
        style={{
          background:
            'radial-gradient(ellipse 80% 50% at 50% -20%, rgba(147, 112, 219, 0.12), transparent), radial-gradient(ellipse 60% 40% at 100% 50%, rgba(100, 149, 237, 0.1), transparent), radial-gradient(ellipse 50% 60% at 0% 80%, rgba(255, 182, 193, 0.12), transparent), linear-gradient(180deg, #e8e4f0 0%, #ddd8e8 45%, #e2dde8 100%)',
        }}
      />
      <div
        className="absolute inset-0 opacity-0 dark:opacity-100"
        style={{
          background:
            'radial-gradient(ellipse 80% 50% at 50% -20%, rgba(255,255,255,0.06), transparent), radial-gradient(ellipse 60% 40% at 100% 50%, rgba(255,255,255,0.03), transparent), radial-gradient(ellipse 50% 60% at 0% 80%, rgba(255,255,255,0.04), transparent), linear-gradient(180deg, #0a0a0a 0%, #111 50%, #0d0d0d 100%)',
        }}
      />

      {/* Плывущие размытые орбы — цветные */}
      <motion.div
        className="absolute rounded-full dark:bg-white/15"
        style={{
          backgroundColor: 'rgba(147, 112, 219, 0.25)',
          width: 'min(85vw, 620px)',
          height: 'min(85vw, 620px)',
          left: '5%',
          top: '15%',
          filter: 'blur(65px)',
        }}
        animate={{
          x: [0, 90, -50, 0],
          y: [0, -60, 70, 0],
          scale: [1, 1.12, 0.94, 1],
        }}
        transition={{
          duration: 14,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />
      <motion.div
        className="absolute rounded-full dark:bg-white/12"
        style={{
          backgroundColor: 'rgba(100, 149, 237, 0.22)',
          width: 'min(75vw, 520px)',
          height: 'min(75vw, 520px)',
          right: '0%',
          top: '35%',
          filter: 'blur(70px)',
        }}
        animate={{
          x: [0, -80, 60, 0],
          y: [0, 80, -40, 0],
          scale: [1, 0.92, 1.12, 1],
        }}
        transition={{
          duration: 18,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />
      <motion.div
        className="absolute rounded-full dark:bg-white/12"
        style={{
          backgroundColor: 'rgba(255, 160, 180, 0.2)',
          width: 'min(65vw, 420px)',
          height: 'min(65vw, 420px)',
          left: '35%',
          bottom: '5%',
          filter: 'blur(60px)',
        }}
        animate={{
          x: [0, 50, -70, 0],
          y: [0, -80, 50, 0],
        }}
        transition={{
          duration: 16,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />

      {/* Пульсирующий градиент — яркие цвета */}
      <div
        className="absolute inset-0 w-full h-full animate-gradient-pulse pointer-events-none"
        style={{
          background:
            'radial-gradient(ellipse 120% 80% at 50% 50%, rgba(147, 112, 219, 0.35), transparent 55%), radial-gradient(ellipse 80% 120% at 85% 15%, rgba(100, 149, 237, 0.3), transparent 50%), radial-gradient(ellipse 100% 70% at 15% 85%, rgba(255, 160, 180, 0.28), transparent 50%)',
        }}
      />
    </div>
  )
}

export default BackgroundAnimation
