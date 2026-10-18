// Small, single-page PDF 1.4 writer for this fixed academic receipt.
// Standard PDF fonts + WinAnsi preserve selectable Spanish text without remote assets.
const dateFormat = new Intl.DateTimeFormat('es-CL', {
  weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC'
});

export function appointmentDate(slot) {
  return dateFormat.format(new Date(Date.UTC(slot.year, slot.month - 1, slot.day, 12)));
}

export function sessionInstructions(modality) {
  return modality === 'Videollamada'
    ? ['Busca un lugar tranquilo y revisa tu conexión.', 'Esta demostración no habilita una sala real de atención.']
    : ['En el servicio propuesto recibirías indicaciones de llegada.', 'No existe una dirección real asignada en esta demostración.'];
}

// Keep the entire PDF ASCII: octal escapes represent WinAnsi/Latin-1 characters.
// Stream lengths and xref offsets therefore equal the serialized byte lengths.
function pdfString(value) {
  return `(${Array.from(value, character => {
    const code = character.codePointAt(0);
    if (code > 255) throw new Error('Carácter fuera del repertorio del comprobante');
    if (code < 32 || code > 126) return `\\${code.toString(8).padStart(3, '0')}`;
    return /[()\\]/.test(character) ? `\\${character}` : character;
  }).join('')})`;
}

export function createReceiptPdf({ slot, modality, channel }) {
  // Reference colors -> semantic roles -> PDF drawing commands.
  const palette = {
    raspberry: '#B01D4B', pastel: '#EDD5E7', pale: '#FBD9F1', ink: '#321521'
  };
  const roles = {
    primary: palette.raspberry, surface: palette.pale,
    statusSurface: palette.pastel, status: palette.raspberry, ink: palette.ink
  };
  const colors = Object.fromEntries(Object.entries(roles).map(([role, hex]) => [
    role, hex.slice(1).match(/../g).map(channel => (parseInt(channel, 16) / 255).toFixed(4)).join(' ')
  ]));
  const height = 841.89;
  const commands = [];
  const text = (value, x, top, size = 12, font = 'F1', color = 'ink') => {
    commands.push(`BT /${font} ${size} Tf ${colors[color]} rg 1 0 0 1 ${x} ${height - top} Tm ${pdfString(value)} Tj ET`);
  };
  const rect = (x, top, width, h, color) => {
    commands.push(`${colors[color]} rg ${x} ${height - top - h} ${width} ${h} re f`);
  };
  const rule = top => rect(48, top, 499.28, 0.7, 'surface');

  rect(0, 0, 595.28, 8, 'primary');
  rect(48, 40, 48, 48, 'surface');
  // Vector mark from assets/mark.svg, using the current brief palette.
  commands.push(`q 1 0 0 -1 48 ${height - 40} cm ${colors.primary} RG 2.8 w 1 J 1 j`,
    '12 30 m 5 18 17 7 23 20 c 29 7 42 18 35 30 c 30 39 19 36 22 28 c 24 23 31 25 30 30 c S',
    `${colors.status} RG 22 28 m 20 36 29 41 36 37 c S Q`);
  text('OncoNova', 110, 63, 27, 'F2', 'primary');
  text('Un espacio para ti', 111, 84, 11);
  text('Prototipo académico', 424, 58, 11, 'F2', 'primary');
  text('Servicio propuesto', 424, 76, 10);
  rule(112);
  text('Comprobante de agendamiento', 48, 156, 27, 'F2', 'primary');
  text('Primera sesión de apoyo psicológico', 48, 189, 17, 'F2');
  text('Usuaria de ejemplo', 48, 216, 13);

  rect(48, 242, 499.28, 155, 'surface');
  text('Fecha de la cita simulada', 68, 269, 11, 'F2', 'primary');
  text(appointmentDate(slot), 68, 294, 15, 'F2');
  text(`${slot.time} h · Hora de Santiago de Chile`, 68, 318, 13);
  text('Modalidad', 68, 351, 11, 'F2', 'primary');
  text(modality, 68, 375, 14, 'F2');
  text('Duración de ejemplo', 329, 351, 11, 'F2', 'primary');
  text('45 minutos', 329, 375, 14, 'F2');

  text('Profesional', 48, 430, 11, 'F2', 'primary');
  text('Profesional de ejemplo, sin identidad asignada', 48, 451, 13);
  rule(466);
  text('Canal seleccionado', 48, 490, 11, 'F2', 'primary');
  text(`${channel} · No se envió ningún mensaje.`, 48, 511, 13);
  rule(526);
  text('Estado', 48, 550, 11, 'F2', 'primary');
  text('Cita simulada; atención aún no realizada.', 48, 571, 13, 'F2');

  text('Antes de la primera sesión', 48, 615, 15, 'F2', 'primary');
  sessionInstructions(modality).forEach((line, index) => text(line, 48, 641 + index * 20, 12));

  rect(48, 700, 499.28, 92, 'statusSurface');
  rect(48, 700, 4, 92, 'status');
  text('Prototipo académico de OncoNova.', 68, 725, 13, 'F2', 'status');
  text('Cita simulada: no constituye una reserva real,', 68, 748, 12);
  text('no acredita atención, cobertura ni pago.', 68, 768, 12);
  text('Demostración con datos ficticios', 48, 815, 10);
  text('1 / 1', 525, 815, 10);

  const stream = commands.join('\n') + '\n';
  const objects = [
    '<< /Type /Catalog /Pages 2 0 R /Lang (es-CL) >>',
    '<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
    '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595.28 841.89] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>',
    '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>',
    '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>',
    `<< /Length ${stream.length} >>\nstream\n${stream}endstream`
  ];
  let pdf = '%PDF-1.4\n';
  const offsets = [0];
  objects.forEach((object, index) => {
    offsets.push(pdf.length);
    pdf += `${index + 1} 0 obj\n${object}\nendobj\n`;
  });
  const xref = pdf.length;
  pdf += `xref\n0 ${objects.length + 1}\n0000000000 65535 f \n`;
  offsets.slice(1).forEach(offset => { pdf += `${String(offset).padStart(10, '0')} 00000 n \n`; });
  pdf += `trailer\n<< /Size ${objects.length + 1} /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF\n`;
  return new Blob([pdf], { type: 'application/pdf' });
}
