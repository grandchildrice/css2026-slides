// 配信用の dist/ を組み立てる。
//
//     node build_site.mjs
//
// `wrangler deploy` が実行前に自動で呼ぶ（wrangler.jsonc の build.command）ので、
// 手で走らせる必要は普通はない。リポジトリ直下には発表準備の原稿（materials/）や
// 生成・検証スクリプトも置いてあるため、配信するのは描画に必要なファイルだけに絞る。
// index.html と slides.md が参照する figs/ の資産を実際に走査して集めるので、
// 図を足しても本スクリプトの変更は要らない。出典の記録（*-sources.json・
// ライセンス）は、図と離れないよう常に同梱する。
import { cp, mkdir, readFile, rm } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const dist = join(root, "dist");
const pages = ["index.html", "slides.md"];
const provenance = [
  "figs/logo-sources.json",
  "figs/illustration-sources.json",
  "figs/ethereum-illustration-LICENSE.txt",
];

const referenced = new Set(provenance);
for (const page of pages) {
  const text = await readFile(join(root, page), "utf8");
  for (const match of text.matchAll(/figs\/[A-Za-z0-9._-]+/g)) referenced.add(match[0]);
}

await rm(dist, { recursive: true, force: true });
const files = [...new Set([...pages, ...referenced])].sort();
for (const name of files) {
  await mkdir(dirname(join(dist, name)), { recursive: true });
  await cp(join(root, name), join(dist, name));
}
console.log(`${files.length} ファイルを ${dist} に配置した`);
for (const name of files) console.log(`  ${name}`);
