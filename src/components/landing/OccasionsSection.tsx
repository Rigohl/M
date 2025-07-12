
import Image from 'next/image';
import { Separator } from '@/components/ui/separator';
import { occasions, guarantees } from '@/config/content';

export function OccasionsSection() {
  return (
    <section id="occasions" className="py-20 sm:py-24">
      <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-2 gap-12 items-center">
              <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full min-h-[500px]">
                  <div className="relative rounded-lg overflow-hidden shadow-lg col-span-1 row-span-1">
                      <Image src="https://images.unsplash.com/photo-1513151233558-d860c5398176?q=80&w=2070&auto=format&fit=crop" alt="Celebración de aniversario con luces bokeh" fill style={{objectFit: 'cover'}} />
                  </div>
                  <div className="relative rounded-lg overflow-hidden shadow-lg col-span-1 row-span-2">
                      <Image src="https://images.unsplash.com/photo-1604357209793-f5d1b87173b2?q=80&w=1974&auto=format&fit=crop" alt="Manos de un recién nacido" fill style={{objectFit: 'cover'}} />
                  </div>
                  <div className="relative rounded-lg overflow-hidden shadow-lg col-span-1 row-span-1">
                      <Image src="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=1974&auto=format&fit=crop" alt="Hombre rindiendo un homenaje emotivo" fill style={{objectFit: 'cover'}} />
                  </div>
              </div>
              <div>
                  <h2 className="font-headline text-4xl font-bold mb-4">
                      El detalle perfecto para cada ocasión
                  </h2>
                  <p className="text-lg text-muted-foreground mb-8">
                      Convierte tus sentimientos en un recuerdo único 🎶
                  </p>
                  <div className="space-y-6">
                      {occasions.map((item) => (
                          <div key={item.title} className="flex items-start gap-4">
                              <div className="text-2xl pt-1">{item.emoji}</div>
                              <div>
                                  <h3 className="font-semibold text-lg">{item.title}</h3>
                                  <p className="text-muted-foreground">{item.description}</p>
                              </div>
                          </div>
                      ))}
                  </div>
                  <Separator className="my-8 bg-border/50" />
                  <div className="space-y-6">
                      {guarantees.map((item) => (
                          <div key={item.title} className="flex items-start gap-4">
                              <div className="text-2xl pt-1">{item.emoji}</div>
                              <div>
                                  <h3 className="font-semibold text-lg">{item.title}</h3>
                                  <p className="text-muted-foreground">{item.description}</p>
                              </div>
                          </div>
                      ))}
                  </div>
              </div>
          </div>
      </div>
    </section>
  );
}
