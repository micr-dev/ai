# Setup and Configuration

Step-by-step setup guides for integrating Fumadocs into Next.js App Router applications.

## Automated Scaffolding

To create a new Fumadocs application from scratch:

```bash
pnpm create fumadocs-app
# or
npm create fumadocs-app
```

Follow the interactive prompts to pick your framework, content source (Fumadocs MDX is recommended), and package manager.

---

## Manual Next.js App Router Setup

### 1. Install Dependencies

```bash
npm install fumadocs-ui fumadocs-core fumadocs-mdx @types/mdx lucide-react
```

### 2. Configure Next.js

Wrap your Next.js config with `createMDX()` in `next.config.mjs`:

```js title="next.config.mjs"
import { createMDX } from 'fumadocs-mdx/next';

/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,
};

const withMDX = createMDX();
export default withMDX(config);
```

### 3. Setup Tailwind CSS Styles

In `app/global.css`, include Fumadocs themes and presets after Tailwind CSS:

```css title="app/global.css"
@import 'tailwindcss';
@import 'fumadocs-ui/css/neutral.css';
@import 'fumadocs-ui/css/preset.css';
```

Available color palettes to substitute for `neutral.css`:
- `fumadocs-ui/css/neutral.css`
- `fumadocs-ui/css/slate.css`
- `fumadocs-ui/css/zinc.css`
- `fumadocs-ui/css/black.css`

### 4. Root Application Provider

Wrap your application in `RootProvider` inside `app/layout.tsx`:

```tsx title="app/layout.tsx"
import { RootProvider } from 'fumadocs-ui/provider/next';
import './global.css';
import type { ReactNode } from 'react';

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="flex flex-col min-h-screen">
        <RootProvider>{children}</RootProvider>
      </body>
    </html>
  );
}
```

### 5. Content Source & Loader

You can configure content using the Macro API in `lib/source.ts`:

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

Alternatively, use `source.config.ts` for build-time compilation:

```ts title="source.config.ts"
import { defineDocs, defineConfig } from 'fumadocs-mdx/config';

export const docs = defineDocs({
  dir: 'content/docs',
});

export default defineConfig();
```

With `source.config.ts`, `lib/source.ts` imports the compiled output:

```ts title="lib/source.ts"
import { docs } from 'collections/server';
import { loader } from 'fumadocs-core/source';

export const source = loader({
  baseUrl: '/docs',
  source: docs.toFumadocsSource(),
});
```

### 6. Shared Layout Configuration

Define shared navigation titles, links, and GitHub repository links in `lib/layout.shared.tsx`:

```tsx title="lib/layout.shared.tsx"
import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';

export function baseOptions(): BaseLayoutProps {
  return {
    nav: {
      title: 'Documentation',
    },
    links: [
      {
        text: 'Documentation',
        url: '/docs',
        active: 'nested-url',
      },
      {
        text: 'Blog',
        url: '/blog',
      },
    ],
    githubUrl: 'https://github.com/my-org/my-project',
  };
}
```

### 7. Documentation Layout

In `app/docs/layout.tsx`, pass your page tree to `DocsLayout`:

```tsx title="app/docs/layout.tsx"
import { source } from '@/lib/source';
import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import { baseOptions } from '@/lib/layout.shared';
import type { ReactNode } from 'react';

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <DocsLayout tree={source.getPageTree()} {...baseOptions()}>
      {children}
    </DocsLayout>
  );
}
```

### 8. Documentation Dynamic Route

Create `app/docs/[[...slug]]/page.tsx` to resolve slugs, render MDX, and generate static parameters:

```tsx title="app/docs/[[...slug]]/page.tsx"
import { source } from '@/lib/source';
import {
  DocsBody,
  DocsDescription,
  DocsPage,
  DocsTitle,
} from 'fumadocs-ui/layouts/docs/page';
import { notFound } from 'next/navigation';
import { getMDXComponents } from '@/components/mdx';
import { createRelativeLink } from 'fumadocs-ui/mdx';
import type { Metadata } from 'next';

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
        <MDX
          components={getMDXComponents({
            a: createRelativeLink(source, page),
          })}
        />
      </DocsBody>
    </DocsPage>
  );
}

export async function generateStaticParams() {
  return source.generateParams();
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const page = source.getPage(slug);
  if (!page) notFound();

  return {
    title: page.data.title,
    description: page.data.description,
  };
}
```

---

## Alternative Layouts

Fumadocs UI provides several alternative layouts:

1. **DocsLayout** (`fumadocs-ui/layouts/docs`): The standard full-featured layout with a sidebar, search dialog, and right-hand table of contents.
2. **NotebookLayout** (`fumadocs-ui/layouts/notebook`): Compact design tailored for tutorials, API references, or dense documentation.
3. **FluxLayout** (`fumadocs-ui/layouts/flux`): Minimalist layout featuring an edge-to-edge reading area and streamlined navigation.
4. **GlassLayout** (`fumadocs-ui/layouts/glass`): Translucent floating surfaces with blur effects for modern web apps.
5. **HomeLayout** (`fumadocs-ui/layouts/home-layout`): Navbar-only layout suited for marketing homepages, blogs, or showcase pages.
