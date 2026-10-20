import { createServer } from 'node:http';
import { readFile, realpath, stat } from 'node:fs/promises';
import { extname, isAbsolute, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const args = process.argv.slice(2);
const option = (key, fallback) => args.includes(key) ? args[args.indexOf(key) + 1] : fallback;
const project = fileURLToPath(new URL('../', import.meta.url));
const directory = option('--dir', 'site');
if (!['site', 'dist'].includes(directory)) throw new Error('--dir debe ser site o dist');
const root = await realpath(resolve(project, directory));
const port = Number(option('--port', '4173'));
const host = option('--host', '127.0.0.1');
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.mp4': 'video/mp4', '.vtt': 'text/vtt; charset=utf-8' };
const contained = path => {
  const rel = relative(root, path);
  return rel !== '..' && !rel.startsWith(`..${sep}`) && !isAbsolute(rel);
};
const server = createServer(async (request, response) => {
  try {
    if (!['GET', 'HEAD'].includes(request.method)) {
      response.writeHead(405, { Allow: 'GET, HEAD' }).end();
      return;
    }
    const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    if (pathname.split('/').some(part => part.startsWith('.') && part !== '.nojekyll')) {
      response.writeHead(403).end('Acceso no permitido');
      return;
    }
    let path = resolve(root, `.${pathname}`);
    if (!contained(path)) { response.writeHead(403).end(); return; }
    if ((await stat(path)).isDirectory()) path = resolve(path, 'index.html');
    path = await realpath(path);
    if (!contained(path)) { response.writeHead(403).end(); return; }
    const data = await readFile(path);
    const headers = { 'Content-Type': types[extname(path)] || 'application/octet-stream', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', 'Content-Length': data.length };
    if (extname(path) === '.mp4') {
      headers['Accept-Ranges'] = 'bytes';
      if (request.headers.range) {
        const range = /^bytes=(\d*)-(\d*)$/.exec(request.headers.range);
        const start = range?.[1] ? Number(range[1]) : Math.max(0, data.length - Number(range?.[2]));
        const end = range?.[1] && range[2] ? Math.min(Number(range[2]), data.length - 1) : data.length - 1;
        if (!range || (!range[1] && !range[2]) || !Number.isSafeInteger(start) || !Number.isSafeInteger(end) || start > end || start >= data.length) {
          response.writeHead(416, { 'Content-Range': `bytes */${data.length}` }).end();
          return;
        }
        response.writeHead(206, { ...headers, 'Content-Range': `bytes ${start}-${end}/${data.length}`, 'Content-Length': end - start + 1 });
        response.end(request.method === 'HEAD' ? undefined : data.subarray(start, end + 1));
        return;
      }
    }
    response.writeHead(200, headers);
    response.end(request.method === 'HEAD' ? undefined : data);
  } catch (error) {
    response.writeHead(error instanceof URIError ? 400 : 404, { 'Content-Type': 'text/plain; charset=utf-8' }).end('Página no disponible');
  }
});
server.listen(port, host, () => console.log(`OncoNova · http://${host}:${port}`));
for (const signal of ['SIGINT', 'SIGTERM']) process.on(signal, () => server.close());
