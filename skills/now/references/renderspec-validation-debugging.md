# RenderSpec validation and debugging

Use this when `lev.now` rendering fails with a terse renderer/runtime error instead of a helpful schema message.

## Symptom

A render command such as:

```bash
npx tsx plugins/now/src/cli.ts ~/.agents/levnow/{slug}.json --output ~/.agents/levnow/{slug}.html
```

may fail with a generic message such as:

```text
Error: Cannot read properties of undefined (reading 'flatMap')
```

Do not treat this as a renderer bug first. In practice it can mean the JSON shape passed the agent's eyeball check but violates the `RenderSpecSchema` union constraints.

## Fast diagnosis

Create a temporary validator that imports the local schema directly:

```ts
// /tmp/validate-now-spec.ts
import fs from 'node:fs';
import { RenderSpecSchema } from '/opt/data/lev/plugins/now/src/contracts/schema.ts';

const path = process.argv[2] ?? '/opt/data/home/.agents/levnow/spec.json';
const spec = JSON.parse(fs.readFileSync(path, 'utf8'));
const result = RenderSpecSchema.safeParse(spec);

if (!result.success) {
  console.error(JSON.stringify(result.error.format(), null, 2));
  process.exit(1);
}
console.log('valid');
```

Run it from the Lev checkout:

```bash
npx tsx /tmp/validate-now-spec.ts ~/.agents/levnow/{slug}.json
```

Then patch the JSON and rerender.

## Common invalid-spec causes

- Hero variants are constrained. Use schema-supported variants such as `centered` or `editorial`; do not invent variants.
- Hero props are constrained. Remove ad hoc keys such as `category` or `meta` unless the schema supports them.
- Section props are constrained. Do not add convenience keys such as `eyebrow` unless the schema explicitly supports them; fold them into `title`/`subtitle` or use a child text/card.
- `code-block` uses `props.content`, not `props.code`; keep `language`, `filename`, and `showLineNumbers` as optional metadata.
- `timeline` item statuses are limited to `completed`, `in-progress`, and `upcoming`; do not use `current`.
- Section and element variants are discriminated unions; one wrong `variant` can cause a large union error.
- The CLI takes the spec path directly. Use `npx tsx plugins/now/src/cli.ts {spec.json} --output {page.html}`. Do not insert a `render` subcommand at the CLI layer; that will be read as the spec path and can surface as `Error: invalid JSON`.

## Recovery loop

1. Validate the JSON against `RenderSpecSchema` before rerendering.
2. Patch the smallest invalid field(s).
3. Re-run the validator until it prints `valid`.
4. Render again.
5. Run visual QA before publishing; if built-in screenshot QA cannot run, use the browser/vision fallback in the main skill.
