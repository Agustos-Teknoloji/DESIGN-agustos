import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = (relative) => readFile(path.join(root, relative), 'utf8');

test('chrome exposes configurable public types', async () => {
  const types = await read('src/types/chrome.ts');
  for (const name of ['ChromeLink', 'HeaderConfig', 'FooterColumn', 'FooterConfig']) {
    assert.match(types, new RegExp(`export interface ${name}`));
  }
});

test('layout indexes only main content with language and kind filters', async () => {
  const layout = await read('src/layouts/BaseLayout.astro');
  assert.match(layout, /data-pagefind-body/);
  assert.match(layout, /kind\[data-search-kind\], lang\[data-search-lang\]/);
  assert.match(layout, /searchKind\?: 'page' \| 'post'/);
  assert.doesNotMatch(layout, /Sidebar|MobileHeader|layout-with-sidebar/);
});

test('header search matches the production interaction contract', async () => {
  const header = await read('src/components/Header.astro');
  const search = await read('src/components/HeaderSearch.astro');

  assert.match(header, /const SEARCH_THRESHOLD = 2/);
  assert.match(header, /await delay\(180\)/);
  assert.match(header, /kind, lang/);
  assert.match(header, /event\.key === 'ArrowDown'/);
  assert.match(header, /event\.key === 'Enter'/);
  assert.match(header, /event\.key === 'Escape'/);
  assert.match(header, /setAttribute\('data-nav-open', 'true'\)/);
  assert.match(header, /setAttribute\('data-theme', 'dark'\)/);
  assert.match(search, /desktop-dropdown/);
  assert.match(search, /responsive-row/);
  assert.match(search, /\.site-header__search--responsive \.site-header__search-field input \{ font-size: 16px; \}/);
});

test('header and footer use the shared frame and accessible control sizes', async () => {
  const header = await read('src/components/Header.astro');
  const footer = await read('src/components/Footer.astro');
  const search = await read('src/components/HeaderSearch.astro');
  const utility = await read('src/components/HeaderUtility.astro');

  assert.match(header, /site-header__bar site-frame/);
  assert.match(footer, /site-footer__inner site-frame/);
  for (const source of [header, search, utility]) assert.match(source, /44px/);
});
