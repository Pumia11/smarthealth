/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      fontFamily: {
        pixel: ['"Fusion Pixel"', 'monospace'],
      },
      colors: {
        pixel: {
          bg: '#1a1c2c',
          surface: '#262b44',
          primary: '#5d275d',
          secondary: '#b13e53',
          accent: '#ef7d57',
          success: '#3b5dc9',
          warning: '#ffcd75',
          text: '#f4f4f4',
          muted: '#5a6988',
          border: '#3a4466',
        },
      },
      boxShadow: {
        pixel: '4px 4px 0px 0px rgba(0, 0, 0, 0.8)',
        'pixel-sm': '2px 2px 0px 0px rgba(0, 0, 0, 0.8)',
        'pixel-lg': '6px 6px 0px 0px rgba(0, 0, 0, 0.8)',
        'pixel-inset': 'inset 2px 2px 0px 0px rgba(0, 0, 0, 0.8)',
      },
      borderRadius: {
        pixel: '0px',
      },
      animation: {
        'pixel-bounce': 'pixel-bounce 0.5s ease-in-out',
        'pixel-fade-in': 'pixel-fade-in 0.3s ease-out',
      },
      keyframes: {
        'pixel-bounce': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-4px)' },
        },
        'pixel-fade-in': {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
      },
    },
  },
  plugins: [],
};
