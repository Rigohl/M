// Utilidad para concatenar clases condicionalmente (como clsx pero simple)
export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ');
}
