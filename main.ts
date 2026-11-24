// main.ts — entry program for the make.fun news-image-20261124 bounty.
// Node 22, standard library only. The front-page image (entry.png, drawn by
// draw_frontpage.py) is bundled next to this file; the harness contract is
// to place that exact image at <output>/entry.png. The operation is a pure
// file copy, so it is deterministic: same bytes in, same bytes out, every
// run, with no clock, no network and no randomness involved.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const sourceDir = dirname(fileURLToPath(import.meta.url));
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = join(sourceDir, "entry.png");
const target = join(outputDir, "entry.png");

if (!existsSync(source)) {
  throw new Error(`bundled entry image missing: ${source}`);
}
mkdirSync(outputDir, { recursive: true });
copyFileSync(source, target);
console.log(`entry.png written to ${target}`);
