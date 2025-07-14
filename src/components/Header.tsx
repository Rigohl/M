"use client";

import Link from "next/link";
import { Button } from "./ui/button";
import { Menu, Music } from "lucide-react";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Sheet, SheetContent, SheetClose, SheetTrigger } from "./ui/sheet";
import { Separator } from "@/components/ui/separator";

export function Header() {
  const pathname = usePathname();

  const navLinks = [
    { href: "/proceso", label: "Cómo Funciona" },
    { href: "/ejemplos", label: "Ejemplos" },
    { href: "/quienes-somos", label: "Quiénes Somos" },
    { href: "/faq", label: "FAQ" },
    { href: "/ayuda", label: "Ayuda" },
    { href: "/contacto", label: "Contacto" },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 max-w-7xl items-center justify-between px-4">
        <Link href="/" className="flex items-center gap-2">
          <Music className="h-6 w-6 text-primary" />
          <span className="font-headline text-xl font-bold">DualMuse</span>
        </Link>
        <nav className="hidden items-center gap-6 text-sm md:flex">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                "transition-colors hover:text-foreground/80",
                pathname === link.href ? "text-foreground font-semibold" : "text-foreground/60"
              )}
            >
              {link.label}
            </Link>
          ))}
        </nav>
        {/* Menú móvil */}
        <div className="md:hidden">
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon">
                <Menu className="h-6 w-6" />
                <span className="sr-only">Abrir menú</span>
              </Button>
            </SheetTrigger>
            <SheetContent className="p-0 left-0">
              <div className="flex flex-col h-full">
                <div className="flex items-center gap-2 px-4 py-4 border-b">
                  <Music className="h-6 w-6 text-primary" />
                  <span className="font-headline text-xl font-bold">DualMuse</span>
                </div>
                <nav className="flex-1 flex flex-col gap-2 p-4">
                  {navLinks.map((link) => (
                    <SheetClose asChild key={link.href}>
                      <Link
                        href={link.href}
                        className={cn(
                          "transition-colors py-2 px-2 rounded hover:bg-secondary/50 hover:text-foreground/80",
                          pathname === link.href ? "text-foreground font-semibold bg-secondary/80" : "text-foreground/60"
                        )}
                      >
                        {link.label}
                      </Link>
                    </SheetClose>
                  ))}
                </nav>
                <Separator />
                <div className="p-4 text-xs text-muted-foreground text-center">
                  © {new Date().getFullYear()} DualMuse
                </div>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}