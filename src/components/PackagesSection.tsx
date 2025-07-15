// src/components/PackagesSection.tsx
import React from 'react';

interface Package {
  id: number;
  name: string;
  price: number;
  description: string;
  features: string[];
}

const packages: Package[] = [
  {
    id: 1,
    name: "Plan Básico",
    price: 149,
    description: "Ideal para empezar a dar vida a tus ideas.",
    features: [
      "Creación de letra base con IA",
      "Elección de género musical",
      "Entrega en formato digital (MP3)",
    ],
  },
  {
    id: 2,
    name: "Plan Premium",
    price: 299,
    description: "La experiencia completa para una canción inolvidable.",
    features: [
      "Todo lo del Plan Básico +",
      "Revisión de letra y melodía con un músico",
      "Control de composición (instrumentos, tempo)",
      "Carátula de álbum digital con IA",
      "Entrega en formatos MP3 y WAV",
    ],
  },
];

export default function PackagesSection() {
  return (
    <section id="paquetes" className="my-8">
      <div className="container mx-auto px-4 text-center">
        <h2 className="text-3xl font-bold mb-8">Nuestros Paquetes</h2>
        <div className="flex flex-wrap justify-center gap-6">
          {packages.map((pkg) => (
            <div key={pkg.id} className="bg-white rounded-lg shadow-md p-6 w-full max-w-sm flex flex-col justify-between">
              <div>
                <h3 className="text-2xl font-semibold mb-2">{pkg.name}</h3>
                <p className="text-gray-600 mb-4">{pkg.description}</p>
                <p className="text-3xl font-bold text-blue-600 mb-4">${pkg.price}</p>
                <ul className="text-left text-gray-700 mb-6">
                  {pkg.features.map((feature, index) => (
                    <li key={index} className="flex items-center mb-2">
                      <svg className="w-4 h-4 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
              <button className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded mt-auto">
                Seleccionar Plan
              </button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}