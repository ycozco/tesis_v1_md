import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 8050,
    proxy: {
      '/api': {
        target: process.env.AGRO_API_TARGET || 'http://localhost:5001',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
