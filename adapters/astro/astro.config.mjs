// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://agustos.example',
  integrations: [mdx(), sitemap()],
  markdown: {
    shikiConfig: {
      // Code blocks render dark on cream/white per the spec (.type-code-block).
      theme: 'github-dark',
      wrap: true,
    },
  },
});
