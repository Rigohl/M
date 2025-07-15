// src/components/ExamplesSection.tsx
import React from 'react';

// Puedes definir una interfaz para la estructura de los datos de ejemplo
interface SongExample {
  id: number;
  title: string;
  description: string;
  audioUrl: string; // O la URL donde se pueda escuchar la canción
}

// Datos de ejemplo (puedes reemplazar esto con datos reales de tu backend o un archivo JSON)
const songExamples: SongExample[] = [
  {
    id: 1,
    title: "Melodía de un Recuerdo",
    description: "Una canción sobre la nostalgia de la infancia.",
    audioUrl: "/audio/melodia_recuerdo.mp3",
  },
  {
    id: 2,
    title: "Ritmo de la Ciudad",
    description: "Inspirada en el pulso vibrante de la vida urbana.",
    audioUrl: "/audio/ritmo_ciudad.mp3",
  },
  {
    id: 3,
    title: "Susurro del Viento",
    description: "Una balada suave sobre la naturaleza y la tranquilidad.",
    audioUrl: "/audio/susurro_viento.mp3",
  },
  // Agrega más ejemplos aquí
];

export default function ExamplesSection() {
  return (
    <section id="ejemplos" className="my-8 text-center">
      <h2 className="text-3xl font-bold mb-8">Ejemplos de canciones creadas con nuestra IA</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {songExamples.map((example) => (
          <div key={example.id} className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold mb-2">{example.title}</h3>
            <p className="text-gray-600 mb-4">{example.description}</p>
            {/* Aquí podrías incrustar un reproductor de audio o un enlace */}
            <audio controls src={example.audioUrl} className="w-full">
              Tu navegador no soporta el elemento de audio.
            </audio>
          </div>
        ))}
      </div>
    </section>
  );
}