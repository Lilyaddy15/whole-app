/* WHOLE sample content. Mock Anthropologic pipeline output written in magazine voice.
   Not real data. Shape matches what live pipeline runs will produce. */
(function(){
const TOPICS = {
  nutrition:{
    name:'Nutrition', bg:'var(--nutrition)', ink:'var(--nutrition-ink)', hi:'var(--nutrition-hi)',
    stat:'64%', statLine:'of Americans are now fibermaxxing, counting grams like macros',
    cover:[['Fiber is the new protein','Why your feed stopped counting what to cut'],['Real or hype?','Seed oils, vinegar shots and CGMs, checked'],['Asking, not posting','What women google about eating on GLP-1s']],
    answer:'Women stopped counting what to cut and started counting what to add.',
    lede:'Two years of protein-in-everything left a lot of women tired. The new goal is 30 grams of fiber a day, tracked with the same apps and the same pride. Underneath it sits a quieter shift: more women eating less on GLP-1s and wanting every bite to count.',
    receipt:{pipe:'Discourse', posts:'4,812 posts and 2.1M searches', window:'Jul 1 – Sep 30, 2026'},
    themes:[
      {h:'Fibermaxxing goes mainstream', p:'Chia, lentils and “30 plants a week” challenges, logged like macros.', posted:24, searched:31},
      {h:'Protein fatigue sets in', p:'Backlash against protein-spiked coffee, chips and cereal.', posted:18, searched:6},
      {h:'Eating on GLP-1s', p:'Smaller plates, nausea workarounds and how to stop losing muscle.', posted:9, searched:28},
      {h:'Blood-sugar hacks', p:'Vinegar before meals, walks after dinner and “naked carbs”.', posted:20, searched:15},
      {h:'Ultra-processed anxiety', p:'Label scanning apps and swapping out seed oils.', posted:17, searched:12},
      {h:'Cottage cheese everything', p:'Flatbreads, ice cream and queso. The viral ingredient that stuck.', posted:12, searched:8}
    ],
    hormone:{b:'Cravings and bloat follow your cycle.', p:'Posts about magnesium, dark chocolate and “why am I so bloated” cluster in the week before a period. If you’re adding fiber, that week is the hardest time to start.'},
    asking:[
      {q:'What should I eat on Ozempic?', mult:'3.1×', a:'Small, protein-first meals and plenty of fluids. The biggest worry in searches is losing muscle along with fat.'},
      {q:'Why am I bloated after adding fiber?', mult:'2.4×', a:'Usually because the jump was too fast. People who stick with it add a few grams a week and drink more water.'},
      {q:'Is it bad to skip breakfast?', mult:'1.9×', a:'The posts are split by goal. For most healthy adults, what you eat over the day matters more than when.'}
    ],
    hype:[
      {id:'nutrition-fibermaxxing', t:'Fibermaxxing', v:'real', says:'“30 grams a day changed my digestion and my cravings.”', ev:'People who eat more fiber, around 25 to 30 grams a day or more, have lower rates of heart disease, type 2 diabetes and colon cancer. Trials show fiber helps with constipation. The effect on appetite and cravings is less consistent, and adding fiber gradually helps limit gas and bloating.'},
      {id:'nutrition-vinegar-shots-before-meals', t:'Vinegar shots before meals', v:'mixed', says:'“A spoon of apple cider vinegar flattens my glucose spike.”', ev:'Pooled clinical trials show that vinegar taken with a meal can modestly lower the rise in blood sugar afterward. The studies are small and vary a lot, and there is not good evidence that it causes weight loss. Vinegar is acidic and can wear down tooth enamel, so it is usually diluted.'},
      {id:'nutrition-wearing-a-cgm-without-diabetes', t:'Wearing a CGM without diabetes', v:'early', says:'“Two weeks with a glucose monitor taught me more than any diet.”', ev:'Research on glucose monitors in people without diabetes is still small and low in certainty. One trial found people ate fewer high-sugar carbs when the monitor came with nutrition coaching, but lasting benefits from the monitor alone have not been shown. In healthy people blood sugar stays in the normal range almost all day, so short rises after meals are expected.'},
      {id:'nutrition-seed-oils-are-toxic', t:'“Seed oils are toxic”', v:'hype', says:'“I cook in butter and tallow now. Seed oils are poison.”', ev:'Major reviews do not support the idea that seed oils are toxic. People who eat more linoleic acid, the main fat in most seed oils, have lower heart disease risk. Replacing saturated fats like butter with unsaturated oils lowers LDL cholesterol and is linked to fewer heart problems.'}
    ],
    segments:[
      {n:'The Add-Don’t-Subtract Eater', q:'I’m done with restriction. I’d rather ask what I can add to my plate.', share:34, trigger:'A fiber challenge or “30 plants” tracker going viral', buys:'Prebiotic sodas, chia, bean pastas'},
      {n:'The Glucose Watcher', q:'If I can see the spike, I can fix it.', share:22, trigger:'Trying a CGM for two weeks, then keeping the habits', buys:'Over-the-counter CGMs, apple cider vinegar'},
      {n:'The Protein Burnout', q:'I’ve had enough protein pudding for a lifetime.', share:19, trigger:'Price hikes and taste fatigue on protein products', buys:'Whole-food swaps, Greek yogurt, eggs'},
      {n:'The Quiet GLP-1 Eater', q:'I’m eating less, so every bite has to count. I just don’t want to talk about why.', share:25, trigger:'Starting a GLP-1 and losing appetite overnight', buys:'Protein shakes, electrolytes, small-portion meals'}
    ],
    brands:[
      {b:'Olipop', t:'up', tl:'Rising', what:'Owns the “soda with fiber” conversation.'},
      {b:'Good Culture', t:'up', tl:'Rising', what:'Rode cottage cheese from recipe hack to fridge staple.'},
      {b:'Protein-spiked snacks', t:'down', tl:'Cooling', what:'The category, not one brand. “Protein chips” are now a punchline.'}
    ],
    products:[
      {name:'Prebiotic soda', brand:'Olipop', mark:'O', price:2.49, unit:'can', perUse:2.49, verdict:'worth', loved:'Tastes like real soda, with 6–9 g of fiber a can', gripes:'Gassy for the first week; the cost adds up', mentions:'1,240', dupe:{name:'Store-brand prebiotic soda', price:1.25}, shops:[['Target',2.49],['Walmart',2.38],['Amazon',2.29]]},
      {name:'Organic chia seeds, 2 lb', brand:'Viva Naturals', mark:'C', price:13.99, unit:'bag', perUse:0.22, verdict:'worth', loved:'The cheapest fiber per gram in every “what I eat” video', gripes:'Texture takes getting used to', mentions:'860', dupe:null, shops:[['Amazon',13.99],['Walmart',12.97]]},
      {name:'Lingo glucose sensor', brand:'Abbott', mark:'L', price:49, unit:'2 weeks', perUse:3.50, verdict:'try', loved:'Seeing which meals spike you is eye-opening', gripes:'People stop after one sensor; habits stay, the monitor doesn’t', mentions:'540', dupe:{name:'Stelo by Dexcom', price:99}, shops:[['Lingo.com',49],['Amazon',49]]},
      {name:'Protein chips', brand:'Any brand', mark:'P', price:2.99, unit:'bag', perUse:2.99, verdict:'skip', loved:'Crunchy and convenient', gripes:'“Just eat Greek yogurt.” Taste and price are the top complaints', mentions:'410', dupe:{name:'Greek yogurt cup', price:1.19}, shops:[['Target',2.99]]}
    ],
    life:[
      {t:'Fibermaxxing', s:'rising', since:'Up 3× since spring', pts:[2,3,3,4,5,7,9,12]},
      {t:'Cottage cheese everything', s:'sticking', since:'Peaked 2024, still steady', pts:[3,8,12,10,9,9,8,8]},
      {t:'Protein in everything', s:'peaked', since:'Turning since June', pts:[6,8,10,12,12,11,9,7]},
      {t:'“Girl dinner”', s:'faded', since:'Gone quiet after 2023', pts:[12,9,6,4,3,2,2,1]}
    ],
    next:[
      {w:'Now', s:'2026', h:'Fiber on the front of the pack', p:'Expect “good source of fiber” to replace “high protein” as the badge brands fight over.'},
      {w:'Next', s:'2027', h:'Food built for GLP-1 bodies', p:'Small, dense, high-protein meals designed for people who can only eat a few bites.'},
      {w:'Later', s:'2030', h:'Your glucose data writes the grocery list', p:'CGMs and food apps merge, and your cart adjusts to how your body responded last week.'}
    ],
    worlds:[['Tracked plate','Every gram logged, every spike seen'],['Intuitive plate','Tracking burnout brings back “just eat real food”']],
    qa:[
      {q:'Is fibermaxxing actually good for me?', a:'For most people, yes. The average American eats about half the recommended fiber. The pushback in posts is about going too fast: bloating shows up in about 1 in 5 fibermaxxing threads.'},
      {q:'Why is everyone over protein?', a:'Taste and price. The protein boom put it in coffee, chips and cereal, and people started saying it tasted like a supplement. Protein itself is not the problem. The joke is protein on every label.'},
      {q:'What are people on GLP-1s eating?', a:'Small, protein-first meals, broths and electrolyte drinks. The most common worry is losing muscle.'}
    ]
  },
  beauty:{
    name:'Beauty', bg:'var(--beauty)', ink:'var(--beauty-ink)', hi:'var(--beauty-hi)',
    stat:"1 in 2",
    statLine:"skincare searches we tracked were about fixing a damaged skin barrier. Only 1 in 10 articles covered it.",
    cover:[["Fewer, better, proven", "Why women are quitting the ten-step routine"], ["Real or hype?", "Glass skin, fragrance-free and AI face scans, checked"], ["Skin on GLP-1s", "37.7% report sagging. What comes next"]],
    answer:"Fewer products now signal competence, and women trust strangers to prove it.",
    lede:"Forty-five percent of US women name cost as a reason they give up on a skincare routine, and 36 percent name too many steps. The women who stay are cutting down to three or four barrier-friendly products, with CeraVe and BYOMA named most often, and checking every choice with strangers on Reddit before they buy. The loudest argument is about who to trust. The quietest is in search: half of it is about repairing skin.",
    receipt:{"pipe": "Discourse · Trends · Segmentation", "posts": "992 articles and videos, 10,399 signals", "window": "Last 3 months to Nov 1, 2026"},
    themes:[{"h": "Quitting before it works", "p": "Cost, too many steps and slow results make routines collapse. The fix women film: a three- or four-product capsule routine.", "posted": 25, "searched": 35}, {"h": "Barrier first, glow second", "p": "Glass skin now reads as long-term damage. Ceramides, fragrance-free formulas and softer “cloud skin” replace stacked actives.", "posted": 11, "searched": 50}, {"h": "Reddit over influencers", "p": "Shoppers trust strangers who show their real skin more than paid endorsements. Almost nobody searches it; everybody argues it.", "posted": 26, "searched": 0}, {"h": "Restraint is the new flex", "p": "Project pan, finishing what you own and lived-in skin. Using less now reads as status.", "posted": 7, "searched": 11}, {"h": "Let AI choose, but not look", "p": "Overwhelmed women want an app to pick their products, and worry about what a face scan sees.", "posted": 4, "searched": 4}],
    hormone:{"b": "Your blood work is showing up in your skincare.", "p": "Women are linking dull skin, breakouts and hair shedding to iron and thyroid levels since Vogue named “ferritin face”. Searches for “low ferritin hair loss” hit their highest point in September. New American Society of Hematology guidelines raise the threshold for diagnosing iron deficiency, which could widen who hears that answer."},
    asking:[{"q": "How do I repair my skin barrier?", "mult": "4.6×", "a": "Half of all searches in this conversation, and barely covered. The research backs the basics: stop over-exfoliating and use a plain moisturizer. Ceramides help, but no cream clearly beats the rest."}, {"q": "Is this skincare free trial a scam?", "mult": "52×", "a": "21,480 searches a month and almost no coverage. Shoppers describe “free” DTC trials, naming Belle Epoque, Nuavive and Neulift, that enroll them in a monthly charge and take a phone call to cancel."}, {"q": "What is the simplest routine that works?", "mult": "1.4×", "a": "The dermatologists’ short list: cleanse, treat if you need to, moisturize, sunscreen. No study has tested ten steps against four."}],
    hype:[{"id": "beauty-barrier-repair", "t": "Barrier repair", "says": "Strip it back to a gentle moisturizer and your skin will heal.", "v": "real", "ev": "Dermatologists warn that over-exfoliating can leave skin red and irritated, so cutting back is a sensible first step. Studies show moisturizers, including ones with ceramides, help dry and irritated skin recover. No single moisturizer has been shown to work clearly better than the rest."}, {"id": "beauty-glass-skin-over-exfoliation", "t": "Glass skin layering", "says": "Chasing glass skin with layers of acids and exfoliants wrecks your barrier long term.", "v": "mixed", "ev": "Dermatologists agree that over-exfoliating, and stacking several strong actives at once, can leave skin red, stinging and irritated. Acids like glycolic and lactic acid are useful at the right strength but can burn and itch at higher doses. What hasn't been studied is whether layering them causes lasting, long-term damage; the evidence is about short-term irritation that usually settles when you cut back."}, {"id": "beauty-fragrance-free", "t": "Fragrance-free", "says": "Fragrance-free products are better for sensitive, irritated skin.", "v": "mixed", "ev": "Fragrance is one of the most common causes of skin allergy, and dermatologists consistently advise fragrance-free products for sensitive skin. But fragrance allergy affects a minority of people, and head-to-head testing is thin: one randomized trial in people with sensitive skin found a mild cleanser with a carefully chosen fragrance was tolerated as well as a fragrance-free one. The advice is a sensible precaution more than a proven rule for everyone."}, {"id": "beauty-fewer-products", "t": "The 3-product routine", "says": "Three or four products work as well as ten steps.", "v": "early", "ev": "Dermatologists generally recommend a short routine built around cleansing, any treatment you need, moisturizer and sunscreen, and say consistency matters more than a 10-step routine. They also warn that stacking several active products can irritate skin. But no study has directly compared a three- or four-product routine with a ten-step one, so 'works just as well' is reasonable expert advice rather than a tested result."}, {"id": "beauty-ai-skin-scans", "t": "AI face scans", "says": "An AI face scan can tell you exactly what your skin needs.", "v": "mixed", "ev": "In small studies, app-based face scans roughly matched a dermatologist's ratings for visible things like redness, wrinkles and pores, but did worse on moisture, texture and firmness. No study shows a scan can tell you which products your skin needs. Apps that check moles for skin cancer have been tested more, and reviews found they miss too many cancers to be relied on."}, {"id": "beauty-at-home-led-masks", "t": "At-home LED masks", "says": "A red-light mask at home is a clinic treatment for less.", "v": "mixed", "ev": "Red and blue light have some trial support for mild acne, and red light for fine lines. Evidence that LED light reduces facial redness or rosacea is thin, with only a few small studies. Most studies are small and use clinic devices, so results from home masks are less certain."}],
    segments:[{"n": "Budget Shoppers", "q": "Good skin shouldn’t cost you — find the shortcut, not the sacrifice.", "share": 24, "trigger": "Affordable products that actually work", "buys": "CeraVe, L’Oréal, Sephora", "pos": {"x": 0.3, "y": 0.1}}, {"n": "Barrier Repairers", "q": "Healing skin is slow, communal work — the process itself is the point.", "share": 22, "trigger": "Simple, low-irritation product stacks", "buys": "Aestura, haruharu wonder, Bioderma", "pos": {"x": 0.2, "y": 0.45}}, {"n": "Transformation Trackers", "q": "Proof lives in the timeline — public struggle earns the right to claim results.", "share": 18, "trigger": "Products that deliver results over time", "buys": "Pharmacy and drugstore skincare, prescription treatments", "pos": {"x": 0.15, "y": 0.4}}, {"n": "Luxury Collectors", "q": "Premium products signal that your skin deserves the best, no justification needed.", "share": 16, "trigger": "Proof that premium products outperform", "buys": "Caudalie, Estée Lauder, Sulwhasoo", "pos": {"x": 0.85, "y": 0.9}}, {"n": "Ingredient Researchers", "q": "Science is the authority — knowing the formula earns the outcome.", "share": 13, "trigger": "Ingredient-level product explanations", "buys": "Skinbetter Science, COSRX, Isntree", "pos": {"x": 0.25, "y": 0.5}}, {"n": "Routine Simplifiers", "q": "A tight, reliable routine is competence — not laziness, just efficiency.", "share": 7, "trigger": "A short stack of proven staples", "buys": "CeraVe", "pos": {"x": 0.55, "y": 0.45}}],
    brands:[{"b": "CeraVe", "t": "up", "tl": "Most named", "what": "The staple of the three-product routine, and the clearance-aisle find budget shoppers grab first."}, {"b": "BYOMA", "t": "up", "tl": "Named often", "what": "Shows up in capsule barrier routines on TikTok next to CeraVe."}, {"b": "e.l.f.", "t": "up", "tl": "The dupe", "what": "Its vitamin C serum is called “almost identical in formulation” to SkinCeuticals C E Ferulic."}, {"b": "Neutrogena", "t": "down", "tl": "Boycott calls", "what": "Reddit and Threads users vowed never to buy again after it ended an ambassador’s contract, reading it as dropping her during postpartum depression."}],
    products:[{"name": "Moisturizing Cream", "brand": "CeraVe", "mark": "CV", "price": 17.99, "unit": "16 oz jar", "perUse": 0.02, "verdict": "worth", "loved": "The base of the three-product routine, and the clearance-aisle find budget shoppers grab first", "gripes": "A class action alleges its “baby” versions charge more for the same formula", "mentions": "", "dupe": null, "shops": [["Target", 17.99], ["Ulta", 19.99]]}, {"name": "Moisturizing Gel Cream", "brand": "BYOMA", "mark": "BY", "price": 14.99, "unit": "1.69 oz jar", "perUse": 0.15, "verdict": "try", "loved": "Named with CeraVe in capsule barrier routines, and on “best under $20” lists", "gripes": "Little pushback in this quarter’s data yet", "mentions": "", "dupe": null, "shops": [["Target", 14.99], ["Ulta", 15.99]]}, {"name": "C E Ferulic", "brand": "SkinCeuticals", "mark": "CE", "price": 185, "unit": "1 oz bottle", "perUse": 1.23, "verdict": "dupe", "loved": "The vitamin C serum every dupe gets measured against", "gripes": "$185, when shoppers call a $17 serum “almost identical in formulation”", "mentions": "", "dupe": {"name": "e.l.f. Bright Icon Vitamin C + E + Ferulic Serum", "price": 17}, "shops": [["Dermstore", 185]]}],
    life:[{"t": "Bemotrizinol sunscreen", "s": "rising", "since": "40,500 searches in June, when the FDA approved it. Still 18,100 in August", "pts": [0, 0, 0, 0, 0, 12, 7, 5]}, {"t": "Low-ferritin hair loss", "s": "rising", "since": "At its highest in September", "pts": [7, 5, 7, 7, 7, 8, 8, 12]}, {"t": "At-home chemical peels", "s": "sticking", "since": "6,600 to 9,900 searches a month for over a year", "pts": [10, 10, 12, 8, 10, 10, 12, 8]}, {"t": "Paraben-free", "s": "faded", "since": "Down from 390 to 70 searches a month since last fall", "pts": [12, 12, 10, 6, 8, 3, 2, 2]}],
    next:[{"w": "Now", "s": "2026", "h": "Proof is the price of entry", "p": "The FDA approved bemotrizinol, the first new US sunscreen filter in over 25 years, and brands sell “longevity” with clinical data. Shoppers want a number, not a feeling."}, {"w": "Next", "s": "2027", "h": "GLP-1 skin becomes a category", "p": "37.7% of GLP-1 users report sagging skin and 29.2% facial volume loss. Expect products built for skin that changes on a drug timeline."}, {"w": "Later", "s": "2029", "h": "Collagen from the inside", "p": "Bioengineered collagen that rebuilds skin from within, and a fight over whether it counts as beauty or medicine."}],
    worlds:[["Beauty becomes medicine", "Skin repair moves behind the pharmacy counter, with prices to match"], ["Medicine becomes beauty", "A weekly face scan sets your dose, and the dermatologist steps back"]],
    qa:[{"q": "Is glass skin bad for you?", "a": "Over-exfoliating and stacking strong acids clearly cause redness and stinging. Lasting damage hasn’t been shown, and the irritation usually settles when you cut back."}, {"q": "Do I need an expensive serum?", "a": "Shoppers say often not: e.l.f.’s vitamin C serum is called “almost identical in formulation” to SkinCeuticals C E Ferulic. The women who do pay $100 or more want proof it outperforms."}, {"q": "What is bemotrizinol?", "a": "A sunscreen filter used for years in Europe and Australia and newly approved in the US, the first new one in over 25 years. Searches hit 40,500 in June."}],
    issueNo:"Issue No. 01",
    feed:[{"who": "@ariellelorre", "plays": "135K", "what": "A 41-year-old woman shares her nighttime skincare routine for achieving 'glass skin,' detailing the products she uses and her experience with them.", "url": "https://www.tiktok.com/@ariellelorre/video/7683997978582846750", "cap": "Glass skin at 41: her full night routine"}, {"who": "@kristynhoffman96", "plays": "4K", "what": "A woman demonstrates a capsule skincare routine for a glowing skin barrier using BYOMA products, highlighting a cleanser, face mist, toner, serum, moisturizer, and SPF.", "url": "https://www.tiktok.com/@kristynhoffman96/video/7701499818136423710", "cap": "A capsule barrier routine, all BYOMA"}, {"who": "@yurileeeee", "plays": "776K", "what": "A woman demonstrates various skincare and beauty practices, including applying products, using facial tools, and consuming a healthy drink, as part of her routine for future self-care.", "url": "https://www.tiktok.com/@yurileeeee/video/7665399075247885582", "cap": "Skincare as care for your future self"}, {"who": "@ashley.paiige", "plays": "247K", "what": "A woman shares her elaborate nighttime skincare and haircare routine, including cleansing, applying serums and moisturizers, and styling her hair, while discussing her skin concerns and product preferences.", "url": "https://www.tiktok.com/@ashley.paiige/video/7696551896999415053", "cap": "The long version: a full night routine"}],
    segMap:{"x": ["Earned", "Given"], "y": ["Budget", "Premium"], "note": "Earned: good skin is something you work for. Given: something you buy your way into."},
    lifeHow:{"line": "Monthly Google searches, last 8 data points", "window": "May 2025 – Sep 2026"},
    pricesNote:"Checked on retailer sites, Nov 1, 2026",
    issueTitle:"The Skin Issue",
    issueDate:"Nov 2026",
    visual:{"statShort": "of skincare searches were about fixing a damaged barrier", "statFill": 50, "highlight": ["Fewer products", "strangers"], "bigStats": [{"n": "45%", "l": "quit a routine over cost"}, {"n": "36%", "l": "quit over too many steps"}, {"n": "3–4", "l": "products in the routine that lasts"}], "gapNote": {"row": 1, "text": "half of all searches, barely posted"}, "hormoneShort": "“Ferritin face”: women are reading their blood work for answers about skin and hair.", "lifeNote": "FDA approval", "dupe": {"hi": {"name": "SkinCeuticals C E Ferulic", "price": 185}, "lo": {"name": "e.l.f. Bright Icon", "price": 17}, "quote": "“almost identical in formulation”"}, "pull": "The routine was always designed to sell the next product, not to finish.", "lifeBig": {"n": 40500, "l": "searches in June, the month it was approved"}}
  },
  exercise:{
    name:'Exercise', bg:'var(--exercise)', ink:'var(--exercise-ink)', hi:'var(--exercise-hi)',
    stat:'2×', statLine:'more women 25–40 posting about lifting heavy than about cardio',
    cover:[['Strong, not small','The weight room is the new yoga studio'],['Real or hype?','Cycle syncing, creatine and cold plunges, checked'],['Asking, not posting','The workout question women don’t post about']],
    answer:'The goal changed from getting smaller to getting stronger.',
    lede:'Lifting heavy is now the most talked-about way women train, and “strong at 70” is how people explain it. Recovery has become a status symbol, tracked on wearables and shared like a workout. The biggest open question is in search: how to train around your cycle.',
    receipt:{pipe:'Discourse', posts:'5,530 posts and 2.7M searches', window:'Jul 1 – Sep 30, 2026'},
    themes:[
      {h:'Strength over shrinking', p:'Progressive overload, PRs and “lift heavy” as self-respect.', posted:27, searched:19},
      {h:'Cycle-synced training', p:'Lighter weeks, harder weeks and phase-based plans.', posted:8, searched:24},
      {h:'Walking is enough', p:'Walking pads, 10k steps and zone 2 as the no-pressure baseline.', posted:18, searched:20},
      {h:'Recovery as a flex', p:'Sauna, cold plunge and sleep scores posted like PRs.', posted:17, searched:11},
      {h:'Reformer price fatigue', p:'$40 classes, at-home reformers and “worth it?” debates.', posted:16, searched:12},
      {h:'The algorithm coach', p:'AI plans and app-built programs replacing trainers.', posted:14, searched:14}
    ],
    hormone:{b:'Your energy isn’t the same every week.', p:'Many women report stronger lifts in the first half of their cycle and lower energy just before a period. The research is still early, so the safest read is to plan lighter days when you need them.'},
    asking:[
      {q:'How should I work out during each phase of my cycle?', mult:'3×', a:'The common pattern: heavier lifting in the first half, walking and mobility in the days before a period. Evidence is early.'},
      {q:'Why do I leak when I jump?', mult:'2.9×', a:'Very common after pregnancy and with age, and almost never posted about. Pelvic floor physical therapy is the most recommended fix.'},
      {q:'How do I keep muscle on a GLP-1?', mult:'2.6×', a:'Strength training two or three times a week plus enough protein. This is the most shared advice in GLP-1 fitness threads.'}
    ],
    hype:[
      {id:'exercise-lifting-heavy', t:'Lifting heavy', v:'real', says:'“I want to be strong at 70, not small at 30.”', ev:'Strength training builds muscle and strength at any age, and heavier weights build the most maximal strength. Lighter weights done close to failure can build similar muscle size. In trials of women after menopause, heavy lifting and impact training raised bone density slightly, while results in younger women are less clear.'},
      {id:'exercise-creatine-for-women', t:'Creatine for women', v:'real', says:'“Creatine gave me energy and my lifts finally moved.”', ev:'Creatine is one of the most studied supplements, and with strength training it helps build strength. Studies in women are fewer, and gains in women tend to be small, with clearer effects on strength than on muscle size. It has not been shown to boost everyday energy.'},
      {id:'exercise-cycle-synced-workouts', t:'Cycle-synced workouts', v:'early', says:'“My body isn’t the same every week, so my workout isn’t either.”', ev:'Studies find that cycle phase has at most a tiny effect on performance on average, and much of the research is low quality. There is no good evidence that strict phase-based training plans build more strength or muscle. Adjusting a workout to how you feel on a given day is reasonable.'},
      {id:'exercise-cold-plunges-for-fat-loss', t:'Cold plunges for fat loss', v:'hype', says:'“Ice baths melt fat and speed up your metabolism.”', ev:'Cold exposure makes the body burn a little more energy, but no good trials show that cold plunges lead to fat loss. Some people use them to feel better after hard training. Taking a cold plunge right after lifting may reduce muscle gains over time.'}
    ],
    segments:[
      {n:'The Strong Era', q:'I want to be strong at 70, not small at 30.', share:33, trigger:'A first PR or a parent’s fall', buys:'Gym memberships, lifting programs, creatine'},
      {n:'The Cycle Syncer', q:'My body isn’t the same every week, so my workout isn’t either.', share:17, trigger:'Burnout from training hard every day', buys:'Cycle-tracking apps, wearables'},
      {n:'The Reformer Loyalist', q:'It’s my therapy, my social life and my splurge.', share:22, trigger:'A friend’s class pack or a new studio opening', buys:'Class packs, grip socks, matching sets'},
      {n:'The Step Counter', q:'10,000 steps and a podcast. That’s the workout.', share:28, trigger:'Gym burnout or a new work-from-home routine', buys:'Walking pads, good sneakers'}
    ],
    brands:[
      {b:'Oura', t:'flat', tl:'Steady', what:'The ring in every recovery-score screenshot.'},
      {b:'Ladder', t:'up', tl:'Rising', what:'The strength app women name most when they leave classes.'},
      {b:'Boutique cardio', t:'down', tl:'Cooling', what:'Spin and HIIT come up as “what I used to do”.'}
    ],
    products:[
      {name:'Creatine monohydrate', brand:'Thorne', mark:'Cr', price:43, unit:'90 servings', perUse:0.48, verdict:'worth', loved:'Cheap per day, third-party tested, lifts improve', gripes:'Some report mild water weight at first', mentions:'1,620', dupe:{name:'Any third-party-tested monohydrate', price:22}, shops:[['Amazon',43],['Thorne.com',43]]},
      {name:'Under-desk walking pad', brand:'WalkingPad', mark:'W', price:399, unit:'pad', perUse:0.55, verdict:'worth', loved:'Hits 10k steps on work calls', gripes:'Loud on hard floors; slow top speed', mentions:'930', dupe:{name:'Budget under-desk treadmill', price:169}, shops:[['Amazon',399],['Walmart',379]]},
      {name:'20 lb weighted vest', brand:'Various', mark:'V', price:69, unit:'vest', perUse:0.35, verdict:'try', loved:'Turns daily walks into strength work', gripes:'Hot, and easy to overdo on the back', mentions:'610', dupe:null, shops:[['Amazon',69],['Target',74.99]]},
      {name:'At-home reformer', brand:'Various', mark:'R', price:1299, unit:'machine', perUse:4.30, verdict:'skip', loved:'Studio feel at home', gripes:'Most say it becomes a clothes rack unless you already go 3× a week', mentions:'340', dupe:{name:'Reformer class pack (10)', price:280}, shops:[['Amazon',1299]]}
    ],
    life:[
      {t:'Weighted vests', s:'rising', since:'Up 4× this year', pts:[1,2,2,3,5,7,9,12]},
      {t:'12-3-30 treadmill', s:'sticking', since:'Viral in 2020, still a routine', pts:[12,9,8,7,7,7,6,6]},
      {t:'Hot girl walk', s:'peaked', since:'Turned into plain “walking”', pts:[5,7,10,11,10,8,6,5]},
      {t:'Wall Pilates', s:'faded', since:'Quiet since 2024', pts:[12,10,7,4,3,2,2,1]}
    ],
    next:[
      {w:'Now', s:'2026', h:'Strength for midlife', p:'Menopause-informed lifting programs move from niche coaches to mainstream apps.'},
      {w:'Next', s:'2027', h:'The algorithm writes your week', p:'Wearable data decides heavy day, walk day or rest day each morning.'},
      {w:'Later', s:'2030', h:'Recovery studios replace gyms', p:'Sauna, cold and mobility become the place people meet, the way spin studios were.'}
    ],
    worlds:[['Quantified athlete','Every rep, cycle day and sleep score feeds one plan'],['Offline mover','Wearable fatigue brings back training by feel']],
    qa:[
      {q:'Should I train differently during my period?', a:'Many women say yes, and it is the most searched training question in this issue. The science is still early, so posts tend to frame it as “listen to your body”.'},
      {q:'Is walking really enough?', a:'For baseline health, walking is well supported. The Strong Era crowd adds that walking alone will not build muscle. The common answer: walk daily, lift two or three times a week.'},
      {q:'Why is everyone taking creatine?', a:'It has moved from bodybuilding into women’s strength posts. Creatine is one of the most studied supplements, and women mention it for strength, energy and recovery.'}
    ]
  },
  sleep:{
    name:'Sleep', bg:'var(--sleep)', ink:'var(--sleep-ink)', hi:'var(--sleep-hi)',
    stat:'1 in 3', statLine:'women 25–40 say they wake up tired most days',
    cover:[['Sleepmaxxing','Mouth tape, magnesium and the 9pm bedtime'],['Real or hype?','Mouth taping, magnesium and the sleepy girl mocktail, checked'],['Asking, not posting','Why do I wake up at 3am?']],
    answer:'Sleep became the wellness goal women actually want to hit.',
    lede:'Sleep is now tracked, optimized and posted like a workout. “Sleepmaxxing” routines stack magnesium, mouth tape and blackout everything. The private side is in search: women waking at 3am and wondering whether hormones are to blame.',
    receipt:{pipe:'Discourse', posts:'3,940 posts and 1.8M searches', window:'Jul 1 – Sep 30, 2026'},
    themes:[
      {h:'Sleepmaxxing routines', p:'Wind-down rituals, blackout rooms and a set bedtime, shared like a skincare routine.', posted:21, searched:18},
      {h:'Magnesium everything', p:'Glycinate before bed, magnesium sprays and “sleepy” powders.', posted:19, searched:22},
      {h:'The 3am wake-up', p:'Falling asleep fine, then waking in the night and lying there.', posted:6, searched:20},
      {h:'Mouth taping', p:'Tape over the lips for nose breathing, sold as better sleep and a sharper jaw.', posted:16, searched:9},
      {h:'Sleep score anxiety', p:'Feeling worse after a bad score, even when you felt fine.', posted:14, searched:8},
      {h:'The sleepy girl mocktail', p:'Tart cherry juice, magnesium and sparkling water before bed.', posted:12, searched:7}
    ],
    hormone:{b:'Sleep often gets worse before a period and in perimenopause.', p:'Many women report lighter sleep and night waking in the days before a period. From the late 30s, night sweats and 3am waking are among the first signs of perimenopause.'},
    asking:[
      {q:'Why do I wake up at 3am every night?', mult:'3.3×', a:'Stress, alcohol and hormone shifts are the most common reasons in the conversation. If it lasts for weeks, posts recommend talking to a doctor.'},
      {q:'Is it safe to take melatonin every night?', mult:'2.5×', a:'In the US melatonin is sold as a supplement, and doses vary widely between brands. Sleep doctors in the conversation suggest low doses and short-term use.'},
      {q:'Why am I tired even after 8 hours?', mult:'2.1×', a:'Sleep quality, not just hours. Snoring, low iron and thyroid come up most when women describe this.'}
    ],
    hype:[
      {id:'sleep-a-consistent-wake-up-time', t:'A consistent wake-up time', v:'real', says:'“Same alarm every day, weekends too. It fixed my sleep.”', ev:'A regular sleep schedule is one of the best-supported habits for better sleep. Getting up at the same time every morning is a core step in the leading talk-and-habit therapy for insomnia, and sleep experts agree that consistent sleep timing matters for health.'},
      {id:'sleep-magnesium-before-bed', t:'Magnesium before bed', v:'mixed', says:'“Magnesium glycinate knocks me out.”', ev:'A few small studies suggest magnesium may help people fall asleep a little faster or feel slightly less sleepless, mostly people who already sleep poorly or get little magnesium from food. The effects are modest, the research is low quality overall, and it is not a strong sleep aid.'},
      {id:'sleep-sleepy-girl-mocktail', t:'The sleepy girl mocktail', v:'early', says:'“Tart cherry juice and magnesium. Best sleep of my life.”', ev:'No studies have tested the mocktail itself. Tart cherry juice has a handful of small, short trials with mixed and mostly modest results, and magnesium’s sleep effects are also small. The drink is plausible but the hype is far ahead of the research.'},
      {id:'sleep-mouth-taping', t:'Mouth taping', v:'hype', says:'“Taping my mouth shut changed my sleep and my jawline.”', ev:'Reviews find little good evidence that mouth taping improves sleep, and no research supports claims about jawline changes. A couple of small studies saw some benefit in people with mild sleep apnea, but doctors warn it can be risky for people with a blocked nose or undiagnosed sleep apnea.'}
    ],
    segments:[
      {n:'The Sleepmaxxer', q:'My bedtime routine is the most important part of my day.', share:29, trigger:'A run of bad sleep or a viral night routine', buys:'Magnesium, eye masks, sunrise alarms'},
      {n:'The 3am Waker', q:'I fall asleep fine. It’s 3am that gets me.', share:24, trigger:'Weeks of night waking with no obvious cause', buys:'Supplements, cooling bedding'},
      {n:'The Score Checker', q:'If my ring says I slept badly, I feel tired all day.', share:21, trigger:'Getting a sleep tracker', buys:'Wearables, sleep apps'},
      {n:'The New Parent', q:'Sleep? I just want four hours in a row.', share:26, trigger:'A new baby', buys:'White noise, blackout blinds, coffee'}
    ],
    brands:[
      {b:'Hatch', t:'up', tl:'Rising', what:'The sunrise alarm in most “night routine” videos.'},
      {b:'Oura', t:'flat', tl:'Steady', what:'The sleep score people screenshot and worry about.'},
      {b:'Melatonin gummies', t:'down', tl:'Cooling', what:'The category, not a brand. Dose worries are growing.'}
    ],
    products:[
      {name:'Magnesium glycinate', brand:'Any third-party-tested brand', mark:'Mg', price:24, unit:'90 capsules', perUse:0.27, verdict:'try', loved:'Gentle, and many say they feel calmer at night', gripes:'Effects are subtle; some notice nothing', mentions:'1,410', dupe:null, shops:[['Amazon',24],['Target',22.99]]},
      {name:'Restore sunrise alarm', brand:'Hatch', mark:'H', price:169.99, unit:'device', perUse:0.47, verdict:'worth', loved:'Waking to light instead of an alarm', gripes:'Subscription upsell for sounds', mentions:'880', dupe:{name:'Basic sunrise alarm clock', price:39}, shops:[['Target',169.99],['Amazon',169.99]]},
      {name:'Silk sleep mask', brand:'Any brand', mark:'S', price:15, unit:'mask', perUse:0.04, verdict:'worth', loved:'Cheapest sleep upgrade people mention', gripes:'Slips off for side sleepers', mentions:'650', dupe:null, shops:[['Amazon',15],['Target',14.99]]},
      {name:'Mouth tape strips', brand:'Any brand', mark:'T', price:12, unit:'30 strips', perUse:0.40, verdict:'skip', loved:'Some say they snore less', gripes:'Uncomfortable; doctors flag the risks', mentions:'520', dupe:null, shops:[['Amazon',12]]}
    ],
    life:[
      {t:'Sleepmaxxing', s:'rising', since:'Up all year', pts:[2,3,4,5,6,8,10,12]},
      {t:'Sleep tourism', s:'sticking', since:'Settled into a hotel category', pts:[4,7,10,9,8,8,8,8]},
      {t:'Sleepy girl mocktail', s:'peaked', since:'Fading since spring', pts:[6,9,12,11,9,7,6,5]},
      {t:'“Sleep banking”', s:'faded', since:'Barely mentioned now', pts:[10,8,6,4,3,2,2,1]}
    ],
    next:[
      {w:'Now', s:'2026', h:'Sleep is the metric that matters', p:'Sleep scores overtake step counts as the number people check first.'},
      {w:'Next', s:'2027', h:'Hormone-aware sleep tracking', p:'Wearables start linking night waking and temperature to cycle and perimenopause.'},
      {w:'Later', s:'2030', h:'Bedrooms designed for sleep', p:'Light, temperature and sound set themselves around your sleep data.'}
    ],
    worlds:[['Optimized night','Every variable tracked and tuned'],['Sleep by feel','Score fatigue brings back simple habits']],
    qa:[
      {q:'Does magnesium actually help sleep?', a:'Possibly a little. The evidence is modest and strongest in people who are low in magnesium. Most posts describe a calmer feeling rather than a knockout effect.'},
      {q:'Is mouth taping dangerous?', a:'It can be for some people, especially anyone with a blocked nose or undiagnosed sleep apnea. Doctors in the conversation suggest checking with a professional first.'},
      {q:'Why does my sleep get worse before my period?', a:'Hormone shifts before a period can raise body temperature and make sleep lighter. Many women report it, and it is one of the most searched sleep questions.'}
    ]
  }
};

const THREADS = {
  glp1:{
    name:'GLP-1', topics:['nutrition','beauty','exercise'], grad:'linear-gradient(135deg,var(--nutrition) 0%,var(--beauty) 55%,var(--exercise) 100%)',
    stat:'1 in 8', statLine:'US adults say they have taken a GLP-1 drug',
    lede:'GLP-1s show up in all three of your issues, usually without the name. They change how much people eat, how faces and hair look after fast weight loss, and why women are suddenly lifting to hold on to muscle.',
    facets:{
      nutrition:{b:'Smaller plates, protein first', p:'Searches for what to eat on a GLP-1 run 3× ahead of posts about it.'},
      beauty:{b:'“Ozempic face” and hair shedding', p:'Volume loss and shedding after fast weight loss are rising in beauty searches.'},
      exercise:{b:'Lift to keep the muscle', p:'Strength training is the most shared advice in GLP-1 fitness threads.'}
    },
    asking:[{q:'How do I keep muscle on a GLP-1?', mult:'2.6×'},{q:'What should I eat on Ozempic?', mult:'3.1×'},{q:'How do I fix “Ozempic face” without filler?', mult:'2.2×'}],
    todo:['Put protein first at every meal.','Lift two or three times a week.','Expect some shedding; it usually settles.','Talk to your prescriber before adding supplements.']
  },
  hormones:{
    name:'Hormones', topics:['beauty','exercise','nutrition','sleep'], grad:'linear-gradient(135deg,var(--beauty) 0%,var(--custom-hi) 100%)',
    stat:'3×', statLine:'more searched than posted: hormone questions across your issues',
    lede:'The most private questions in this week’s issues are all about hormones: skin that changes at 38, workouts that feel different week to week, and cravings that follow a cycle. Women are searching for answers they rarely see posted.',
    facets:{
      beauty:{b:'Perimenopause skin, starting in your 30s', p:'Searched 3.5× more than posted. Dryness and jawline breakouts lead.'},
      exercise:{b:'Training with your cycle', p:'The most searched workout question this quarter. Evidence is still early.'},
      nutrition:{b:'Cravings and bloat follow your cycle', p:'Magnesium and “why am I so bloated” cluster in the week before a period.'},
      sleep:{b:'The 3am wake-up', p:'Night waking is searched 3.3× more than posted, often alongside “perimenopause”.'}
    },
    asking:[{q:'Why did my skin change at 38?', mult:'3.5×'},{q:'How should I work out during each phase of my cycle?', mult:'3×'},{q:'Why is my hair shedding after stopping the pill?', mult:'2.8×'}],
    todo:['Track one month of skin, energy and cravings together.','Plan lighter training days where you need them.','Bring patterns, not just symptoms, to your doctor.']
  },
  recovery:{
    name:'Recovery', topics:['exercise','beauty','sleep'], grad:'linear-gradient(135deg,var(--exercise) 0%,#7a5cff 60%,var(--beauty) 100%)',
    stat:'+38%', statLine:'more posts about rest days than a year ago',
    lede:'Rest has become the new effort. In fitness it is sleep scores and sauna; in beauty it is “barrier repair” and doing less. The same idea runs through both: stop stacking and let your body recover.',
    facets:{
      exercise:{b:'Rest days posted like PRs', p:'Recovery scores and sauna sessions are shared like workouts.'},
      beauty:{b:'Barrier repair over actives', p:'Fewer products, gentler routines and calm skin as the goal.'},
      sleep:{b:'Sleep is the base of both', p:'Sleep scores decide rest days, and “beauty sleep” is back as a real routine.'}
    },
    asking:[{q:'How many rest days do I need?', mult:'1.8×'},{q:'Is my skin barrier damaged?', mult:'2.1×'}],
    todo:['Take at least one full rest day a week.','Cut actives to two or three nights a week.','Protect sleep first; it helps both.']
  }
};

const QUILT = [
  {t:'Protein fatigue is real. Fiber is taking its place.', why:'Your Nutrition issue’s biggest story.', topics:['nutrition'], open:['issue','nutrition']},
  {t:'Hormones are this week’s common thread.', why:'Cycle-synced training and perimenopause skin are both searched far more than posted.', topics:['exercise','beauty'], open:['thread','hormones']},
  {t:'GLP-1s are quietly changing food, faces and the gym.', why:'It shows up in all three of your issues.', topics:['nutrition','beauty','exercise'], open:['thread','glp1']}
];

window.WHOLE_DATA = {TOPICS, THREADS, QUILT};
})();
