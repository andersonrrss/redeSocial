/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.{html,js}", "./app/static/**/*.{html,js}"],
  theme: {
    extend: {
      backgroundImage: {
        'none-sm': 'none',
      },
    },
  },
  variants: {
    extend: {
      backgroundImage: ['responsive', 'hover', 'focus', 'active', 'group-hover'],
    },
  },
  plugins: [],
}

