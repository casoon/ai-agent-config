import type { ShowcaseExample } from '@casoon/pages-theme/showcase';
import { agentSource, agents, codexAgentSource } from './catalog';

const escapeHtml = (s: string) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// Each subagent exists once, as Markdown in agents/. scripts/render-codex-agents.py turns it
// into the TOML file Codex reads; both files are shown here exactly as committed.
export const examples: ShowcaseExample[] = agents.map(({ name, description }) => ({
  slug: name,
  title: name,
  description: `${description} Left: agents/${name}.md, linked into ~/.claude/agents. Right: codex-agents/${name}.toml, generated from it and linked into ~/.codex/agents.`,
  file: `agents/${name}.md`,
  tags: ['subagent', 'Claude Code', 'Codex'],
  input: { code: agentSource(name), lang: 'markdown' },
  output: {
    html: `<pre class="toml" style="margin:0;white-space:pre-wrap;overflow-wrap:anywhere"><code>${escapeHtml(codexAgentSource(name))}</code></pre>`,
    kind: 'panel',
  },
}));
