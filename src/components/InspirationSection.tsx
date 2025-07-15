// src/components/InspirationSection.tsx
import Link from 'next/link';
import React from 'react';

export default function InspirationSection() {
  return (
    <section id="inspiracion" className="my-8 text-center">
      <h2 className="text-3xl font-bold mb-4">Inspírate a crear tu canción</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {/* Aquí puedes agregar tus imágenes */}
        <div className="bg-gray-200 p-4 rounded-lg">
          <img src="/images/inspiration1.jpg" alt="Inspiración 1" className="rounded-lg mb-2"/>
          <p>"Cada historia merece ser cantada."</p>
        </div>
        <div className="bg-gray-200 p-4 rounded-lg">
          <img src="/images/inspiration2.jpg" alt="Inspiración 2" className="rounded-lg mb-2"/>
          <p>"Transforma tus recuerdos en melodías."</p>
        </div>
        <div className="bg-gray-200 p-4 rounded-lg">
          <img src="/images/inspiration3.jpg" alt="Inspiración 3" className="rounded-lg mb-2"/>
          <p>"Tu vida es la mejor letra."</p>
        </div>
      </div>
       {/* Botón "Crea la tuya ahora" */}
       {/* Enlaza al ID de la sección del formulario en page.tsx */}
       <Link href="#formulario-cancion">
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-full text-lg">
            Crea la tuya ahora
          </button>
       </Link>
    </section>
  );
}