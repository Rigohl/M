import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

export default function Home() {
  return (
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

      {/* TESTIMONIOS */}
      <section className="w-full max-w-2xl grid grid-cols-1 sm:grid-cols-2 gap-6 mb-10">
        <Card className="bg-[#191919]/80 text-white">
          <CardContent className="p-4">
            <span className="font-bold text-lg text-[#fbbf24]">⭐⭐⭐⭐⭐</span>
            <p className="italic text-sm mt-2">“El corrido para mi papá nos hizo llorar. Increíble cómo capturaron la historia y hasta la voz se parecía a un famoso.”</p>
            <span className="block mt-3 font-semibold text-xs text-gray-400">– Miriam, CDMX</span>
          </CardContent>
        </Card>
        <Card className="bg-[#191919]/80 text-white">
          <CardContent className="p-4">
            <span className="font-bold text-lg text-[#fbbf24]">⭐⭐⭐⭐⭐</span>
            <p className="italic text-sm mt-2">“Pedí un corrido alterado para mi compa y fue la sensación de la fiesta. La carátula y la base musical: 10/10.”</p>
            <span className="block mt-3 font-semibold text-xs text-gray-400">– El Güero, Monterrey</span>
          </CardContent>
        </Card>
      </section>

      {/* PAQUETES */}
      <section id="paquetes" className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-3 gap-8 mb-10">
        <Card className="bg-[#232323]/90 border-[#65d46e] border-2 text-white shadow-xl">
          <CardContent className="p-6 flex flex-col gap-2 items-center">
            <h3 className="text-xl font-bold text-[#65d46e] mb-2">Express</h3>
            <ul className="text-sm mb-4 text-gray-300 list-disc list-inside">
              <li>Letra y base musical original IA</li>
              <li>Entrega 24h</li>
              <li>Portada digital</li>
            </ul>
            <span className="font-bold text-2xl mb-2">$399 MXN</span>
            <Button variant="outline" className="w-full border-[#65d46e] text-[#65d46e] hover:bg-[#65d46e] hover:text-black transition">¡Lo quiero!</Button>
          </CardContent>
        </Card>
        <Card className="bg-[#232323]/90 border-[#fbbf24] border-2 text-white shadow-xl">
          <CardContent className="p-6 flex flex-col gap-2 items-center">
            <h3 className="text-xl font-bold text-[#fbbf24] mb-2">Premium</h3>
            <ul className="text-sm mb-4 text-gray-300 list-disc list-inside">
              <li>Letra + música IA</li>
              <li>Carátula premium</li>
              <li>Entrega prioritaria</li>
              <li>Incluye dedicatoria grabada</li>
            </ul>
            <span className="font-bold text-2xl mb-2">$599 MXN</span>
            <Button variant="outline" className="w-full border-[#fbbf24] text-[#fbbf24] hover:bg-[#fbbf24] hover:text-black transition">Quiero este</Button>
          </CardContent>
        </Card>
        <Card className="bg-[#232323]/90 border-[#38bdf8] border-2 text-white shadow-xl">
          <CardContent className="p-6 flex flex-col gap-2 items-center">
            <h3 className="text-xl font-bold text-[#38bdf8] mb-2">Famoso</h3>
            <ul className="text-sm mb-4 text-gray-300 list-disc list-inside">
              <li>Voz clonada de artista/banda</li>
              <li>Letra personalizada</li>
              <li>Audio profesional HQ</li>
              <li>Paquete sorpresa VIP</li>
            </ul>
            <span className="font-bold text-2xl mb-2">$1499 MXN</span>
            <Button variant="default" className="w-full bg-[#38bdf8] text-black hover:bg-[#0ea5e9] transition">¡Quiero un famoso!</Button>
          </CardContent>
        </Card>
      </section>

      {/* FOOTER */}
      <footer className="text-center text-gray-400 text-xs py-6">
        Powered by <span className="text-[#65d46e] font-bold">Atlas Web Pro Max</span> • Next.js • ShadCN • IA • 2024
      </footer>
    </main>
  );
}
