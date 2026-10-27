# Fumadocs UI Components

Interactive and presentational components provided by `fumadocs-ui`.

## Global MDX Registration

Register components in `components/mdx.tsx` (or `mdx-components.tsx`) so they are available across all MDX files without per-file imports.

```tsx title="components/mdx.tsx"
import defaultMdxComponents from 'fumadocs-ui/mdx';
import * as TabsComponents from 'fumadocs-ui/components/tabs';
import * as StepsComponents from 'fumadocs-ui/components/steps';
import * as FilesComponents from 'fumadocs-ui/components/files';
import * as AccordionComponents from 'fumadocs-ui/components/accordion';
import * as TypeTableComponents from 'fumadocs-ui/components/type-table';
import { ImageZoom } from 'fumadocs-ui/components/image-zoom';
import { Banner } from 'fumadocs-ui/components/banner';
import { InlineTOC } from 'fumadocs-ui/components/inline-toc';
import type { MDXComponents } from 'mdx/types';

export function getMDXComponents(components?: MDXComponents): MDXComponents {
  return {
    ...defaultMdxComponents,
    ...TabsComponents,
    ...StepsComponents,
    ...FilesComponents,
    ...AccordionComponents,
    ...TypeTableComponents,
    ImageZoom,
    Banner,
    InlineTOC,
    ...components,
  };
}

export const useMDXComponents = getMDXComponents;
```

---

## Component Catalog

### 1. Callout

Highlights important notes, warnings, errors, or tips.

```mdx
<Callout title="Heads Up" type="info">
  This is an informative callout.
</Callout>

<Callout title="Warning" type="warn">
  Proceed with caution when deleting keys.
</Callout>

<Callout title="Error" type="error">
  This configuration will cause build failures.
</Callout>

<Callout title="Tip" type="idea">
  Use persistent tabs to remember user preferences.
</Callout>

<Callout title="Success" type="success">
  Deployment completed successfully.
</Callout>
```

Props:
- `title` (optional `string`): Callout header text.
- `type` (optional `"info" | "warn" | "error" | "idea" | "success"`, default: `"info"`).
- `icon` (optional `ReactNode`): Custom leading icon.

---

### 2. Cards and Card

Displays link grids or featured documentation entry points.

```mdx
import { CpuIcon, ShieldIcon } from 'lucide-react';

<Cards>
  <Card
    icon={<CpuIcon />}
    title="Architecture"
    href="/docs/architecture"
  >
    Learn about our core runtime engine and data flow.
  </Card>
  <Card
    icon={<ShieldIcon />}
    title="Security"
    href="/docs/security"
  >
    Review authentication policies and token lifetimes.
  </Card>
</Cards>
```

Props for `<Card>`:
- `title` (`string`, required): Card title.
- `href` (optional `string`): Target route or external URL. External links automatically receive secure rel attributes.
- `icon` (optional `ReactNode`): Icon rendered beside the title.
- `children` (optional `ReactNode`): Body description text.

---

### 3. Tabs and Tab

Displays multi-variant content such as package managers or languages.

```mdx
<Tabs items={['npm', 'pnpm', 'bun']} id="package-manager">
  <Tab value="npm">
    ```bash
    npm install fumadocs-ui
    ```
  </Tab>
  <Tab value="pnpm">
    ```bash
    pnpm add fumadocs-ui
    ```
  </Tab>
  <Tab value="bun">
    ```bash
    bun add fumadocs-ui
    ```
  </Tab>
</Tabs>
```

Props for `<Tabs>`:
- `items` (`string[]`, required): List of tab labels.
- `id` (optional `string`): Persistence key stored in localStorage. All tabs sharing the same `id` stay synchronized across pages.
- `defaultIndex` (optional `number`): Initial tab index.

Props for `<Tab>`:
- `value` (`string`, required): Label matching one entry from parent `items`.

---

### 4. Steps and Step

Formats sequential setup instructions with numeric indicator styling.

```mdx
<Steps>
  <Step>
    ### Install Dependencies
    Run the package manager install command.
  </Step>
  <Step>
    ### Configure Source
    Add `source.config.ts` to the project root.
  </Step>
  <Step>
    ### Start Dev Server
    Execute `npm run dev` to preview pages.
  </Step>
</Steps>
```

Fumadocs also supports automatic steps via markdown headings when `remark-steps` is enabled:
```md
### Installation [step]
Run the install command.

### Verification [step]
Run the test command.
```

---

### 5. Accordion and Accordions

Collapsible sections for FAQs, deep technical details, or collapsible references.

```mdx
<Accordions type="single">
  <Accordion title="Can I use Fumadocs without Next.js?">
    Yes. Fumadocs supports React Router, TanStack Start, Astro, and Waku.
  </Accordion>
  <Accordion title="Does it support Tailwind CSS v4?">
    Yes. Fumadocs UI is built for Tailwind CSS v4.
  </Accordion>
</Accordions>
```

Props for `<Accordions>`:
- `type` (`"single" | "multiple"`, default: `"single"`): Allow one or multiple panels open simultaneously.

Props for `<Accordion>`:
- `title` (`string`, required): Header label.
- `id` (optional `string`): Unique anchor identifier.
- `defaultOpen` (optional `boolean`): Whether initially expanded.

---

### 6. Files, Folder, and File

Visualizes project directory structures and file organization.

```mdx
<Files>
  <Folder name="src" defaultOpen>
    <Folder name="app" defaultOpen>
      <Folder name="docs" defaultOpen>
        <File name="layout.tsx" />
        <File name="page.tsx" />
      </Folder>
    </Folder>
    <Folder name="content">
      <File name="index.mdx" />
      <File name="meta.json" />
    </Folder>
  </Folder>
  <File name="package.json" />
</Files>
```

Props:
- `<Folder name="string" defaultOpen={boolean} disabled={boolean}>`
- `<File name="string" icon={ReactNode}>`

---

### 7. TypeTable and AutoTypeTable

Renders type definitions and property tables cleanly.

```mdx
<TypeTable
  type={{
    endpoint: {
      type: 'string',
      description: 'The target API base endpoint.',
      default: '"https://api.example.com"',
    },
    timeout: {
      type: 'number',
      description: 'Request timeout in milliseconds.',
      default: '5000',
    },
    retries: {
      type: 'number',
      description: 'Total retry attempts on network error.',
      default: '3',
    },
  }}
/>
```

Fields for each property:
- `type` (`string`): TypeScript type expression.
- `description` (optional `string`): Documentation for the field.
- `default` (optional `string`): Default value fallback.
- `required` (optional `boolean`): Indicates whether the property is required.

Using `<AutoTypeTable>` to parse types directly from TypeScript source:
```mdx
<AutoTypeTable path="./types/config.ts" name="ClientOptions" />
```

---

### 8. ImageZoom

Enables medium-style click-to-zoom on images.

```mdx
import { ImageZoom } from 'fumadocs-ui/components/image-zoom';

<ImageZoom
  src="/architecture-diagram.png"
  alt="System architecture diagram"
  width={1200}
  height={600}
/>
```

When registered in `mdx-components.tsx` under the `img` key, all markdown images `![alt](url)` gain zoom capability automatically.

---

### 9. Banner

Displays a dismissible notification banner across docs pages.

```mdx
<Banner id="v2-release" variant="rainbow">
  Version 2.0 has been released! Check out the migration guide.
</Banner>
```

Props:
- `id` (`string`, required): Persistent ID stored in localStorage when dismissed.
- `variant` (`"rainbow" | "normal"`, default: `"normal"`).

---

### 10. InlineTOC

Embeds a table of contents directly inside page content instead of only in the sidebar.

```mdx
<InlineTOC items={toc} defaultOpen />
```

Props:
- `items` (`TOCItemType[]`, required): Extracted table of contents data from frontmatter or loader.
- `defaultOpen` (optional `boolean`): Whether expanded by default.

---

### 11. DynamicCodeBlock

Highlights code dynamically on the client side at runtime.

```tsx
import { DynamicCodeBlock } from 'fumadocs-ui/components/dynamic-codeblock';

<DynamicCodeBlock
  lang="json"
  code={JSON.stringify({ status: 'ok', timestamp: Date.now() }, null, 2)}
/>
```

Props:
- `lang` (`string`): Language identifier for Shiki.
- `code` (`string`): Source code string to highlight.
