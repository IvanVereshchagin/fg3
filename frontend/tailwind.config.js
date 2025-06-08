/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', // ✅ ВАЖНО: разрешаем переключение тёмной темы через class
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};