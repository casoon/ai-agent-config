// Reads the agents and skills straight from the repository at build time, so the lists on
// this site always match the folders that the install scripts link.

export interface Entry {
  name: string;
  description: string;
  /** Path in the repository, e.g. "skills/seo/SKILL.md". */
  file: string;
}

const agentSources = import.meta.glob<string>('../../agents/*.md', {
  query: '?raw',
  import: 'default',
  eager: true,
});
const codexSources = import.meta.glob<string>('../../codex-agents/*.toml', {
  query: '?raw',
  import: 'default',
  eager: true,
});
const skillSources = import.meta.glob<string>('../../skills/*/SKILL.md', {
  query: '?raw',
  import: 'default',
  eager: true,
});

/** name and description from a YAML frontmatter block (single-line or folded values). */
function frontmatter(source: string): Record<string, string> {
  const block = /^---\n([\s\S]*?)\n---/.exec(source)?.[1] ?? '';
  const fields: Record<string, string> = {};
  let key: string | null = null;
  for (const line of block.split('\n')) {
    const field = /^([A-Za-z_-]+):\s*(.*)$/.exec(line);
    if (field) {
      key = field[1];
      fields[key] = /^[>|][-+]?$/.test(field[2]) ? '' : field[2];
    } else if (key && /^\s+\S/.test(line)) {
      fields[key] = `${fields[key]} ${line.trim()}`.trim();
    }
  }
  for (const [k, v] of Object.entries(fields)) {
    fields[k] = v.replace(/^(["'])([\s\S]*)\1$/, '$2');
  }
  return fields;
}

function toEntries(sources: Record<string, string>): Entry[] {
  return Object.entries(sources)
    .map(([path, source]) => {
      const file = path.replace(/^(\.\.\/)+/, '');
      const meta = frontmatter(source);
      const fallback = file.split('/').at(-2) ?? file;
      return { name: meta.name || fallback, description: meta.description ?? '', file };
    })
    .sort((a, b) => a.name.localeCompare(b.name));
}

export const agents: Entry[] = toEntries(agentSources);
export const skills: Entry[] = toEntries(skillSources);

export function agentSource(name: string): string {
  const source = agentSources[`../../agents/${name}.md`];
  if (source === undefined) throw new Error(`Unknown agent: ${name}`);
  return source;
}

export function codexAgentSource(name: string): string {
  const source = codexSources[`../../codex-agents/${name}.toml`];
  if (source === undefined) throw new Error(`No generated Codex agent for: ${name}`);
  return source;
}
