// @ts-check
import { defineConfig, passthroughImageService } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://agustos.example',
  integrations: [mdx(), sitemap()],
  // The adapter optimizes no images, so it needs no sharp. Astro's default
  // service imports sharp, and npm drops sharp without an error when a system
  // libvips (Homebrew vips) makes its install fail. Use the default service
  // again when a page uses <Image> or <Picture>.
  image: { service: passthroughImageService() },
  markdown: {
    shikiConfig: {
      // Code blocks render dark on cream/white per the spec (.type-code-block).
      theme: 'github-dark',
      wrap: true,
    },
  },
});
