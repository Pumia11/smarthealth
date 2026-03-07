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
          bg: '#0f0f23',
          surface: '#1a1a3e',
          primary: '#ff6b9d',
          secondary: '#c44569',
          cyan: '#4ecdc4',
          cyanDark: '#2ab7ca',
          yellow: '#ffe66d',
          yellowDark: '#f7b731',
          green: '#a8e6cf',
          greenDark: '#56ab91',
          text: '#ccccdc',
          muted: '#5a5a8a',
          border: '#3d3d6b',
        },
      },
      boxShadow: {
        pixel: '8px 8px 0px 0px rgba(0, 0, 0, 0.8)',
        'pixel-sm': '4px 4px 0px 0px rgba(0, 0, 0, 0.8)',
        'pixel-lg': '12px 12px 0px 0px rgba(0, 0, 0, 0.8)',
        'pixel-inset': 'inset 4px 4px 0px 0px rgba(0, 0, 0, 0.8)',
        'pixel-glow-pink': '0 0 20px rgba(255, 107, 157, 0.5), 0 0 40px rgba(255, 107, 157, 0.3)',
        'pixel-glow-cyan': '0 0 20px rgba(78, 205, 196, 0.5), 0 0 40px rgba(78, 205, 196, 0.3)',
      },
      borderWidth: {
        pixel: '4px',
      },
      animation: {
        'pixel-bounce': 'pixel-bounce 0.3s steps(2) infinite',
        'pixel-pulse': 'pixel-pulse 0.5s steps(2) infinite',
        'pixel-float': 'pixel-float 2s steps(4) infinite',
      },
      keyframes: {
        'pixel-bounce': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-8px)' },
        },
        'pixel-pulse': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.5' },
        },
        'pixel-float': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-4px)' },
        },
      },
    },
  },
  plugins: [],
};
