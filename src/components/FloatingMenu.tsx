// src/components/FloatingMenu.tsx
import Link from 'next/link';

export default function FloatingMenu() {
  return (
    <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white p-3 rounded-full shadow-lg z-50">
      <nav>
        <ul className="flex space-x-4">
          <li>
            <Link href="#inspiracion" className="hover:text-gray-300">
              Inspiración
            </Link>
          </li>
          <li>
            <Link href="#ejemplos" className="hover:text-gray-300">
              Ejemplos
            </Link>
          </li>
          <li>
            <Link href="#opiniones" className="hover:text-gray-300">
              Opiniones
            </Link>
          </li>
          <li>
            <Link href="#paquetes" className="hover:text-gray-300">
              Paquetes
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
}