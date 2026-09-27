// @ts-check
import casoonPages from '@casoon/pages-theme';
import { defineConfig } from 'astro/config';

// Project page: https://casoon.github.io/ai-agent-config/ — `base` is the GitHub Pages path.
export default defineConfig({
  site: 'https://casoon.github.io/ai-agent-config',
  base: '/ai-agent-config/',
  integrations: [
    casoonPages({
      name: 'ai-agent-config',
      description:
        'A shareable baseline configuration for Claude Code and Codex: global instructions, subagents and skills in one tree, symlinked into each tool’s config directory.',
      repo: 'casoon/ai-agent-config',
      license: 'MIT',
      packages: [{ label: 'Project page', href: 'https://ai-agent-config.casoon.de' }],
      docsGroups: {
        'getting-started': 'Getting started',
        guides: 'Guides',
        reference: 'Reference',
      },
      mdxComponents: './src/mdx-components.ts',
    }),
  ],
});
