import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import vercel from '@astrojs/vercel';

export default defineConfig({
  output: 'server',
  adapter: vercel(),
  integrations: [
    react(),
    tailwind({
      applyBaseStyles: false,
    }),
  ],
  vite: {
    ssr: {
      noExternal: ['lucide-react'],
    },
  },
  env: {
    schema: {
      API_BASE_URL: envField('string', { context: 'client', access: 'public' }),
    },
  },
});

function envField(type: string, options: any) {
  return { type, ...options };
}
