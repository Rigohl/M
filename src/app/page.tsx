import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import FloatingMenu from '@/components/FloatingMenu';
import InspirationSection from '@/components/InspirationSection';
import ExamplesSection from '@/components/ExamplesSection';
import TestimonialsSection from '@/components/TestimonialsSection';
import PackagesSection from '@/components/PackagesSection';

export default function Home() {
  return ( // Main container div wrapping all content
    <main className="flex flex-col min-h-screen items-center justify-center bg-gradient-to-br from-[#191919] via-[#111827] to-[#1e293b] px-4 py-10">
      {/* HERO */}
      <section className="w-full max-w-2xl text-center bg-black/60 rounded-3xl shadow-2xl p-10 mb-10 border border-[#323232]">
        <h1 className="text-4xl sm:text-5xl font-extrabold mb-4 text-white drop-shadow-2xl">
          Tu historia, <span className="text-[#65d46e]">tu corrido.</span>
        </h1>
        <p className="text-lg sm:text-xl mb-8 text-gray-200 font-light leading-relaxed">
          Convierte tus emociones y anécdotas en una <span className="font-semibold text-[#fbbf24]">canción inolvidable</span>, creada por IA y músicos expertos.
          <br />
          Elige tu paquete, cuenta tu historia y recibe una canción única—con letra, base musical, portada e incluso voz de famoso si lo deseas.
        </p>
        <Button
          size="lg"
          className="bg-[#65d46e] hover:bg-[#a3e635] text-black text-lg font-bold px-8 py-6 shadow-md transition-all"
        >
          ¡Quiero mi corrido personalizado!
        </Button>
        <div className="mt-6 flex flex-col sm:flex-row gap-5 justify-center">
          <a href="#paquetes" className="text-sm text-[#65d46e] hover:underline underline-offset-4 font-semibold">
            Ver paquetes y precios
          </a>
          <a href="#como-funciona" className="text-sm text-gray-400 hover:text-white hover:underline underline-offset-4">
            ¿Cómo funciona?
          </a>
        </div>
      </section>

      {/* Use imported components for sections */}
      <InspirationSection />
      <ExamplesSection />
      <TestimonialsSection />
      <PackagesSection />

      {/* Song Creation Form Section */}
      {/* Assuming SongCreationForm needs to be here based on the blueprint */}
      <section id="formulario-cancion" className="my-8">
        {/* <SongCreationForm />  Uncomment and import if needed */}
      </section>
      {/* FOOTER */}
      <footer className="text-center text-gray-400 text-xs py-6">
        Powered by <span className="text-[#65d46e] font-bold">Atlas Web Pro Max</span> • Next.js • ShadCN • IA • 2024
      </footer>
    </main>
  );
}

