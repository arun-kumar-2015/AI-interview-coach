import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// API URL - Change this to your backend URL in production
const API_URL = 'http://localhost:8000'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: API_URL,
        changeOrigin: true,
      }
    }
  }
})
