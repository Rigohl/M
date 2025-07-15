// src/components/TestimonialsSection.tsx
import React from 'react';

interface Testimonial {
  id: number;
  quote: string;
  author: string;
}

const testimonials: Testimonial[] = [
  {
    id: 1,
    quote: "¡Increíble! Pude crear una canción para el cumpleaños de mi esposa en minutos y le encantó. La IA capturó perfectamente la emoción que quería transmitir.",
    author: "Carlos G.",
  },
  {
    id: 2,
    quote: "Siempre quise escribir una canción, pero no sabía por dónde empezar. Esta herramienta lo hizo posible. Es muy intuitiva y los resultados son sorprendentes.",
    author: "Ana M.",
  },
  {
    id: 3,
    quote: "Utilicé el servicio para una sorpresa de aniversario y la canción personalizada fue el punto culminante. Recomiendo esto a cualquiera que busque un regalo único.",
    author: "Sofía R.",
  },
];

export default function TestimonialsSection() {
  return (
    <section id="opiniones" className="my-8">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-8">Lo que dicen nuestros clientes</h2>
        <div className="flex flex-wrap justify-center gap-6">
          {testimonials.map((testimonial) => (
            <div key={testimonial.id} className="bg-white rounded-lg shadow-md p-6 max-w-sm w-full">
              <p className="text-gray-700 italic mb-4">"{testimonial.quote}"</p>
              <p className="text-gray-900 font-semibold">- {testimonial.author}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}