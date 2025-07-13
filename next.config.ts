/**
 * Archivo de configuración de Next.js
 * Este archivo define las opciones de configuración para el proyecto.
 *
 * @property {compress} Habilita la compresión para optimizar la producción
 * @property {poweredByHeader} Elimina el encabezado X-Powered-By
 * @property {images} Configuración de imágenes remotas
 * @property {headers} Configuración de headers de seguridad
 * @property {experimental} Configuración experimental para rendimiento
 * @property {webpack} Configuración del bundler
 */

import type {NextConfig} from 'next';

const nextConfig: NextConfig = {
  /**
   * Configuración de producción optimizada
   */
  compress: true,
  poweredByHeader: false,

  /**
   * Optimización de imágenes
   */
  images: {
    domains: ['localhost'],
    formats: ['image/webp', 'image/avif'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },

  /**
   * Headers de seguridad
   */
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'Referrer-Policy', value: 'origin-when-cross-origin' },
        ],
      },
    ];
  },

  /**
   * Configuración experimental para mejor rendimiento
   */
  experimental: {
    optimizeCss: true,
    scrollRestoration: true,
  },

  /**
   * Configuración del bundler
   */
  webpack: (config, { dev, isServer }) => {
    if (!dev && !isServer) {
      config.optimization.splitChunks.chunks = 'all';
    }
    return config;
  },

  /**
   * Configuración de funciones serverless
   */
  functions: {
    "api/index.php": {
      runtime: "now-php@1.0.0"
    },
    "api/**/*.py": {
      runtime: "python@3.9"
    }
  }
};

export default nextConfig;
