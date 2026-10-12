/* WHOLE daily edition, follow updates and search examples.
   SAMPLE content: shows what these screens will look like once the
   Anthropologic pipelines are connected. Real or hype claims link to the
   real, verified verdicts in data/evidence.json. */
(function(){

const EDITION = {
  date: 'Monday, October 12',
  // Shown in order; stories for topics the reader hasn't picked are skipped.
  stories: [
    {kind:'moved', topic:'nutrition', kicker:'What moved', title:'Protein in everything just peaked',
     body:'Posts about protein-spiked snacks fell for the fourth month in a row. Fiber is filling the gap, and “30 grams a day” is now the number people share.',
     stat:'−18%', statLabel:'protein-snack posts vs. last month', open:'issue:nutrition:life', follow:'trend:nutrition:Protein in everything'},
    {kind:'game', topic:'beauty', claim:'beauty-beef-tallow-moisturizer'},
    {kind:'asking', topic:'sleep', kicker:'Asking, not posting', title:'Why do I wake up at 3am?', mult:'3.3×',
     body:'Searched more than three times as often as it’s posted. Stress, alcohol and hormone shifts come up most in the conversation.', open:'issue:sleep:asking'},
    {kind:'study', topic:'exercise', kicker:'New in the research', title:'Creatine helps women get stronger, gently',
     body:'A 2026 review of seven trials in women after menopause found small gains in strength and lean mass when creatine was paired with strength training, and no sign of harm.',
     claim:'exercise-creatine-for-women', open:'issue:exercise:hype'},
    {kind:'who', topic:'beauty', kicker:'Who’s talking', title:'Meet the Early Peri',
     quote:'Nobody told me my skin would change at 38.', body:'18% of the beauty conversation, and growing fastest in search.', open:'issue:beauty:who'},
    {kind:'thread', thread:'glp1', kicker:'Thread', title:'GLP-1s are changing food, faces and the gym',
     body:'One story running through three of your issues this week.', open:'thread:glp1'},
    {kind:'shop', topic:'beauty', kicker:'Worth it this week', title:'The $10 primer people keep choosing',
     body:'e.l.f. Power Grip is the most-named dupe for Milk Makeup’s $38 Hydro Grip. People say it holds up all day.', open:'issue:beauty:shop'}
  ]
};

// What changed for things a reader follows. Keys match follow ids.
const FOLLOW_UPDATES = {
  'trend:nutrition:Fibermaxxing': {status:'rising', text:'Still rising: up 12% this week.'},
  'trend:nutrition:Protein in everything': {status:'peaked', text:'Down for the fourth month in a row.'},
  'trend:beauty:LED masks': {status:'rising', text:'Up again, mostly in “is it worth it” posts.'},
  'trend:exercise:Weighted vests': {status:'rising', text:'Up 4× this year. Walking pad posts are pairing with it.'},
  'trend:sleep:Sleepmaxxing': {status:'rising', text:'Up 9% this week.'},
  'claim:exercise-creatine-for-women': {status:'study', text:'A 2026 review in women after menopause was added to the evidence.'},
  'claim:sleep-mouth-taping': {status:'study', text:'A 2026 meta-analysis on nasal obstruction was added. Still Hype.'},
  'product:nutrition:0': {status:'price', text:'Now $2.29 at Amazon.'},
  'product:beauty:1': {status:'price', text:'The e.l.f. dupe is back in stock at Target.'},
  'search:Is creatine safe for women?': {status:'ready', text:'Your deep dive is ready.'}
};

const TRENDING_SEARCHES = ['Is creatine safe for women?','What are people saying about retinol?','Is Olipop actually good for you?','Where is sleep tourism heading?','Why is everyone doing Pilates?'];

// Fully written sample answers for the trending searches. Anything else
// shows the agent's plan and a sample results layout.
const SEARCH_SAMPLES = [
  {q:'Is creatine safe for women?', topic:'exercise', intent:'real',
   instant:'Yes, for most healthy adults, according to an expert position stand. In women, studies show small strength gains when creatine is paired with strength training, and no sign of harm in recent trials. It has not been shown to boost everyday energy.',
   links:[{type:'claim', id:'exercise-creatine-for-women'},{type:'issue', topic:'exercise', page:'hype'}],
   result:{headline:'Creatine moved from bodybuilding to women’s strength, and the research mostly backs it.',
     themes:[['“Will it make me bulky?”','The top worry in posts, and the top question in search.'],['Creatine for brain fog','A newer angle, mostly from women in their late 30s.'],['Gummies vs. powder','Price and testing complaints about gummies are rising.']],
     who:[['The Strong Era','I want to be strong at 70, not small at 30.'],['The Cautious Starter','I’ll try it once I know it’s safe for women.']],
     next:'Expect creatine to be marketed for women’s energy and focus, ahead of the evidence.'}},
  {q:'What are people saying about retinol?', topic:'beauty', intent:'talk',
   instant:'Retinol is moving from “every night” to “a few nights a week”. Barrier repair is the bigger story in your Beauty issue, and over-use is the most common complaint in posts.',
   links:[{type:'issue', topic:'beauty', page:'conversation'},{type:'claim', id:'beauty-barrier-repair'}],
   result:{headline:'Retinol isn’t over. People just want less of it.',
     themes:[['Retinol sandwiching','Moisturizer before and after to cut irritation.'],['Skin cycling','Retinol two nights, rest nights in between.'],['Retinal vs. retinol','The stronger cousin is the new upgrade question.']],
     who:[['The Shelf Editor','Fewer products, better ones.'],['The Longevity Investor','I’m protecting what I’ve got.']],
     next:'Gentler retinoid formats and “retinol for sensitive skin” lines keep growing.'}},
  {q:'Is Olipop actually good for you?', topic:'nutrition', intent:'worth',
   instant:'People love it as a soda swap with 6 to 9 grams of fiber a can. The main complaints are gas in the first week and the cost adding up. It’s rated Worth it in your Nutrition issue.',
   links:[{type:'issue', topic:'nutrition', page:'shop'},{type:'claim', id:'nutrition-fibermaxxing'}],
   result:{headline:'Olipop owns “soda with fiber”, but price is the pushback.',
     themes:[['The soda swap','Most posts frame it as a replacement, not a health drink.'],['Gut talk','Prebiotic claims drive interest; bloating drives complaints.'],['Store-brand copies','Cheaper prebiotic sodas are getting named more.']],
     who:[['The Add-Don’t-Subtract Eater','I’d rather ask what I can add to my plate.']],
     next:'Expect more store brands and fiber claims on every soda shelf.'}},
  {q:'Where is sleep tourism heading?', topic:'sleep', intent:'future',
   instant:'Sleep tourism has settled into a steady hotel category after its 2024 peak, per your Sleep issue. Hotels are adding sleep menus and quiet rooms.',
   links:[{type:'issue', topic:'sleep', page:'life'}],
   result:{headline:'Sleep tourism is becoming a hotel standard, not a trend.',
     themes:[['Sleep menus','Pillow, sound and blackout options at check-in.'],['Recovery retreats','Sleep packaged with sauna and spa.'],['Price backlash','“Paying $400 to sleep” posts.']],
     who:[['The Sleepmaxxer','My bedtime routine is the most important part of my day.']],
     next:'Two futures: sleep becomes a standard hotel amenity, or a luxury niche.'}},
  {q:'Why is everyone doing Pilates?', topic:'exercise', intent:'why',
   instant:'Reformer Pilates is a workout, a social life and a status signal at once. Your Exercise issue’s Reformer Loyalist calls it “my therapy, my social life and my splurge”.',
   links:[{type:'issue', topic:'exercise', page:'who'}],
   result:{headline:'Pilates sells calm, community and a look, not just a workout.',
     themes:[['The quiet luxury workout','Matching sets, neutral studios, low sweat.'],['$40 a class','Price fatigue pushes people to at-home reformers.'],['Strength crossover','More posts pair Pilates with lifting.']],
     who:[['The Reformer Loyalist','It’s my therapy, my social life and my splurge.']],
     next:'Studios add strength classes; at-home reformers get cheaper.'}}
];

window.WHOLE_DAILY = {EDITION, FOLLOW_UPDATES, TRENDING_SEARCHES, SEARCH_SAMPLES};
})();
