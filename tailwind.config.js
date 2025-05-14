/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./src/**/*.{js,css}"],
  theme: { extend: {} },
  plugins: [require('@tailwindcss/typography')],
};