import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
  // @ts-ignore - vitest config
  test: {
    globals: true,
    environment: 'jsdom',
  },
})
