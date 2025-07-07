/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'sage-green': '#87A96B',
        'sage-dark': '#6B8E4F',
        'sage-light': '#A3C083',
        'sage-bg': '#F8FAF6',
        'sage-text': '#2D3748',
      },
      animation: {
        'rainbow-border': 'rainbow-border 3s ease-in-out infinite',
        'pulse-gentle': 'pulse-gentle 2s ease-in-out infinite',
        'slide-in': 'slide-in 0.5s ease-out',
        'fade-in': 'fade-in 0.3s ease-out',
      },
      keyframes: {
        'rainbow-border': {
          '0%, 100%': {
            'border-color': '#ff6b6b',
            'box-shadow': '0 0 20px rgba(255, 107, 107, 0.3)',
          },
          '16.66%': {
            'border-color': '#ffa726',
            'box-shadow': '0 0 20px rgba(255, 167, 38, 0.3)',
          },
          '33.33%': {
            'border-color': '#ffeb3b',
            'box-shadow': '0 0 20px rgba(255, 235, 59, 0.3)',
          },
          '50%': {
            'border-color': '#66bb6a',
            'box-shadow': '0 0 20px rgba(102, 187, 106, 0.3)',
          },
          '66.66%': {
            'border-color': '#42a5f5',
            'box-shadow': '0 0 20px rgba(66, 165, 245, 0.3)',
          },
          '83.33%': {
            'border-color': '#ab47bc',
            'box-shadow': '0 0 20px rgba(171, 71, 188, 0.3)',
          },
        },
        'pulse-gentle': {
          '0%, 100%': {
            opacity: '1',
            transform: 'scale(1)',
          },
          '50%': {
            opacity: '0.8',
            transform: 'scale(1.02)',
          },
        },
        'slide-in': {
          '0%': {
            transform: 'translateX(-100%)',
            opacity: '0',
          },
          '100%': {
            transform: 'translateX(0)',
            opacity: '1',
          },
        },
        'fade-in': {
          '0%': {
            opacity: '0',
          },
          '100%': {
            opacity: '1',
          },
        },
      },
    },
  },
  plugins: [],
};