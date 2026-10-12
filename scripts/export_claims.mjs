// Export every "Real or hype?" claim from data/issues.js for the Evidence Agent.
//   node scripts/export_claims.mjs          -> agents/evidence_check/claims.json
//   node scripts/export_claims.mjs --seed   -> also writes a SAMPLE data/evidence.json
import fs from 'node:fs';
import vm from 'node:vm';

const ctx = { window: {} };
vm.runInNewContext(fs.readFileSync('data/issues.js', 'utf8'), ctx);
const { TOPICS } = ctx.window.WHOLE_DATA;

const claims = Object.entries(TOPICS).flatMap(([topic, t]) =>
  t.hype.map(h => ({ id: h.id, topic: t.name, trend: h.t, says: h.says.replace(/[“”]/g, '') })));
fs.writeFileSync('agents/evidence_check/claims.json', JSON.stringify(claims, null, 2) + '\n');
console.log(`Wrote ${claims.length} claims to agents/evidence_check/claims.json`);

if (process.argv.includes('--seed')) {
  // Placeholder output in the agent's format, so the app has something to show
  // before the agent has run. Sources are left empty on purpose: only a live run fills them.
  const types = {
    real: [['Systematic review', 'Clinical guideline'], 'high'],
    mixed: [['Randomized trial', 'Systematic review'], 'medium'],
    early: [['Small trials'], 'low'],
    hype: [['Systematic review', 'Expert body'], 'medium'],
  };
  const out = { generated_by: 'scripts/export_claims.mjs --seed', sample: true, claims: {} };
  for (const t of Object.values(TOPICS)) for (const h of t.hype) {
    const [source_types, confidence] = types[h.v];
    out.claims[h.id] = {
      verdict: h.v, evidence: h.ev, confidence, caveats: '', sources: [], source_types,
      checked_at: '2026-10-09', model: 'claude-opus-5-5', sample: true,
      review: { status: 'approved', editor: 'Sample editor' },
    };
  }
  fs.writeFileSync('data/evidence.json', JSON.stringify(out, null, 2) + '\n');
  console.log(`Wrote sample data/evidence.json (${Object.keys(out.claims).length} claims)`);
}
