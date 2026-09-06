---
name: fumadocs
description: Scaffold, write, and configure Fumadocs documentation sites and MDX pages. Use when creating docs pages, structuring page trees with meta.json, configuring fumadocs-ui components (Callout, Tabs, Steps, Cards, TypeTable, Accordion, Files), setting up Fumadocs in Next.js or React frameworks, or integrating OpenAPI, search, and llms.txt.
---

# Fumadocs

Build, write, and structure fast, elegant documentation sites using Fumadocs.

## Mental Model

Fumadocs consists of four cooperative packages:
1. `fumadocs-core`: Headless runtime handling content loader logic, page trees, search indexing, and MDX AST plugins.
2. `fumadocs-ui`: Presentation layer built on Tailwind CSS v4. Supplies layout shells (`DocsLayout`, `NotebookLayout`, `FluxLayout`, `GlassLayout`) and interactive components (`Callout`, `Tabs`, `Steps`, `Cards`, `TypeTable`, `Files`, `Accordion`).
3. `fumadocs-mdx`: Content source compiler that transforms markdown and MDX files into type-safe JavaScript collections via `source.config.ts` or `fumadocs-mdx/macro`.
4. `@fumadocs/cli`: Tooling for rapid scaffolding (`create-fumadocs-app`) and on-demand component installation (`npx @fumadocs/cli add`).

Files live under `content/docs/`. Folder layouts generate URL slugs. Each directory uses a `meta.json` file to establish navigation titles, page ordering, separators, and root scopes.

---

## Sequential Procedure

### Step 1: Detect or Initialize Environment

Inspect the target project. Determine if Fumadocs is already installed or if initialization is needed.

- If scaffolding a new project: run `pnpm create fumadocs-app` and select Fumadocs MDX.
- If adding to an existing Next.js App Router project:
  1. Install packages: `npm install fumadocs-ui fumadocs-core fumadocs-mdx @types/mdx lucide-react`.
  2. Wrap Next.js config in `next.config.mjs` with `createMDX()`.
  3. Add Tailwind styles in `app/global.css`:
     ```css
     @import 'tailwindcss';
     @import 'fumadocs-ui/css/neutral.css';
     @import 'fumadocs-ui/css/preset.css';
     ```
  4. Wrap the root layout in `app/layout.tsx` with `<RootProvider>` from `fumadocs-ui/provider/next`.

**Completion Criterion**: Project builds without missing package errors, `createMDX` is active in `next.config.mjs`, and Fumadocs CSS presets load into the application stylesheet. Consult [references/setup-and-config.md](references/setup-and-config.md) for complete file templates.

---

### Step 2: Establish the Content Source

Configure the loader to parse documents from `content/docs`.

In `lib/source.ts`, instantiate the loader:

```ts title="lib/source.ts"
import { defineDocs } from 'fumadocs-mdx/macro';
import { loader } from 'fumadocs-core/source';

const docs = defineDocs({
  dir: 'content/docs',
});

export const source = loader({
  baseUrl: '/docs',
  source: docs.toFumadocsSource(),
});
```

When using `source.config.ts` instead of the macro, define collections in `source.config.ts` and import `docs` from `collections/server` in `lib/source.ts`.

**Completion Criterion**: Executing `source.getPageTree()` returns the hierarchy of content files, and `source.getPages()` returns all discoverable documentation pages.

---

### Step 3: Wire Layout and Route Handlers

Create documentation routes:

1. **Docs Layout (`app/docs/layout.tsx`)**:
   Wrap page children with `DocsLayout`, passing the page tree:
   ```tsx title="app/docs/layout.tsx"
   import { source } from '@/lib/source';
   import { DocsLayout } from 'fumadocs-ui/layouts/docs';
   import type { ReactNode } from 'react';

   export default function Layout({ children }: { children: ReactNode }) {
     return (
       <DocsLayout tree={source.getPageTree()} nav={{ title: 'Docs' }}>
         {children}
       </DocsLayout>
     );
   }
   ```

2. **Docs Dynamic Page (`app/docs/[[...slug]]/page.tsx`)**:
   Resolve slugs, render frontmatter headings, pass table of contents data, and register global MDX components:
   ```tsx title="app/docs/[[...slug]]/page.tsx"
   import { source } from '@/lib/source';
   import { DocsBody, DocsDescription, DocsPage, DocsTitle } from 'fumadocs-ui/layouts/docs/page';
   import { notFound } from 'next/navigation';
   import { getMDXComponents } from '@/components/mdx';
   import { createRelativeLink } from 'fumadocs-ui/mdx';

   interface PageProps {
     params: Promise<{ slug?: string[] }>;
   }

   export default async function Page({ params }: PageProps) {
     const { slug } = await params;
     const page = source.getPage(slug);
     if (!page) notFound();

     const MDX = page.data.body;

     return (
       <DocsPage toc={page.data.toc} full={page.data.full}>
         <DocsTitle>{page.data.title}</DocsTitle>
         <DocsDescription>{page.data.description}</DocsDescription>
         <DocsBody>
           <MDX components={getMDXComponents({ a: createRelativeLink(source, page) })} />
         </DocsBody>
       </DocsPage>
     );
   }

   export async function generateStaticParams() {
     return source.generateParams();
   }
   ```

3. **MDX Component Registry (`components/mdx.tsx`)**:
   Export `getMDXComponents()` combining `defaultMdxComponents` with interactive components.

**Completion Criterion**: Visiting `/docs` displays the root documentation page inside `DocsLayout` with a functional sidebar, header, and search trigger.

---

### Step 4: Structure Navigation with `meta.json`

Arrange files inside `content/docs/`. Place a `meta.json` file in every directory where ordering, section dividers, or custom folder titles are needed.

```json title="content/docs/meta.json"
{
  "title": "Documentation",
  "pages": [
    "index",
    "---Getting Started---",
    "quick-start",
    "installation",
    "---Features---",
    "components",
    "architecture",
    "...",
    "[GitHub Repo](https://github.com/my-org/my-project)"
  ]
}
```

Key Navigation Rules:
- Items in `pages` must match the file basename without `.mdx`.
- Prefix section dividers with triple hyphens: `"---Section Title---"`.
- Use `"..."` as a wildcard to capture remaining unlisted files in alphabetical order.
- Never list the same page URL more than once across the entire tree.
- Use `"root": true` for top-level product sections (rendered as navigation tabs).
- Use `"root": "version"` for multi-version documentation dropdowns.

**Completion Criterion**: Every `.mdx` file appears in the sidebar at its intended position, section dividers render between groups, and no console warnings report duplicate URLs. Consult [references/page-conventions.md](references/page-conventions.md) for advanced patterns.

---

### Step 5: Author Content with Interactive MDX

Write clear, structured MDX pages with YAML frontmatter:

```mdx
---
title: Working with Data
description: Learn how to query, transform, and cache datasets.
---
```

Select the right Fumadocs components for the content:
- **Alerts & Tips**: Use `<Callout title="..." type="info|warn|error|idea|success">`.
- **Navigation Links**: Use `<Cards>` with `<Card title="..." href="..." icon={<Icon />}>`.
- **Multi-Environment Instructions**: Use `<Tabs items={['npm', 'pnpm', 'bun']} id="package-manager">` with `<Tab value="...">`.
- **Step-by-Step Guides**: Use `<Steps>` and `<Step>`.
- **Directory Visualizations**: Use `<Files>`, `<Folder name="..." defaultOpen>`, and `<File name="...">`.
- **API & Configuration Tables**: Use `<TypeTable type={{ key: { type: 'string', description: '...' } }}>` or `<AutoTypeTable path="..." name="..." />`.
- **Collapsible FAQs**: Use `<Accordions>` with `<Accordion title="...">`.
- **Code Highlighting**: Use Shiki annotations (`// [!code highlight]`, `// [!code ++]`, `// [!code --]`, `// [!code focus]`, `// [!code word:token]`) and file titles (```` ```ts title="src/index.ts" ````).

**Completion Criterion**: MDX files render clean typography, codeblocks display syntax highlighting with accurate annotations, and interactive components respond to clicks without client hydration errors. Consult [references/components.md](references/components.md) and [references/markdown-and-code.md](references/markdown-and-code.md).

---

### Step 6: Configure Search and AI Endpoints

1. **Search Route**: Create `app/api/search/route.ts`:
   ```ts
   import { source } from '@/lib/source';
   import { createFromSource } from 'fumadocs-core/search/server';

   export const { GET } = createFromSource(source, { language: 'english' });
   ```

2. **AI Discovery Index (`llms.txt`)**: Create `app/llms.txt/route.ts`:
   ```ts
   import { source } from '@/lib/source';
   import { llms } from 'fumadocs-core/source';

   export const revalidate = false;
   export function GET(): Response {
     return new Response(llms(source).index(), {
       headers: { 'content-type': 'text/plain; charset=utf-8' },
     });
   }
   ```

3. **Full Content AI Export (`llms-full.txt`)**: Enable `includeProcessedMarkdown: true` in `source.config.ts` and create `app/llms-full.txt/route.ts`.

**Completion Criterion**: Pressing `Cmd+K` opens the search modal and returns search results from page content; fetching `/llms.txt` returns a clean plaintext summary of the docs tree. Consult [references/integrations.md](references/integrations.md).

---

## Quick Reference

### Frontmatter Fields

| Field | Type | Purpose |
| :--- | :--- | :--- |
| `title` | `string` | Main page heading (H1) and browser title. |
| `description` | `string` | Page subtitle and search snippet. |
| `icon` | `string` | Associated icon name in navigation. |
| `full` | `boolean` | When true, expands body width and hides table of contents. |

### Component Syntax Cheat Sheet

```mdx
<Callout title="Note" type="info">Note content</Callout>

<Cards>
  <Card title="Page Title" href="/docs/target">Description</Card>
</Cards>

<Tabs items={['Option A', 'Option B']} id="group-id">
  <Tab value="Option A">Content A</Tab>
  <Tab value="Option B">Content B</Tab>
</Tabs>

<Steps>
  <Step>### Step 1 Header</Step>
</Steps>

<Files>
  <Folder name="src" defaultOpen>
    <File name="index.ts" />
  </Folder>
</Files>

<Accordions>
  <Accordion title="Question?">Answer text</Accordion>
</Accordions>
```

---

## Disclosed References

Consult these detailed references for full signatures, complex setups, and edge cases:

- [references/components.md](references/components.md): Full component catalog with props, copy-paste snippets, and MDX registration patterns.
- [references/page-conventions.md](references/page-conventions.md): URL slug resolution, folder groupings, root tabs, version dropdowns, and full `meta.json` syntax.
- [references/setup-and-config.md](references/setup-and-config.md): Complete Next.js App Router manual setup, Tailwind CSS v4 styling, alternative layouts (`NotebookLayout`, `FluxLayout`, `GlassLayout`), and shared navigation options.
- [references/markdown-and-code.md](references/markdown-and-code.md): Shiki annotations, code tabs, line numbers, Twoslash type inspection, KaTeX math, Mermaid diagrams, and `<include>` tags.
- [references/integrations.md](references/integrations.md): Search backends (ZBSearch, Algolia, FlexSearch), OpenAPI generation (`fumadocs-openapi`), `llms.txt` routes, i18n, and dynamic OG images.
