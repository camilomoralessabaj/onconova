import assert from 'node:assert/strict';
import { readFile, readdir, stat } from 'node:fs/promises';
import { dirname, extname, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const site = resolve(root, 'site');
const project = JSON.parse(await readFile(resolve(site, 'content/project.json'), 'utf8'));
const expected = ['desafio', 'historia', 'propuesta', 'iteracion', 'prototipo', 'preguntas', 'validacion', 'aprendizajes'];
assert.deepEqual(project.chapters.map(chapter => chapter.id), expected, 'El relato debe seguir el recorrido aprobado');
const sources = new Set(project.sources.map(source => source.id));
assert.equal(sources.size, project.sources.length, 'Los IDs de fuentes deben ser únicos');
assert.equal(project.institution, null, 'No hay una institución piloto confirmada');
assert.equal(project.prototype.status, 'qualitative-behavioral-evaluation-reported', 'La evaluación es cualitativa y conductual reportada, no una certificación de efectividad');
assert.equal(project.validation.status, 'reported-by-team', 'Distinguir reporte del equipo de verificación documental');
assert.equal(project.prototype.evaluationSource, project.validation.source, 'El estado del prototipo debe apuntar al reporte de evaluación');
const evaluationSource = project.sources.find(source => source.id === project.validation.source);
assert.equal(evaluationSource?.type, 'team-reported-evaluation', 'La evaluación debe tener una fuente trazable del equipo');
for (const field of ['quantitativeResults', 'clinicalEffectiveness', 'realCareAccess']) {
  assert.equal(project.validation[field], null, `No inferir resultados de ${field}`);
}
assert.equal(project.validation.institutionalEvaluation, 'pending', 'Las pruebas con usuarias no acreditan evaluación operativa institucional');
for (const id of ['S04', 'S05']) {
  const document = project.sources.find(source => source.id === id);
  assert.equal(document?.destinationConfirmedBy, evaluationSource.id, `El destino ${id} debe estar confirmado por el equipo`);
  assert.equal(document.updatedTrialRecordsVerified, false, `No presentar ${id} como registro actualizado verificado`);
}
assert.equal(project.interviews.prototypeValidation, false, 'Las entrevistas exploran necesidades, no prueban la solución');
for (const metric of project.metrics) {
  assert.equal(metric.status, 'proposed', 'Las métricas son propuestas');
  assert.equal(metric.observed, null, 'No inventar resultados observados');
  assert(sources.has(metric.source), `Fuente desconocida: ${metric.source}`);
}
for (const chapter of project.chapters) {
  assert(chapter.sources.length, `Faltan fuentes en ${chapter.id}`);
  chapter.sources.forEach(id => assert(sources.has(id), `Fuente desconocida en ${chapter.id}: ${id}`));
}
const files = [];
async function collect(path) {
  for (const entry of await readdir(path, { withFileTypes: true })) {
    assert(!entry.isSymbolicLink(), `Enlace simbólico no permitido: ${entry.name}`);
    assert(!/\.(pdf|docx|xlsx|zip|log)$/i.test(entry.name), `Original privado en el sitio: ${entry.name}`);
    assert(!entry.name.startsWith('.') || entry.name === '.nojekyll', `Archivo oculto en el sitio: ${entry.name}`);
    const child = resolve(path, entry.name);
    if (entry.isDirectory()) await collect(child);
    else files.push(child);
  }
}
await collect(site);
const htmlFiles = files.filter(file => extname(file) === '.html');
const htmlByPath = new Map(await Promise.all(htmlFiles.map(async path => [path, await readFile(path, 'utf8')])));
for (const [path, html] of htmlByPath) {
  assert.match(html, /<html lang="es-CL">/, 'Idioma del sitio');
  assert.equal((html.match(/<h1\b/g) || []).length, 1, `Debe existir un h1 en ${path}`);
  assert(!/maximum-scale\s*=\s*1|user-scalable\s*=\s*no/.test(html), 'No bloquear zoom');
  assert(!/\bon(click|change|load)=/i.test(html), 'No usar handlers inline');
  const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
  assert.equal(new Set(ids).size, ids.length, `IDs duplicados en ${path}`);
  for (const match of html.matchAll(/<img\b[^>]*>/g)) {
    assert(/\balt="[^"]*"/.test(match[0]), 'Imagen sin alt');
    assert(/\bwidth="\d+"/.test(match[0]) && /\bheight="\d+"/.test(match[0]), 'Imagen sin dimensiones');
  }
  for (const match of html.matchAll(/\b(?:href|src)="([^"]+)"/g)) {
    const link = match[1];
    if (/^(?:https?:|mailto:|data:)/.test(link)) continue;
    const [base, hash] = link.split('#');
    let target = base ? resolve(dirname(path), decodeURIComponent(base.split('?')[0])) : path;
    assert(!relative(site, target).startsWith('..'), `Enlace fuera de site/: ${link}`);
    if ((await stat(target)).isDirectory()) target = resolve(target, 'index.html');
    if (hash && htmlByPath.has(target)) assert(htmlByPath.get(target).includes(`id="${hash}"`), `Ancla rota: ${link}`);
  }
}
const index = htmlByPath.get(resolve(site, 'index.html'));
let lastPosition = index.indexOf('id="inicio"');
assert(lastPosition >= 0, 'Debe conservarse la portada');
for (const id of expected) {
  const position = index.indexOf(`id="${id}"`);
  assert(position > lastPosition, `Orden de sección incorrecto: ${id}`);
  lastPosition = position;
}
for (const id of ['resultados', 'proximos-pasos']) {
  assert(index.includes(`id="${id}"`), `Conservar el ancla existente: ${id}`);
}
for (const source of project.sources) {
  assert(index.includes(`id="fuente-${source.id}"`), `Fuente sin referencia visible: ${source.id}`);
  if (source.asset) await stat(resolve(site, source.asset));
}
console.log(`Contenido coherente: ${project.chapters.length} etapas, ${sources.size} fuentes y ${project.metrics.length} metas sin resultados inventados.`);
console.log(`${htmlFiles.length} páginas y ${files.length} archivos públicos: enlaces locales, imágenes y anclas verificados.`);
