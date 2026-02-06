# Frontend - Интернет-магазин

## Технологии

- **React 18** + **TypeScript**
- **Vite** - сборщик
- **React Router v6** - роутинг
- **Zustand** - управление состоянием
- **@tanstack/react-query** - работа с серверным состоянием
- **Tailwind CSS** - стилизация
- **Framer Motion** - анимации
- **React Hook Form + Zod** - формы и валидация
- **Axios** - HTTP клиент
- **Swiper.js** - галерея
- **Headless UI** - доступные UI компоненты

## Установка

```bash
npm install
```

## Запуск в режиме разработки

```bash
npm run dev
```

## Сборка для продакшена

```bash
npm run build
```

## Структура проекта

```
frontend/
├── src/
│   ├── api/              # API запросы
│   ├── components/        # React компоненты
│   │   ├── layout/       # Компоненты макета
│   │   ├── ui/           # Переиспользуемые UI компоненты
│   │   └── gallery/      # Компоненты галереи
│   ├── pages/            # Страницы приложения
│   ├── store/            # Zustand stores
│   ├── types/            # TypeScript типы
│   ├── utils/            # Утилиты
│   ├── App.tsx           # Главный компонент
│   └── main.tsx          # Точка входа
├── public/               # Статические файлы
└── package.json
```

## Роуты

- `/` - Главная страница
- `/catalog` - Каталог товаров
- `/product/:id` - Страница товара
- `/login` - Авторизация
- `/register` - Регистрация
- `/profile` - Профиль пользователя
- `/admin/*` - Админ панель
- `/feedback` - Форма обратной связи
- `*` - 404 страница
