# Integrations & Advanced Features

Guide for search engines, OpenAPI schemas, AI discovery files, internationalization, and versioning in Fumadocs.

## Full-Text Document Search

### Built-in Search (ZBSearch / Orama)

Fumadocs includes built-in full-text search powered by ZBSearch. Create a search route handler at `app/api/search/route.ts`:

```ts title="app/api/search/route.ts"
import { source } from '@/lib/source';
import { createFromSource } from 'fumadocs-core/search/server';

export const { GET } = createFromSource(source, {
  language: 'english',
});
```

The default search dialog in `DocsLayout` automatically connects to `/api/search`.

### Third-Party Search Providers

For high-scale or external search indexes, Fumadocs supports:
- **Algolia Search**: `fumadocs-core/search/algolia` with instant indexing scripts.
- **FlexSearch**: Client-side lightweight search for smaller documentation sets.
- **Typesense**: Open-source typo-tolerant search engine adapter.
- **Mixedbread**: Vector search integration for semantic search queries.

---

## AI & LLM Discovery (`llms.txt`)

Provide machine-readable documentation indexes for AI agents and LLM tools.

### 1. Enable Processed Markdown

In `source.config.ts`, configure `postprocess` to expose parsed markdown:

```ts title="source.config.ts"
import { defineDocs, defineConfig } from 'fumadocs-mdx/config';

export const docs = defineDocs({
  dir: 'content/docs',
  docs: {
    postprocess: {
      includeProcessedMarkdown: true,
    },
  },
});

export default defineConfig();
```

### 2. Standard `llms.txt` Route

Create `app/llms.txt/route.ts` to return an index of all available documentation pages:

```ts title="app/llms.txt/route.ts"
import { source } from '@/lib/source';
import { llms } from 'fumadocs-core/source';

export const revalidate = false;

export function GET(): Response {
  return new Response(llms(source).index(), {
    headers: {
      'content-type': 'text/plain; charset=utf-8',
    },
  });
}
```

### 3. Full Content `llms-full.txt` Route

Create `app/llms-full.txt/route.ts` to serve the full text of all pages in a single context file:

```ts title="app/llms-full.txt/route.ts"
import { source } from '@/lib/source';

export const revalidate = false;

export async function GET(): Promise<Response> {
  const pages = source.getPages();
  const documents = await Promise.all(
    pages.map(async (page) => {
      const processed = await page.data.getText('processed');
      return `# ${page.data.title} (${page.url})\n\n${processed}`;
    })
  );

  return new Response(documents.join('\n\n---\n\n'), {
    headers: {
      'content-type': 'text/plain; charset=utf-8',
    },
  });
}
```

---

## OpenAPI & Swagger Integration

Generate interactive API reference pages directly from OpenAPI v3 schemas.

### 1. Installation

```bash
npm install fumadocs-openapi
```

### 2. Configure OpenAPI Instance

```ts title="lib/openapi.ts"
import { createOpenAPI } from 'fumadocs-openapi/server';

export const openapi = createOpenAPI({
  input: ['./openapi.yaml'],
});
```

### 3. Generate Documentation Pages

Generate MDX files from endpoints:

```ts title="scripts/generate-docs.ts"
import { generateFiles } from 'fumadocs-openapi';
import { openapi } from '@/lib/openapi';

await generateFiles({
  input: openapi,
  output: './content/docs/api',
  groupBy: 'tag',
});
```

Run this generator script during your prebuild step (`"prebuild": "tsx scripts/generate-docs.ts"`).

### 4. Interactive API Playground Component

Render interactive request runners, response tabs, and schema explorers:

```tsx title="components/api-page.tsx"
'use client';
import { createOpenAPIPage } from 'fumadocs-openapi/ui';

export const OpenAPIPage = createOpenAPIPage();
```

Use `<OpenAPIPage />` in your MDX route to give users a try-it-out playground for endpoints.

---

## Internationalization (i18n)

Support multiple language locales with automatic routing and language switchers.

### 1. Define i18n Configuration

```ts title="lib/i18n.ts"
import { defineI18n } from 'fumadocs-core/i18n';

export const i18n = defineI18n({
  languages: ['en', 'ja', 'es'],
  defaultLanguage: 'en',
});
```

### 2. Multi-Language File Structure

Name files using language code suffixes:
```
content/docs/
├── index.mdx       (default language, e.g. English)
├── index.ja.mdx    (Japanese translation)
└── index.es.mdx    (Spanish translation)
```

Fumadocs UI detects the available translations for each page and adds a language selector in the navbar.

---

## Multi-Version Documentation

Maintain simultaneous documentation sets for different software versions (e.g. `v1` and `v2`).

Organize content folders and mark their `meta.json` with `"root": "version"`:

```
content/docs/
├── v1/
│   ├── meta.json  -> { "title": "1.0", "root": "version" }
│   ├── index.mdx
│   └── guide.mdx
└── v2/
    ├── meta.json  -> { "title": "2.0", "root": "version" }
    ├── index.mdx
    └── guide.mdx
```

Fumadocs UI automatically renders a version selector dropdown in the navigation header. When a user switches versions, Fumadocs maps them directly to the corresponding page in the newly selected version.

---

## Dynamic OpenGraph (OG) Images

Generate dynamic social preview images for documentation pages using Next.js ImageResponse and `@fumadocs/ui/og`:

```tsx title="app/docs/[[...slug]]/og/route.ts"
import { source } from '@/lib/source';
import { generateOGImage } from 'fumadocs-ui/og';
import { notFound } from 'next/navigation';

export function GET(
  request: Request,
  { params }: { params: Promise<{ slug?: string[] }> }
) {
  const { slug } = await params;
  const page = source.getPage(slug);
  if (!page) notFound();

  return generateOGImage({
    title: page.data.title,
    description: page.data.description,
    site: 'My Project Docs',
  });
}
```
