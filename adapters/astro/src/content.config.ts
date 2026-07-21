import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    deck: z.string().optional(),
    date: z.coerce.date(),
    lang: z.enum(['en', 'tr']).default('en'),
    brand: z.enum(['agustos', 'pataraz', 'pld', 'photo', 'specquick']).default('agustos'),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
