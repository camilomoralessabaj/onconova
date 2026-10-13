import assert from 'node:assert/strict';
import { cp, lstat, mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const source = resolve(root, '.agents/skills');
const destination = resolve(root, '.claude/skills');
const manifest = resolve(destination, '.onconova-managed.json');

async function statIfPresent(path) {
  try { return await lstat(path); }
  catch (error) { if (error.code === 'ENOENT') return null; throw error; }
}

const destinationStat = await statIfPresent(destination);
assert(!destinationStat || (destinationStat.isDirectory() && !destinationStat.isSymbolicLink()),
  'La ubicación .claude/skills debe ser una carpeta local, no un enlace.');
let managed = [];
if (await statIfPresent(manifest)) {
  const saved = JSON.parse(await readFile(manifest, 'utf8'));
  assert(saved.schema_version === 1 && Array.isArray(saved.skills), 'Registro de sincronización inválido.');
  assert(saved.skills.every(name => typeof name === 'string' && /^[a-z0-9-]+$/.test(name)),
    'Nombre inválido en el registro de sincronización.');
  managed = saved.skills;
}

const names = (await readdir(source, { withFileTypes: true }))
  .filter(entry => entry.isDirectory()).map(entry => entry.name).sort();
assert(names.length > 0, 'No hay skills compartidas para sincronizar.');
for (const name of names) {
  assert(/^[a-z0-9-]+$/.test(name), `Nombre de skill inválido: ${name}`);
  await readFile(resolve(source, name, 'SKILL.md'));
  const existing = await statIfPresent(resolve(destination, name));
  assert(!existing || (managed.includes(name) && existing.isDirectory() && !existing.isSymbolicLink()),
    `Skill local no administrada: ${name}. Revisa o mueve esa carpeta antes de sincronizar.`);
}
for (const name of managed) {
  const existing = await statIfPresent(resolve(destination, name));
  assert(!existing || (existing.isDirectory() && !existing.isSymbolicLink()),
    `Copia administrada inesperada: ${name}. No se modificó.`);
}

await mkdir(destination, { recursive: true });
// Registrar la propiedad antes de copiar permite repetir una sincronización interrumpida.
await writeFile(manifest, JSON.stringify({ schema_version: 1, skills: [...new Set([...managed, ...names])] }, null, 2) + '\n');
for (const name of managed.filter(name => !names.includes(name))) {
  await rm(resolve(destination, name), { recursive: true, force: true });
}
for (const name of names) {
  const target = resolve(destination, name);
  // Solo se reemplazan copias generadas propias, nunca otras skills locales.
  if (managed.includes(name)) await rm(target, { recursive: true, force: true });
  await cp(resolve(source, name), target, { recursive: true, force: false, errorOnExist: true });
}
await writeFile(manifest, JSON.stringify({ schema_version: 1, skills: names }, null, 2) + '\n');
console.log(`${names.length} skills compartidas sincronizadas en .claude/skills/; originales en .agents/skills/.`);
