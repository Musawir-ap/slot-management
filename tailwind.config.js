/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/*.html',
    './**/*.js',
    './**/*.css',
  ],
  theme: {
    extend: {
      spacing: {
        '1': '0.25rem',
        '2': '0.5rem',
        '3': '0.75rem',
        '4': '1rem',
        '5': '1.25rem',
        '6': '1.5rem',
        '7': '1.75rem',
        '8': '2rem',
        '9': '2.25rem',
        '10': '2.5rem',
      },
      colors:{
        booked: {
          bg: 'rgba(16, 132, 239, 0.15)',
          text: 'rgba(16, 132, 239, 1)',
        },
        pending: {
          bg: 'rgba(231, 231, 233, 1)',
          text: 'rgba(75, 79, 94, 1)',
        },
        rejected: {
          bg: 'rgba(240, 68, 56, 0.15)',
          text: 'rgba(240, 68, 56, 1)',
        },
        cancelled: {
          bg: 'rgba(240, 68, 56, 0.15)',
          text: 'rgba(240, 68, 56, 1)',
        },
        completed: {
          bg: '',
          text: '',
        },
        paid: {
          bg: '',
          text: '',
        },
        cancelled: {
          bg: '',
          text: '',
        },
        cancelled: {
          bg: '',
          text: '',
        },
        cancelled: {
          bg: '',
          text: '',
        },
        cancelled: {
          bg: '',
          text: '',
        },
        cancelled: {
          bg: '',
          text: '',
        },
      }
    },
    fontFamily: {
      // 'sans': ['ui-sans-serif', 'system-ui'],
      // 'serif': ['ui-serif', 'Georgia'],
      'mono': ['ui-monospace', 'SFMono-Regular'],
      'display': ['Gilroy'],
      'body': ['"Gilroy"'],
    },
    
  },
  plugins: [
    // require('@tailwindcss/forms'),
  ],
}

