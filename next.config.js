/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configuración de producción optimizada
  compress: true,
  poweredByHeader: false,
  
  // Optimización de imágenes
  images: {
    domains: ['localhost'],
    formats: ['image/webp', 'image/avif'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },

  // Headers de seguridad
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin'
          }
        ]
      }
    ]
  },

  // Configuración experimental para mejor rendimiento
  experimental: {
    optimizeCss: true,
    scrollRestoration: true,
  },

  // Configuración del bundler
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Optimizaciones de webpack
    if (!dev && !isServer) {
      config.optimization.splitChunks.chunks = 'all';
    }
    
    return config;
  },
}

module.exports = nextConfig