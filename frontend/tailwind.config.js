/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Light theme - solid colors, no gradients
        light: {
          bg: '#FFFFFF',
          'bg-secondary': '#F9FAFB',
          text: '#111827',
          'text-secondary': '#374151',
          border: '#E5E7EB',
        },
        // Dark theme
        dark: {
          bg: '#111827',
          'bg-secondary': '#1F2937',
          text: '#F9FAFB',
          'text-secondary': '#E5E7EB',
          border: '#374151',
        },
        // Status colors
        status: {
          active: '#10B981',
          completed: '#3B82F6',
          'on-hold': '#F59E0B',
          todo: '#6B7280',
          'in-progress': '#3B82F6',
          done: '#10B981',
        },
        // Primary
        primary: {
          DEFAULT: '#3B82F6',
          light: '#60A5FA',
          dark: '#2563EB',
        },
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}
