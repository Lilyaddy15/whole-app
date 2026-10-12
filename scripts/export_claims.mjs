// Export every "Real or hype?" claim from data/issues.js for the Evidence Agent.
//   node scripts/export_claims.mjs          -> agents/evidence_check/claims.json
import fs from 'node:fs';
import vm from 'node:vm';

const ctx = { window: {} };
vm.runInNewContext(fs.readFileSync('data/issues.js', 'utf8'), ctx);
const { TOPICS } = ctx.window.WHOLE_DATA;

const claims = Object.entries(TOPICS).flatMap(([topic, t]) =>
  t.hype.map(h => ({ id: h.id, topic: t.name, trend: h.t, says: h.says.replace(/[“”]/g, '') })));
fs.writeFileSync('agents/evidence_check/claims.json', JSON.stringify(claims, null, 2) + '\n');
console.log(`Wrote ${claims.length} claims to agents/evidence_check/claims.json`);
