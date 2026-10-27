# Page Conventions & Page Tree

Fumadocs generates page slugs and sidebar navigation trees from your content directory using the `loader()` API.

## File to Route Mapping

Slugs map directly from file paths relative to your docs content folder:

| File Path | Slug Path | Route URL |
| :--- | :--- | :--- |
| `content/docs/index.mdx` | `[]` | `/docs` |
| `content/docs/quick-start.mdx` | `['quick-start']` | `/docs/quick-start` |
| `content/docs/guide/install.mdx` | `['guide', 'install']` | `/docs/guide/install` |
| `content/docs/guide/index.mdx` | `['guide']` | `/docs/guide` |

### Route Groups

Enclose a folder name in parentheses `(group)` to organize files on disk without altering the generated URL slugs:

| File Path | Generated Slug | Route URL |
| :--- | :--- | :--- |
| `content/docs/(advanced)/caching.mdx` | `['caching']` | `/docs/caching` |
| `content/docs/(getting-started)/setup.mdx` | `['setup']` | `/docs/setup` |

---

## Frontmatter Schema

Each `.mdx` or `.md` file begins with YAML frontmatter:

```mdx
---
title: Quick Start
description: Get started with Fumadocs in under five minutes.
icon: RocketIcon
full: false
---
```

Standard Frontmatter Fields:
- `title` (`string`, required): Page title rendered as the main heading in Fumadocs UI and document `<title>`.
- `description` (`string`, optional): Page summary displayed beneath the title and in search metadata.
- `icon` (`string`, optional): Name of the icon associated with the page in navigation trees.
- `full` (`boolean`, optional): When `true`, expands the content width to span the full container and omits the right-hand table of contents.

### Extending the Schema with Zod

In `source.config.ts`, extend the standard schema to validate custom metadata properties:

```ts title="source.config.ts"
import { defineDocs } from 'fumadocs-mdx/config';
import { pageSchema, metaSchema } from 'fumadocs-core/source/schema';
import { z } from 'zod';

export const docs = defineDocs({
  docs: {
    schema: pageSchema.extend({
      author: z.string().optional(),
      category: z.enum(['guide', 'reference', 'tutorial']).default('guide'),
      draft: z.boolean().default(false),
    }),
  },
  meta: {
    schema: metaSchema.extend({
      badge: z.string().optional(),
    }),
  },
});
```

---

## The `meta.json` Specification

Place `meta.json` in any directory to control folder titles, visibility, page ordering, separators, and external links.

```json title="content/docs/meta.json"
{
  "title": "Documentation",
  "icon": "BookIcon",
  "defaultOpen": true,
  "collapsible": true,
  "pages": [
    "index",
    "---Getting Started---",
    "quick-start",
    "installation",
    "---Guides---",
    "advanced",
    "...folder",
    "...",
    "!secret-page",
    "[GitHub](https://github.com/example/repo)",
    "external:[Discord Community](https://discord.gg/example)"
  ]
}
```

### Configuration Keys

| Key | Type | Description |
| :--- | :--- | :--- |
| `title` | `string` | Display label for this folder in the navigation tree. |
| `icon` | `string` | Icon name rendered next to the title. |
| `defaultOpen` | `boolean` | Whether the folder is expanded on first render (default: `false`). |
| `collapsible` | `boolean` | Whether users can collapse or expand this group (default: `true`). |
| `root` | `boolean \| string` | Marks folder as a root scope. See Root Folders section below. |
| `pagesIndex` | `string` | Target file or link when clicking the folder header itself. |
| `pages` | `string[]` | Ordered list of child pages, separators, links, and wildcards. |

### `pages` Array Item Types

1. **Page Reference**: Matches the slug without file extension (e.g. `"quick-start"`).
2. **Separator**: Creates a labeled divider in the sidebar:
   - Plain separator: `"---Section Label---"`
   - Separator with icon: `"---[FolderIcon]Section Label---"`
3. **Custom Links**: Embeds links inside the sidebar:
   - Internal or relative: `"[Changelog](/changelog)"`
   - External with explicit target: `"external:[Status Page](https://status.example.com)"`
   - Link with icon: `"[GithubIcon][GitHub](https://github.com/my-org/my-repo)"`
4. **Rest Operator (`...`)**: Appends all unmentioned pages in alphabetical order.
5. **Reversed Rest (`z...a`)**: Appends all unmentioned pages in reverse alphabetical order.
6. **Folder Extraction (`...folder-name`)**: Extracts all pages from a subfolder into the current tree level without folder nesting.
7. **Exclusion (`!page-name`)**: Excludes a page from the wildcard `...` catch-all.

> Note: The same page URL must never appear more than once in the entire page tree. Duplicated entries will cause routing collisions.

---

## Root Folders & Multi-Section Docs

### Root Tabs (`"root": true`)

When a top-level folder contains `"root": true`, Fumadocs UI isolates that section into its own root scope. The UI presents root folders as top-level layout tabs:

```
content/docs/
├── core/
│   ├── meta.json  -> { "title": "Core", "root": true }
│   └── index.mdx
└── ui/
    ├── meta.json  -> { "title": "UI Library", "root": true }
    └── index.mdx
```

When viewing pages inside `core`, only `core` items appear in the sidebar navigation.

### Versioning (`"root": "version"`)

Root folders of the same string type act as interchangeable versions:

```
content/docs/
├── v1/
│   ├── meta.json  -> { "title": "v1.0", "root": "version" }
│   └── guide.mdx
└── v2/
    ├── meta.json  -> { "title": "v2.0", "root": "version" }
    └── guide.mdx
```

Fumadocs UI automatically renders a version selector dropdown in the navigation header. Switching versions projects the user to the matching relative page in the chosen version.
