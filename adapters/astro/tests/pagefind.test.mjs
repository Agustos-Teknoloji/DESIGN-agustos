import assert from 'node:assert/strict';
import { access, readFile } from 'node:fs/promises';
import http from 'node:http';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const pagefindPath = path.join(root, 'dist', 'pagefind', 'pagefind.js');

test('generated Pagefind index supports the header filters', async (context) => {
  await access(pagefindPath);
  const server = http.createServer(async (request, response) => {
    const relative = new URL(request.url, 'http://localhost').pathname.replace(/^\/+/, '');
    const filePath = path.join(root, 'dist', relative);
    try {
      const body = await readFile(filePath);
      if (filePath.endsWith('.wasm')) response.setHeader('content-type', 'application/wasm');
      if (filePath.endsWith('.json')) response.setHeader('content-type', 'application/json');
      response.end(body);
    } catch {
      response.statusCode = 404;
      response.end();
    }
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  context.after(() => new Promise((resolve) => server.close(resolve)));
  const address = server.address();
  const basePath = `http://127.0.0.1:${address.port}/pagefind/`;

  const pagefind = await import(pathToFileURL(pagefindPath).href);
  await pagefind.options?.({ basePath, language: 'en' });
  await pagefind.init?.();

  const pages = await pagefind.search('typography', { filters: { kind: 'page', lang: 'en' } });
  assert.ok(pages.results.length > 0, 'expected an English page result');

  const posts = await pagefind.search('cream', { filters: { kind: 'post', lang: 'en' } });
  assert.ok(posts.results.length > 0, 'expected an English post result');

  const entry = JSON.parse(await readFile(path.join(root, 'dist', 'pagefind', 'pagefind-entry.json'), 'utf8'));
  assert.equal(entry.languages.tr.page_count, 1, 'expected the Turkish post in its language index');
  const turkishPost = await readFile(path.join(root, 'dist', 'blog', 'turkce-yerel', 'index.html'), 'utf8');
  assert.match(turkishPost, /<html lang="tr">/);
  assert.match(turkishPost, /data-search-kind="post"/);
  assert.match(turkishPost, /data-search-lang="tr"/);
});

test('built demo renders unique search surfaces and working default chrome', async () => {
  const html = await readFile(path.join(root, 'dist', 'index.html'), 'utf8');
  const count = (value) => html.split(value).length - 1;

  assert.equal(count('id="header-search-panel-desktop-en"'), 1);
  assert.equal(count('id="header-search-panel-responsive-en"'), 1);
  assert.equal(count('id="header-search-results-desktop-en"'), 1);
  assert.equal(count('id="header-search-results-responsive-en"'), 1);
  for (const href of ['/', '/about', '/blog', '/typography']) {
    assert.match(html, new RegExp(`href="${href.replace('/', '\\/')}"`));
  }
  assert.match(html, /data-pagefind-body/);
  assert.match(html, /data-search-kind="page"/);
  assert.match(html, /View source/);
  assert.doesNotMatch(html, /site-header__lang-link/);
});
