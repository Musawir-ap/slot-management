/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './client/**/*.html',
    './client/**/*.js',
    './client/**/*.css',
  ],
  theme: {
    extend: {},
    fontFamily: {
      // 'sans': ['ui-sans-serif', 'system-ui'],
      // 'serif': ['ui-serif', 'Georgia'],
      'mono': ['ui-monospace', 'SFMono-Regular'],
      'display': ['Gilroy'],
      'body': ['"Gilroy"'],
    },
    
  },
  plugins: [],
}

