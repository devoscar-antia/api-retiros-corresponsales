/**
 * Monto en pesos colombianos: miles con punto, decimales con coma (es-CO).
 * Ej.: 50000 -> "50.000"; 50000.5 -> "50.000,5"
 */

export function parseMontoCOP(input: string): number {
  const s = input.trim().replace(/\s/g, '');
  if (!s) return NaN;

  const commaIdx = s.lastIndexOf(',');
  if (commaIdx !== -1) {
    let intPart = s
      .slice(0, commaIdx)
      .replace(/\./g, '')
      .replace(/[^\d]/g, '');
    const decPart = s.slice(commaIdx + 1).replace(/[^\d]/g, '').slice(0, 2);
    if (intPart === '') intPart = '0';
    if (decPart.length > 0) {
      return parseFloat(`${intPart}.${decPart}`);
    }
    return parseInt(intPart, 10);
  }

  const digitsOnly = s.replace(/\./g, '').replace(/[^\d]/g, '');
  if (digitsOnly === '') return NaN;
  return parseInt(digitsOnly, 10);
}

export function formatMontoCOP(n: number): string {
  if (!Number.isFinite(n)) return '';
  return new Intl.NumberFormat('es-CO', {
    maximumFractionDigits: 2,
    minimumFractionDigits: 0,
  }).format(n);
}

/** Durante la edición: solo dígitos, puntos y una coma decimal. */
export function sanitizeMontoInput(raw: string): string {
  let t = raw.replace(/[^\d.,]/g, '');
  const parts = t.split(',');
  if (parts.length > 2) {
    t = parts[0] + ',' + parts.slice(1).join('');
  }
  return t;
}
