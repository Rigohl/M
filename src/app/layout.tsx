import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
// Los imports de React ya no son necesarios en la versión actual de Next.js
// para componentes server components
// Comentado temporalmente mientras trabajamos solo en la landing
// import { Header } from "@/components/Header";
// import { Footer } from "@/components/Footer";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "DualMuse | Tu historia hecha corrido",
  description: "Convierte tus emociones y anécdotas en una canción inolvidable, creada por IA y músicos expertos.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <div className="flex min-h-screen flex-col">
          {/* Comentario: Header está comentado temporalmente mientras se trabaja solo en la landing
          <Header /> */}
          <main className="flex-1">{children}</main>
          {/* Comentario: Footer está comentado temporalmente mientras se trabaja solo en la landing
          <Footer /> */}
        </div>
      </body>
    </html>
  );
}
