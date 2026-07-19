import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { micromark } from 'micromark';
import { gfm, gfmHtml } from 'micromark-extension-gfm';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '../../..');
const sourcePath = resolve(root, 'DESIGN.md');
const outputPath = resolve(root, 'artifacts/agustos-design-system-v3.0.0.html');

const source = await readFile(sourcePath, 'utf8');

function stripTags(value) {
  return value.replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
}

function slugify(value) {
  return stripTags(value)
    .toLocaleLowerCase('tr')
    .normalize('NFKD')
    .replace(/[^\p{Letter}\p{Number}]+/gu, '-')
    .replace(/^-+|-+$/g, '') || 'section';
}

let htmlBody = micromark(source, {
  extensions: [gfm()],
  htmlExtensions: [gfmHtml()],
});

const usedSlugs = new Map();
const toc = [];

htmlBody = htmlBody.replace(/<h([1-3])>([\s\S]*?)<\/h\1>/g, (_match, level, inner) => {
  const base = slugify(inner);
  const count = usedSlugs.get(base) || 0;
  usedSlugs.set(base, count + 1);
  const id = count === 0 ? base : `${base}-${count + 1}`;
  const depth = Number(level);

  if (depth <= 3) {
    toc.push({ id, depth, title: stripTags(inner) });
  }

  return `<h${level} id="${id}"><a class="heading-anchor" href="#${id}" aria-label="Link to ${stripTags(inner)}">#</a>${inner}</h${level}>`;
});

const tocHtml = toc
  .filter((item) => item.depth <= 2)
  .map((item) => `<a class="toc__item toc__item--${item.depth}" href="#${item.id}">${item.title}</a>`)
  .join('\n');

const renderedAt = new Intl.DateTimeFormat('en-GB', {
  dateStyle: 'long',
  timeStyle: 'short',
  timeZone: 'Europe/Istanbul',
}).format(new Date());

const html = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Ağustos Design System v3.0.0</title>
    <style>
      :root {
        --paper: #fefcf2;
        --ink: #1a1a1a;
        --ink-soft: #4a4a4a;
        --ink-faint: #8a8a8a;
        --rule: #e8e3d0;
        --brand: #cf142a;
        --display: 'Inter Tight Variable', 'Inter Tight', 'Inter Variable', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        --body: 'Inter Variable', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        --mono: 'JetBrains Mono', 'SF Mono', Menlo, Consolas, ui-monospace, monospace;
      }

      * { box-sizing: border-box; }

      html {
        background: var(--paper);
        color: var(--ink);
        font-family: var(--body);
        font-feature-settings: "locl" on, "kern" on, "ss01" on;
        -webkit-font-smoothing: antialiased;
        text-rendering: optimizeLegibility;
        scroll-behavior: smooth;
      }

      body {
        margin: 0;
        min-height: 100vh;
      }

      a {
        color: inherit;
        font-weight: 600;
        text-decoration: underline;
        text-decoration-color: var(--brand);
        text-decoration-thickness: 2px;
        text-underline-offset: 3px;
      }

      a:focus-visible {
        outline: 2px solid var(--brand);
        outline-offset: 4px;
      }

      .page {
        display: grid;
        grid-template-columns: minmax(220px, 280px) minmax(0, 1fr);
        min-height: 100vh;
      }

      .toc {
        position: sticky;
        top: 0;
        height: 100vh;
        padding: 2rem 1.25rem 2rem 1.5rem;
        border-right: 1px solid var(--rule);
        overflow: auto;
      }

      .toc__brand {
        display: block;
        margin-bottom: 1.75rem;
        font-family: var(--display);
        font-size: 22px;
        font-weight: 650;
        letter-spacing: 0;
        color: var(--brand);
        text-decoration: none;
      }

      .toc__meta {
        margin: 0 0 1.5rem;
        color: var(--ink-faint);
        font-size: 12.5px;
        line-height: 1.5;
      }

      .toc__item {
        display: block;
        margin: 0 0 0.7rem;
        color: var(--ink-soft);
        font-family: var(--display);
        font-size: 13px;
        line-height: 1.35;
        text-decoration: none;
      }

      .toc__item:hover {
        color: var(--ink);
        text-decoration: underline;
        text-decoration-color: var(--brand);
      }

      .toc__item--1 {
        color: var(--ink);
        font-weight: 600;
      }

      main {
        width: min(calc(100% - 3rem), 980px);
        margin: 0 auto;
        padding: 4rem 0 7rem;
      }

      article > *:first-child { margin-top: 0; }

      h1, h2, h3, h4, h5, h6 {
        font-family: var(--display);
        color: var(--ink);
        text-wrap: balance;
      }

      h1 {
        margin: 0 0 0.45em;
        font-size: clamp(46px, 7vw, 88px);
        font-weight: 300;
        line-height: 0.98;
        letter-spacing: -0.044em;
      }

      h2 {
        margin: 2.5em 0 1em;
        padding-top: 0.15em;
        border-top: 1px solid var(--rule);
        font-size: 26px;
        font-weight: 500;
        line-height: 1.18;
        letter-spacing: -0.014em;
      }

      h3 {
        margin: 2.25em 0 0.8em;
        font-size: 18px;
        font-style: italic;
        font-weight: 500;
        line-height: 1.3;
      }

      h4 {
        margin: 2em 0 0.8em;
        color: var(--ink-soft);
        font-size: 12px;
        font-weight: 700;
        line-height: 1.4;
        letter-spacing: 0.14em;
        text-transform: uppercase;
      }

      .heading-anchor {
        float: left;
        width: 1em;
        margin-left: -1.2em;
        color: var(--brand);
        font-weight: 600;
        text-decoration: none;
        opacity: 0;
      }

      h1:hover .heading-anchor,
      h2:hover .heading-anchor,
      h3:hover .heading-anchor,
      .heading-anchor:focus-visible {
        opacity: 1;
      }

      p, li, dd {
        font-size: 16.5px;
        line-height: 1.65;
      }

      p, ul, ol, dl, blockquote, pre, table {
        margin: 0 0 1em;
      }

      ul, ol { padding-left: 1.5em; }
      li::marker { color: var(--brand); }

      dt {
        margin-top: 1em;
        font-weight: 600;
      }

      dd {
        margin-left: 0;
        color: var(--ink-soft);
      }

      blockquote {
        padding: 0.25em 0 0.25em 1.25em;
        border-left: 2px solid var(--brand);
        color: var(--ink-soft);
        font-style: italic;
      }

      code {
        font-family: var(--mono);
        font-size: 0.86em;
        padding: 1px 5px;
        border-radius: 3px;
        background: rgba(0, 0, 0, 0.05);
      }

      pre {
        overflow-x: auto;
        padding: 1em 1.25em;
        border-radius: 4px;
        background: var(--ink);
        color: var(--rule);
      }

      pre code {
        padding: 0;
        background: transparent;
        color: inherit;
        font-size: 13.5px;
      }

      table {
        display: block;
        width: 100%;
        overflow-x: auto;
        border-collapse: collapse;
        font-size: 14px;
        font-variant-numeric: tabular-nums;
      }

      th {
        font-family: var(--display);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-align: left;
        text-transform: uppercase;
        color: var(--ink-soft);
        border-bottom: 2px solid var(--rule);
      }

      td {
        border-bottom: 1px solid var(--rule);
        vertical-align: top;
      }

      th, td {
        padding: 0.55em 0.8em;
      }

      hr {
        height: 1px;
        margin: 2.5em 0 1em;
        border: 0;
        background: var(--rule);
      }

      strong { font-weight: 700; }
      em { font-style: italic; }

      .render-note {
        margin: 0 0 2rem;
        color: var(--ink-faint);
        font-size: 13.5px;
      }

      @media (max-width: 900px) {
        .page {
          display: block;
        }

        .toc {
          position: static;
          height: auto;
          border-right: 0;
          border-bottom: 1px solid var(--rule);
        }

        .toc__items {
          columns: 2;
          column-gap: 1.5rem;
        }

        main {
          width: min(calc(100% - 2rem), 760px);
          padding: 3rem 0 5rem;
        }

        .heading-anchor {
          display: none;
        }
      }

      @media (max-width: 560px) {
        .toc__items { columns: 1; }
        h1 { font-size: 42px; }
        h2 { font-size: 23px; }
      }
    </style>
  </head>
  <body>
    <div class="page">
      <aside class="toc" aria-label="Table of contents">
        <a class="toc__brand" href="#ağustos-design-system">ağustos</a>
        <p class="toc__meta">Rendered from DESIGN.md<br />${renderedAt} Istanbul time</p>
        <nav class="toc__items">
          ${tocHtml}
        </nav>
      </aside>
      <main>
        <p class="render-note">Standalone HTML preview of the canonical design specification.</p>
        <article>
          ${htmlBody}
        </article>
      </main>
    </div>
  </body>
</html>
`;

await mkdir(dirname(outputPath), { recursive: true });
await writeFile(outputPath, html, 'utf8');
console.log(outputPath);
