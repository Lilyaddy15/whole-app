// Publish Editor Agent drafts into the app's content file.
//   node scripts/apply_drafts.mjs nutrition [beauty ...]
// Only drafts with status "ready" (fact-check passed) are applied. Fields the
// Editor Agent doesn't write (products, brands, hype claims, colors) are kept.
import fs from 'node:fs';
import vm from 'node:vm';

const topics = process.argv.slice(2);
if (!topics.length) { console.error('Usage: node scripts/apply_drafts.mjs <topic> [...]'); process.exit(1); }

const ctx = { window: {} };
vm.runInNewContext(fs.readFileSync('data/issues.js', 'utf8'), ctx);
const data = ctx.window.WHOLE_DATA;

for (const t of topics) {
  const path = `data/drafts/${t}.json`;
  if (!fs.existsSync(path)) { console.error(`No draft at ${path}`); continue; }
  const draft = JSON.parse(fs.readFileSync(path, 'utf8'));
  if (draft.status !== 'ready') { console.error(`${t}: draft status is "${draft.status}", not applied. Read its fact_check log.`); continue; }
  if (!data.TOPICS[t]) { console.error(`${t}: no such topic in data/issues.js`); continue; }
  const { editor_note, ...copy } = draft.issue;
  Object.assign(data.TOPICS[t], copy);
  console.log(`${t}: applied (${editor_note})`);
}

fs.writeFileSync('data/issues.js',
  '/* WHOLE issue content. Edited by the WHOLE Editor Agent from Anthropologic pipeline output. */\n' +
  'window.WHOLE_DATA = ' + JSON.stringify(data, null, 2) + ';\n');
