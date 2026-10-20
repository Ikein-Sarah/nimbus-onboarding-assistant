import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Requests to /api/... are forwarded to the FastAPI server, so the browser
// only ever talks to one origin and the backend needs no CORS setup.
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8001',
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
