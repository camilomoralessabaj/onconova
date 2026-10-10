import { cp, mkdir, readdir, realpath, rm } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { isAbsolute, relative, resolve } from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
const source = resolve(root, 'site');
const output = resolve(root, 'dist');
const forbidden = /\.(pdf|docx|xlsx|zip|log)$/i;
async function inspect(path) {
  for (const entry of await readdir(path, { withFileTypes: true })) {
    if (entry.name.startsWith('.') && entry.name !== '.nojekyll') throw new Error(`Archivo oculto inesperado: ${entry.name}`);
    if (forbidden.test(entry.name)) throw new Error(`Original privado no permitido en el sitio: ${entry.name}`);
    if (entry.isSymbolicLink()) throw new Error(`Enlace simbólico no permitido: ${entry.name}`);
    if (entry.isDirectory()) await inspect(resolve(path, entry.name));
  }
}
await inspect(source);
const projectRoot = await realpath(root);
const outputRelative = relative(projectRoot, output);
if (outputRelative !== 'dist' || isAbsolute(outputRelative)) throw new Error('Directorio de salida fuera del proyecto');
// El destino resuelto es exactamente <raíz del proyecto>/dist.
await rm(output, { recursive: true, force: true });
await mkdir(output, { recursive: true });
// Solo site/ contiene material público. Nunca empaquetar la raíz del repositorio.
await cp(source, output, { recursive: true });
console.log('Sitio preparado en dist/');
