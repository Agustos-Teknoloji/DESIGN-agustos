import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = (relative) => readFile(path.join(root, relative), 'utf8');

test('chrome exposes configurable public types', async () => {
  const types = await read('src/types/chrome.ts');
  for (const name of ['ChromeLink', 'HeaderConfig', 'FooterConfig']) {
    assert.match(types, new RegExp(`export interface ${name}`));
  }
  assert.match(types, /moreLabel\?: string/);
  assert.match(types, /note\?: string/);
  assert.match(types, /links\?: ChromeLink\[\]/);
  assert.match(types, /export const NAV_LIMIT = 5/);
  assert.doesNotMatch(types, /FooterColumn|columns|description\?:|cta\?: ChromeLink \| null;\n\}\n\nexport const NAV/);
});

test('nav over five items keeps four and moves the rest under More', async () => {
  const types = await read('src/types/chrome.ts');
  const body = types.match(/export function splitNav<T>\(items: T\[\]\): \[T\[\], T\[\]\] \{([\s\S]*?)\n\}/)[1];
  const splitNav = new Function('items', 'const NAV_LIMIT = 5;' + body);
  const items = (n) => Array.from({ length: n }, (_, i) => i + 1);
  assert.deepEqual(splitNav(items(5)), [items(5), []]);
  assert.deepEqual(splitNav(items(7)), [[1, 2, 3, 4], [5, 6, 7]]);
  assert.match(types, /more: 'Daha fazla'/);
  assert.match(types, /more: 'More'/);

  const header = await read('src/components/Header.astro');
  assert.match(header, /splitNav\(nav\)/);
  assert.match(header, /<details class="site-header__more">/);
  assert.match(header, /<summary class="site-header__link">\{moreLabel\}<\/summary>/);
  assert.match(header, /<div class="site-header__more-menu">/);
  assert.match(header, /class="site-header__more-link"\s+aria-current=\{currentState\(item\.href, pathname\)\}/);
});

test('aria-current is page on the exact route and true on a parent section', async () => {
  const types = await read('src/types/chrome.ts');
  const body = types.match(/export function currentState\(href: string, pathname: string\): 'page' \| 'true' \| undefined \{([\s\S]*?)\n\}/)[1];
  const currentState = new Function('href', 'pathname', body);
  // The exact route, with or without a trailing slash.
  assert.equal(currentState('/haberler/', '/haberler/'), 'page');
  assert.equal(currentState('/haberler', '/haberler/'), 'page');
  assert.equal(currentState('/haberler/', '/haberler'), 'page');
  // A nested route: the parent is the current section, not the current page.
  assert.equal(currentState('/haberler/', '/haberler/guncel/'), 'true');
  assert.equal(currentState('/haberler', '/haberler/guncel'), 'true');
  // A sibling that shares a prefix, an anchor and an external link are not current.
  assert.equal(currentState('/haber', '/haberler/'), undefined);
  assert.equal(currentState('#top', '/'), undefined);
  assert.equal(currentState('https://example.com/haberler', '/haberler/'), undefined);
  // A fragment or a query link is a place on the page, not the page (Codex, PR #76).
  assert.equal(currentState('/about#team', '/about'), undefined);
  assert.equal(currentState('/about#jobs', '/about/'), undefined);
  assert.equal(currentState('/haberler/?sayfa=2', '/haberler/guncel/'), undefined);
  // Home is only ever exact.
  assert.equal(currentState('/', '/'), 'page');
  assert.equal(currentState('/', '/haberler/'), undefined);

  const header = await read('src/components/Header.astro');
  assert.doesNotMatch(header, /isCurrent|aria-current=\{[^}]*'page'/, 'the header sets aria-current from currentState only');
  assert.equal(header.match(/aria-current=\{currentState\(item\.href, pathname\)\}/g).length, 2);
});

test('layout indexes only main content with language and kind filters', async () => {
  const layout = await read('src/layouts/BaseLayout.astro');
  assert.match(layout, /data-pagefind-body/);
  assert.match(layout, /kind\[data-search-kind\], lang\[data-search-lang\]/);
  assert.match(layout, /searchKind\?: 'page' \| 'post'/);
  assert.doesNotMatch(layout, /Sidebar|MobileHeader|layout-with-sidebar/);
});

test('every page names its screen on <body>', async () => {
  const layout = await read('src/layouts/BaseLayout.astro');
  assert.match(layout, /screen\?: string/);
  assert.match(layout, /<body class=\{bodyClass\} data-screen=\{screen\}>/);
  for (const [page, screen] of [
    ['src/pages/index.astro', 'home'],
    ['src/pages/about.astro', 'static'],
    ['src/pages/blog/index.astro', 'content-index'],
    ['src/pages/blog/[...slug].astro', 'content'],
    ['src/pages/typography.astro', 'content'],
  ]) {
    assert.match(await read(page), new RegExp(`screen="${screen}"`), page);
  }
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
  assert.match(header, /popovertarget="site-header-panel"/);
  assert.match(header, /config\.theme === true/);
  assert.match(header, /agustos-button agustos-button--primary site-header__cta/);
  assert.match(header, /setAttribute\('data-theme', 'dark'\)/);
  assert.match(header, /header-search-panel-desktop-\$\{idSuffix\}/);
  assert.match(header, /header-search-panel-responsive-\$\{idSuffix\}/);
  assert.match(header, /groups\.forEach\(\(group\) => renderGroup/);
  assert.match(search, /desktop-dropdown/);
  assert.match(search, /responsive-row/);
  assert.match(await read('src/styles/tokens.css'), /\.site-header__search-field input \{[^}]*font-size: 16px;/);
});

test('header and footer use the shared frame and accessible control sizes', async () => {
  const header = await read('src/components/Header.astro');
  const footer = await read('src/components/Footer.astro');
  const search = await read('src/components/HeaderSearch.astro');
  const utility = await read('src/components/HeaderUtility.astro');

  assert.match(header, /site-header__bar site-frame/);
  assert.match(footer, /site-footer__inner site-frame/);
  assert.doesNotMatch(footer, /<style>/);
  assert.match(footer, /<ul class="site-footer__links">/);
  assert.match(footer, /class="site-footer__link"/);
  assert.match(footer, /<p class="type-footnote">\{note\}<\/p>/);
  assert.doesNotMatch(footer, /site-footer__(cols|col|col-heading|list|cta)\b|agustos-button/);
  // v7.3.0: the kit styles the search and the language link; the components carry no <style>.
  const kit = await read('src/styles/tokens.css');
  for (const source of [header, search, utility]) assert.doesNotMatch(source, /<style>/);
  assert.match(kit, /\.site-header__search-result a:focus-visible \{[^}]*outline: 2px solid var\(--signal\)/);
  assert.match(kit, /\.site-header__search-toggle \{[^}]*width: var\(--control-min\)/);
  assert.match(utility, /theme = false/);
  assert.match(header, /class="site-lockup"/);
  assert.match(footer, /class="site-lockup"/);
  assert.doesNotMatch(header, /BrandLockup/);
  assert.doesNotMatch(footer, /BrandLockup/);
});

test('homepage follows locked marketing composition', async () => {
  const page = await read('src/pages/index.astro');
  const layout = await read('src/layouts/BaseLayout.astro');
  const header = await read('src/components/Header.astro');
  assert.match(page, /Light, <mark class="type-highlight">placed with intent<\/mark>\./);
  assert.equal(page.split('type-highlight').length - 1, 1, 'one highlighter per page');
  assert.match(page, /<div class="hero-actions">\s*<a class="agustos-button agustos-button--primary"[^>]*>[^<]+<\/a>\s*<a class="agustos-button agustos-button--secondary"/);
  assert.doesNotMatch(page, /hero-links?\b|hero-link--|hero-action\b|hero-action--|site-sidebar|columns:|description: '/);
  assert.match(page, /band band--cream/);
  assert.match(page, /Request pricing/);
  assert.match(page, /Selected work/);
  assert.match(page, /hero-trust/);
  assert.doesNotMatch(page, /type-blockquote|type-pullquote/);
  assert.doesNotMatch(page, /→|arrow/);
  assert.doesNotMatch(page, /data-theme-toggle|setTheme/);
  assert.match(layout, /header\.theme === true/);
  assert.match(header, /config\.theme === true/);
});
