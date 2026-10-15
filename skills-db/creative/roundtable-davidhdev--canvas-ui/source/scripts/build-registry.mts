import fs from "node:fs";
import path from "node:path";

import { getRegistryItem, REGISTRY_ITEMS } from "../src/lib/registry.ts";

const OUT_DIR = path.join(process.cwd(), "public/r");

fs.rmSync(OUT_DIR, { recursive: true, force: true });
fs.mkdirSync(OUT_DIR, { recursive: true });

const items = REGISTRY_ITEMS.map((name) => {
  const item = getRegistryItem(name);
  if (!item) throw new Error(`Unknown registry item: ${name}`);
  fs.writeFileSync(
    path.join(OUT_DIR, `${name}.json`),
    JSON.stringify(item, null, 2),
  );
  return item;
});

const registry = {
  $schema: "https://ui.shadcn.com/schema/registry.json",
  name: "canvasui",
  homepage: "https://canvasui.dev",
  items: items.map((item) => ({
    name: item.name,
    type: item.type,
    title: item.title,
    description: item.description,
    dependencies: item.dependencies,
    devDependencies: item.devDependencies,
    files: item.files.map((file) => ({
      path: file.path,
      type: file.type,
      target: file.target,
    })),
  })),
};
fs.writeFileSync(
  path.join(OUT_DIR, "registry.json"),
  JSON.stringify(registry, null, 2),
);

console.log(
  `Built ${items.length} registry items + index into public/r/:`,
  items.map((item) => item.name).join(", "),
);
