/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Можно добавить кастомные цвета бренда
      },
      fontFamily: {
        unbounded: ['Unbounded', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
