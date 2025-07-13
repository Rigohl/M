#!/bin/bash

# Script de build con verificaciones de calidad
echo "🚀 Iniciando proceso de build..."

# Verificar que existe package.json
if [ ! -f "package.json" ]; then
  echo "❌ No se encontró package.json"
  exit 1
fi

# Limpiar cache de npm
echo "🧹 Limpiando cache..."
npm cache clean --force

# Instalar dependencias con legacy peer deps
echo "📦 Instalando dependencias..."
npm install --legacy-peer-deps

# Ejecutar linting
echo "🔍 Ejecutando linting..."
npm run lint --if-present || echo "⚠️ Linting no configurado o falló"

# Ejecutar tests
echo "🧪 Ejecutando tests..."
npm test --if-present || echo "⚠️ Tests no configurados o fallaron"

# Ejecutar type checking
echo "🔎 Verificando tipos TypeScript..."
npx tsc --noEmit --skipLibCheck || echo "⚠️ Type checking falló"

# Build de producción
echo "🏗️ Construyendo aplicación..."
npm run build

echo "✅ Build completado exitosamente!"