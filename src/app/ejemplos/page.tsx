import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import Image from 'next/image';

export default function EjemplosPage() {
  const examples = [
    {
      title: 'Corazón de Neón',
      description: 'Una balada emocional sobre un amor perdido en la ciudad.',
      type: 'Emocional',
      audioSrc: '/audio/placeholder-1.mp3',
      imageSrc: 'https://placehold.co/400x400.png',
      imageHint: 'neon heart',
    },
    {
      title: 'El Jefe de la Sierra',
      description: 'Un corrido tumbado que narra la historia de un líder respetado.',
      type: 'Corrido',
      audioSrc: '/audio/placeholder-2.mp3',
      imageSrc: 'https://placehold.co/400x400.png',
      imageHint: 'sierra mountain',
    },
    {
      title: 'Memorias de un Verano',
      description: 'Canción nostálgica sobre momentos inolvidables de juventud.',
      type: 'Emocional',
      audioSrc: '/audio/placeholder-3.mp3',
      imageSrc: 'https://placehold.co/400x400.png',
      imageHint: 'beach sunset',
    },
    {
      title: 'La Silverado Negra',
      description: 'Relato de poder y lealtad en las calles de la ciudad.',
      type: 'Corrido',
      audioSrc: '/audio/placeholder-4.mp3',
      imageSrc: 'https://placehold.co/400x400.png',
      imageHint: 'black truck night',
    },
  ];

  return (
    <div className="container mx-auto py-12 px-4">
      <div className="text-center mb-12">
        <h1 className="font-headline text-5xl font-bold">Galería de Éxitos</h1>
        <p className="text-lg text-muted-foreground mt-4 max-w-2xl mx-auto">
          Escucha algunas de las canciones que hemos creado con nuestra IA. Cada una cuenta una historia única, como la tuya.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-8">
        {examples.map((example, index) => (
          <Card key={index} className="overflow-hidden shadow-lg hover:shadow-2xl transition-shadow duration-300">
             <CardHeader className="flex flex-row items-start gap-4 space-y-0 p-4 md:p-6">
               <Image 
                src={example.imageSrc} 
                alt={`Carátula de ${example.title}`} 
                width={100} 
                height={100} 
                className="rounded-lg aspect-square object-cover" 
                data-ai-hint={example.imageHint}
                loading="lazy"
              />
              <div className="flex-1">
                <CardTitle className="font-headline text-2xl">{example.title}</CardTitle>
                <CardDescription className="mt-1">{example.description}</CardDescription>
                <span className={`mt-2 inline-block px-2 py-1 text-xs rounded-full ${example.type === 'Emocional' ? 'bg-emotional-pink text-primary-foreground' : 'bg-corridos-red text-white'}`}>
                  {example.type}
                </span>
              </div>
            </CardHeader>
            <CardContent className="px-4 md:px-6 pb-4 md:pb-6">
              <audio controls className="w-full">
                <source src={example.audioSrc} type="audio/mpeg" />
                Tu navegador no soporta el elemento de audio.
              </audio>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
