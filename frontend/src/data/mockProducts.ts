import { Product } from '@/types'

export const createPlaceholderImage = (text: string) => {
  const svg = `
    <svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
      <rect width="400" height="400" fill="#1a1a1a"/>
      <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="24" fill="#ffffff" text-anchor="middle" dominant-baseline="middle">${text}</text>
    </svg>
  `
  return `data:image/svg+xml;base64,${btoa(unescape(encodeURIComponent(svg)))}`
}

export const mockProducts: Product[] = [
  {
    id: 1,
    name: 'Антистресс кубик',
    price: 599,
    description:
      'Классический антистресс кубик с вращающимися элементами. Идеально подходит для снятия напряжения.',
    image: createPlaceholderImage('Антистресс кубик'),
    category: 'Кубики',
    inStock: true,
  },
  {
    id: 2,
    name: 'Спиннер-звезда',
    price: 799,
    description:
      'Красивый спиннер в форме звезды. Помогает сосредоточиться и расслабиться.',
    image: createPlaceholderImage('Спиннер-звезда'),
    category: 'Спиннеры',
    inStock: true,
  },
  {
    id: 3,
    name: 'Мяч-антистресс',
    price: 499,
    description:
      'Мягкий мяч для снятия стресса. Приятная текстура и эргономичная форма.',
    image: createPlaceholderImage('Мяч-антистресс'),
    category: 'Мячи',
    inStock: true,
  },
  {
    id: 4,
    name: 'Поп-ит фиджет',
    price: 699,
    description:
      'Популярный поп-ит с пузырьками. Удовлетворяющее нажатие и яркие цвета.',
    image: createPlaceholderImage('Поп-ит фиджет'),
    category: 'Поп-иты',
    inStock: true,
  },
  {
    id: 5,
    name: 'Трансформер-куб',
    price: 899,
    description:
      'Многофункциональный трансформирующийся куб. Развивает моторику и снимает стресс.',
    image: createPlaceholderImage('Трансформер-куб'),
    category: 'Трансформеры',
    inStock: true,
  },
  {
    id: 6,
    name: 'Сенсорный слайм',
    price: 549,
    description:
      'Приятный на ощупь слайм с различными текстурами. Отлично подходит для релаксации.',
    image: createPlaceholderImage('Сенсорный слайм'),
    category: 'Слаймы',
    inStock: true,
  },
  {
    id: 7,
    name: 'Вращающийся диск',
    price: 649,
    description:
      'Плавно вращающийся диск с успокаивающим эффектом. Идеален для концентрации.',
    image: createPlaceholderImage('Вращающийся диск'),
    category: 'Диски',
    inStock: true,
  },
  {
    id: 8,
    name: 'Тактильный куб',
    price: 749,
    description:
      'Куб с различными текстурами на каждой стороне. Развивает тактильные ощущения.',
    image: createPlaceholderImage('Тактильный куб'),
    category: 'Кубики',
    inStock: true,
  },
  {
    id: 9,
    name: 'Релакс-спиннер',
    price: 599,
    description:
      'Классический спиннер с плавным вращением. Помогает снять напряжение.',
    image: createPlaceholderImage('Релакс-спиннер'),
    category: 'Спиннеры',
    inStock: true,
  },
]

export const getProductById = (id: number): Product | undefined =>
  mockProducts.find((p) => p.id === id)
