import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile, readdir, lstat } from 'node:fs/promises';
import { resolve, relative, isAbsolute } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../.agents/skills/', import.meta.url));
const names = new Set();
let count = 0;
for (const entry of await readdir(root, { withFileTypes: true })) {
  if (!entry.isDirectory()) continue;
  const content = await readFile(resolve(root, entry.name, 'SKILL.md'), 'utf8');
  const header = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  assert(header, `Falta frontmatter: ${entry.name}`);
  const name = header[1].match(/^name:\s*([a-z0-9-]+)\s*$/m)?.[1];
  assert(name && name === entry.name, `Nombre y carpeta no coinciden: ${entry.name}`);
  assert(!names.has(name), `Nombre duplicado: ${name}`);
  assert(/^description:\s*\S/m.test(header[1]), `Falta descripción: ${name}`);
  names.add(name);
  count++;
}
const lock = JSON.parse(await readFile(resolve(root, 'sources.lock.json'), 'utf8'));
let checked = 0;
for (const skill of lock.skills) {
  assert(names.has(skill.name), `Skill registrada ausente: ${skill.name}`);
  assert(/^[a-f0-9]{40}$/.test(skill.commit), `Commit inválido: ${skill.name}`);
  for (const [file, expected] of Object.entries(skill.sha256)) {
    const base = resolve(root, skill.name);
    const path = resolve(base, file);
    const rel = relative(base, path);
    assert(rel && !isAbsolute(rel) && rel !== '..' && !rel.startsWith('../'), `Ruta fuera de skill: ${file}`);
    assert(!(await lstat(path)).isSymbolicLink(), `Enlace inesperado: ${file}`);
    const actual = createHash('sha256').update(await readFile(path)).digest('hex');
    assert.equal(actual, expected, `Copia modificada: ${skill.name}/${file}; revisar y actualizar el registro de origen`);
    checked++;
  }
}
for (const skill of ['idea-a-tarea', 'revision-landing']) {
  const instructions = await readFile(resolve(root, skill, 'SKILL.md'), 'utf8');
  for (const match of instructions.matchAll(/\]\(((?:references\/|\.\.\/)[^)#]+)(?:#[^)]*)?\)/g)) {
    await readFile(resolve(root, skill, match[1]));
  }
}
console.log(`${count} skills: nombres y descripciones presentes; ${checked} archivos externos coinciden con las huellas registradas; referencias de las skills propias disponibles.`);
