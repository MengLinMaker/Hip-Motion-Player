import { defineConfig } from 'vite'
import { VitePWA } from 'vite-plugin-pwa'

let faviconURL = '/favicon.svg'



// https://vitejs.dev/config/
export default defineConfig({
  base: '',
  root: 'src',
  build: {
    outDir: '../dist'
  },
  plugins: [
    VitePWA({
      includeAssets: [faviconURL],
      manifest: {
        theme_color: '#ffffff',
        icons: [
          {
            src: faviconURL,
            sizes: '512x512',
            type: 'image/svg+xml',
            purpose: 'any maskable'
          },
          {
            src: faviconURL,
            sizes: '512x512',
            type: 'image/png',
          }
        ]
      },
    })
  ]
})