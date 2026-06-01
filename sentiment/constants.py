# --- 2a. Emoji → sentiment-descriptive text ------------------
EMOJI_MAP = {
    "💪": " strong motivated energetic ",
    "🔥": " on fire pumped energetic ",
    "😤": " determined aggressive motivated ",
    "🏋️": " lifting weights training hard ",
    "🏆": " champion winning achieving goal ",
    "🎯": " focused goal crushing it ",
    "⚡": " powerful energetic explosive ",
    "😊": " happy positive feeling good ",
    "😁": " very happy excited positive ",
    "😃": " excited enthusiastic positive ",
    "😍": " loving it very positive ",
    "🤩": " amazing super excited positive ",
    "👍": " good positive approved ",
    "❤️":  " love positive happy ",
    "🥳": " celebrating winning positive ",
    "😒": " disappointed unhappy negative ",
    "😔": " sad down feeling low ",
    "😩": " exhausted drained very tired ",
    "😫": " depleted burnt out negative ",
    "😢": " sad upset emotional negative ",
    "😭": " very sad crying very negative ",
    "😴": " sleepy tired low energy ",
    "🥱": " bored lazy unmotivated ",
    "🤒": " sick ill cannot train ",
    "🤮": " very sick unwell negative ",
    "💔": " heartbroken sad demotivated ",
    "👎": " bad negative disapprove ",
    "😐": " okay neutral normal average ",
    "😑": " blank neutral indifferent ",
}

# --- 2b. Gym / Fitness Slang → expanded meaning --------------
GYM_SLANG = {
    # High-energy / Positive
    "beast mode"    : "extremely motivated training at maximum intensity",
    "beastmode"     : "extremely motivated training at maximum intensity",
    "killing it"    : "performing excellently great progress",
    "crushing it"   : "performing excellently great progress",
    "on fire"       : "feeling energetic performing great",
    "new pr"        : "achieved personal record great accomplishment",
    "new pb"        : "achieved personal best great accomplishment",
    "hit a pr"      : "achieved personal record very happy",
    "hit a pb"      : "achieved personal best very happy",
    "pr"            : "personal record achievement",
    "pb"            : "personal best achievement",
    "gains"         : "muscle progress improvement positive",
    "gainz"         : "muscle progress improvement positive",
    "swole"         : "very muscular strong positive",
    "jacked"        : "very muscular strong positive",
    "shredded"      : "very lean and fit positive",
    "ripped"        : "very lean muscular positive",
    "pump"          : "great muscle pump feeling energized",
    "sweat session" : "intense workout very positive",
    "grind mode"    : "working hard consistently motivated",
    "hustle"        : "working hard motivated positive",
    "no days off"   : "training every day very motivated",
    "leg day"       : "leg training day workout",
    "push day"      : "push muscle group training",
    "pull day"      : "pull muscle group training",
    "hiit"          : "high intensity interval training",
    "bulk"          : "muscle building eating more phase",
    "bulking"       : "muscle building eating more phase",
    "lean bulk"     : "clean muscle building controlled diet",
    "cut"           : "fat loss diet phase",
    "cutting"       : "fat loss diet phase",
    "recomp"        : "muscle recomposition body transformation",
    "macros"        : "macronutrients balanced nutrition",
    "macro"         : "macronutrient balanced nutrition",
    "cheat meal"    : "planned break from diet okay",
    "cheat day"     : "planned diet break acceptable",
    "refeed"        : "planned high carbohydrate recovery day",
    "natty"         : "natural training no performance drugs",
    "compound"      : "compound movement heavy exercise",
    "superset"      : "back to back exercise technique",
    "dropset"       : "drop set advanced technique",
    "burnout set"   : "high rep burnout training hard",

    # Low-energy / Negative
    "skipping gym"  : "missing workout not going to gym",
    "missed gym"    : "skipped workout session negative",
    "no motivation" : "unmotivated depressed not feeling gym",
    "burnt out"     : "exhausted overtrained very fatigued",
    "overtrained"   : "too much training body exhausted",
    "overtraining"  : "too much training body exhausted",
    "injured"       : "hurt injured unable to train",
    "injury"        : "hurt injured pain unable to train",
    "sore af"       : "extremely sore muscle soreness pain",
    "doms"          : "delayed onset muscle soreness recovery needed",
    "plateau"       : "stuck no progress frustrated",
    "binge"         : "ate too much unhealthy food negative",
    "binging"       : "eating too much unhealthy negative",
    "cheat week"    : "whole week off diet negative",
    "deload"        : "rest recovery reduced training week",
    "rest day"      : "planned rest recovery day",

    # Neutral / Maintenance
    "bulk season"   : "muscle building phase training",
    "gym rat"       : "dedicated gym person consistent",
    "cardio"        : "cardiovascular exercise training",
    "fasted cardio" : "morning empty stomach cardiovascular training",
    "pre workout"   : "pre workout energy supplement training",
    "post workout"  : "post workout recovery nutrition",
    "protein shake" : "protein supplement recovery drink",
    "whey"          : "whey protein supplement",
    "creatine"      : "creatine strength supplement",
    "reps"          : "repetitions exercise",
    "sets"          : "training sets",
}

# --- 2c. Roman Urdu (Pakistani gym / daily slang) -----------
ROMAN_URDU = {
    # Positive
    "mast workout"      : "great excellent workout feeling positive",
    "mast training"     : "great excellent training feeling positive",
    "maza aa gaya"      : "enjoyed it feeling great very positive",
    "achi feeling"      : "feeling good positive satisfied",
    "bohat acha"        : "very good feeling positive",
    "josh aa gaya"      : "feeling pumped energized very motivated",
    "motivated hun"     : "feeling very motivated ready to train",
    "motivated hoon"    : "feeling very motivated ready to train",
    "jeet gaya"         : "won achieved feeling great positive",
    "jeet gayi"         : "won achieved feeling great positive",
    "mein karunga"      : "i will do it determined motivated",
    "mein karonga"      : "i will do it determined motivated",
    "bohat khushi"      : "very happy feeling great positive",
    "khushi hai"        : "feeling happy positive",
    "full josh"         : "full energy very motivated ready",
    "full energy"       : "very energetic motivated ready to train",
    "game on"           : "ready determined very motivated",
    "uthao weights"     : "lift weights training motivated",

    # Negative
    "thak gaya"         : "feeling very exhausted tired cannot train",
    "thak gayi"         : "feeling very exhausted tired cannot train",
    "bahut thaka"       : "extremely tired exhausted drained",
    "bahut thaki"       : "extremely tired exhausted drained",
    "bohat thaka"       : "extremely tired exhausted drained",
    "body sore hai"     : "body is sore aching recovery needed",
    "dard ho raha"      : "body is paining sore uncomfortable",
    "dard ho rahi"      : "body is paining sore uncomfortable",
    "bura lag raha"     : "feeling bad negative low mood",
    "bura lag rahi"     : "feeling bad negative low mood",
    "demotivated hun"   : "feeling demotivated negative not motivated",
    "demotivated hoon"  : "feeling demotivated negative not motivated",
    "kuch nahi karna"   : "do not want to do anything very low motivation",
    "gym nahi gaya"     : "missed gym skipped workout negative",
    "gym nahi gayi"     : "missed gym skipped workout negative",
    "gym nahi jaon ga"  : "not going to gym skipping workout",
    "gym nahi jaon gi"  : "not going to gym skipping workout",
    "haar gaya"         : "lost defeated feeling negative disappointed",
    "haar gayi"         : "lost defeated feeling negative disappointed",
    "nirasha"           : "disappointed hopeless negative",
    "bohat bura"        : "feeling very bad very negative",
    "bilkul man nahi"   : "absolutely no motivation very negative",
    "uthne ka man nahi" : "do not want to get up lazy negative",

    # ── "gy" endings (colloquial Pakistani — gender-neutral past tense) ──
    # e.g. "haar gy" = "we/they lost"  |  "jeet gy" = "we/they won"
    # These differ from formal "gaya/gayi" but are extremely common in chat
    "haar gy"           : "lost defeated feeling negative disappointed",
    "jeet gy"           : "won achieved feeling great positive",
    "thak gy"           : "feeling very exhausted tired cannot train",
    "uth gy"            : "got up started feeling okay",
    "gir gy"            : "fell down failed feeling negative",
    "ruk gy"            : "stopped gave up feeling negative",
    "bhaag gy"          : "ran away escaped okay",
    "gym nahi gy"       : "missed gym skipped workout negative",
    "aa gy"             : "came arrived feeling okay",
    "kr gy"             : "did it accomplished feeling positive",
    "kar gy"            : "did it accomplished feeling positive",
    "ho gy"             : "it happened done okay neutral",
    "ho gya"            : "it happened done okay neutral",
    "ho gyi"            : "it happened done okay neutral",
    "mar gy"            : "exhausted totally drained very negative",

    # Filler / Neutral connectors
    "yr"                : "friend",
    "yaar"              : "friend",
    "bhai"              : "brother friend",
    "yar"               : "friend",
    "kal"               : "yesterday tomorrow",
}

EXPLICIT_OVERRIDES = [

    # ── Explicit Negative overrides ──────────────────────────
    (r'\b(no motivation|zero motivation|lost all motivation|can\'t train|cant train)\b',
     "Negative"),
    (r'\b(feel(ing)?\s+(terrible|awful|horrible|miserable|depressed|crushed|broken))\b',
     "Negative"),
    (r'\b(worst day|bad day|really bad|very bad|feeling bad)\b',
     "Negative"),

    # ── Explicit Neutral overrides ────────────────────────────
    (r'\b(feel(ing)?\s+neutral)\b',                         "Neutral"),
    (r'\b(just\s+okay|just\s+ok|feeling\s+ok(ay)?)\b',     "Neutral"),
    (r'\b(meh|average day|average today|so[\s-]so|nothing special)\b',
     "Neutral"),
    (r'\b(okay\s+aaj|thek\s+hai|theek\s+hai|normal\s+day|bas\s+theek)\b',
     "Neutral"),
    (r'\b(not\s+great\s+not\s+bad|not\s+bad\s+not\s+great)\b',
     "Neutral"),
    (r'\b(maintenance\s+(mode|day)|steady\s+state|cruise\s+control)\b',
     "Neutral"),

    # ── Explicit Positive overrides ──────────────────────────
    (r'\b(best day|greatest day|absolutely amazing|on top of the world)\b',
     "Positive"),
]

WORKOUT_PLANS = {

    "Positive": {
        "mode"       : "💪 Beast Mode — High Intensity",
        "description": "You're fired up. Chase that PR, go heavy, and make today count.",
        "exercises"  : [
            {"exercise": "Barbell Back Squat",        "sets": 5, "reps": "5",      "note": "Attempt a PR if energy is high"},
            {"exercise": "Deadlift",                  "sets": 4, "reps": "6",      "note": "Compound king — max effort today"},
            {"exercise": "Bench Press",               "sets": 4, "reps": "8",      "note": "Add 2.5–5 kg from last session"},
            {"exercise": "Weighted Pull-Ups",         "sets": 4, "reps": "8–10",   "note": "Add weight if bodyweight feels easy"},
            {"exercise": "Overhead Press",            "sets": 3, "reps": "6–8",    "note": "Full lockout at the top"},
            {"exercise": "HIIT Finisher (sprints)",   "sets": 1, "reps": "20 min", "note": "All-out effort — battle ropes or treadmill"},
        ],
        "intensity"  : "High (85–100% 1RM on compounds)",
        "rest_period": "60–90 sec between sets",
        "tips"       : [
            "Keep rest short to stay in the zone.",
            "Prioritise compound lifts — max hormonal response.",
            "Take creatine pre-workout if supplementing.",
            "Record every set — today is a PR-chasing day.",
        ],
    },

    "Neutral": {
        "mode"       : "🏋️ Steady Grind — Standard Training",
        "description": "Feeling average? Good. Champions are built on consistent ordinary days.",
        "exercises"  : [
            {"exercise": "Dumbbell Lunges",       "sets": 3, "reps": "12 each", "note": "Focus on controlled descent"},
            {"exercise": "Lat Pulldown",          "sets": 3, "reps": "12",      "note": "Full range, slow eccentric"},
            {"exercise": "Incline DB Press",      "sets": 3, "reps": "10–12",   "note": "Moderate weight, mind-muscle"},
            {"exercise": "Cable Rows",            "sets": 3, "reps": "12",      "note": "Squeeze at peak contraction"},
            {"exercise": "Dumbbell Shoulder Press","sets": 3, "reps": "12",     "note": "No momentum, strict form"},
            {"exercise": "Treadmill / Zone-2 Cardio","sets":1,"reps": "30 min", "note": "Conversational pace"},
        ],
        "intensity"  : "Moderate (70–80% 1RM)",
        "rest_period": "90–120 sec between sets",
        "tips"       : [
            "Apply 2.5% progressive overload from last week.",
            "Log your weights — small wins add up.",
            "Neutral days build the habit. Show up.",
        ],
    },

    "Negative": {
        "mode"       : "🧘 Recovery Mode — Active Rest",
        "description": "Feeling down or drained. Your body and mind need care. Moving gently IS progress.",
        "exercises"  : [
            {"exercise": "Slow-pace Walking / Light Treadmill", "sets": 1, "reps": "20–30 min", "note": "Easy stroll, no pressure"},
            {"exercise": "Full-Body Yoga / Stretching",         "sets": 1, "reps": "15–20 min", "note": "Deep breathing, hold each stretch 30 sec"},
            {"exercise": "Foam Rolling",                        "sets": 1, "reps": "10–15 min", "note": "Quads, lats, thoracic spine, calves"},
            {"exercise": "Bodyweight Exercises (optional)",     "sets": 2, "reps": "10",        "note": "Push-ups / air squats only if you feel up to it"},
            {"exercise": "Box Breathing / Meditation",          "sets": 1, "reps": "10 min",    "note": "4-4-4-4 breathing — stress & cortisol relief"},
        ],
        "intensity"  : "Low (bodyweight / mobility only)",
        "rest_period": "As needed — no rush",
        "tips"       : [
            "Rest IS training. Skipping heavy work today protects tomorrow.",
            "Prioritise 7–9 hours of sleep tonight.",
            "Even 10 minutes of movement improves mood.",
            "Talk to your gym buddy — social support matters.",
        ],
    },
}

DIET_PLANS = {

    "Positive": {
        "mode"       : "🍗 Gains Fuel — High-Performance Diet",
        "description": "You're in beast mode — fuel hard, recover harder.",
        "meals"      : [
            {
                "timing": "Pre-Workout  (90 min before)",
                "foods" : ["Oats + banana + honey",
                           "2 boiled eggs",
                           "Black coffee or green tea"],
                "macros": "~500 kcal | P: 25g | C: 70g | F: 10g",
            },
            {
                "timing": "Post-Workout  (within 30 min)",
                "foods" : ["Whey protein shake (1–2 scoops)",
                           "Banana or 4–5 dates  (fast carbs)",
                           "Peanut butter toast"],
                "macros": "~450 kcal | P: 40g | C: 50g | F: 8g",
            },
            {
                "timing": "Lunch",
                "foods" : ["Grilled chicken breast 200g",
                           "Brown rice or sweet potato",
                           "Mixed salad + olive oil"],
                "macros": "~650 kcal | P: 45g | C: 65g | F: 15g",
            },
            {
                "timing": "Dinner",
                "foods" : ["Salmon or tuna 200g",
                           "Quinoa or whole-wheat roti",
                           "Steamed broccoli + spinach"],
                "macros": "~600 kcal | P: 42g | C: 50g | F: 18g",
            },
        ],
        "hydration"    : "3.5–4 L water + electrolytes during workout",
        "supplements"  : ["Creatine 5g/day", "Whey Protein", "Multivitamin"],
        "key_principle": "Aim for 1.8–2.2g protein per kg bodyweight. Time carbs around your workout.",
    },

    "Neutral": {
        "mode"       : "🥗 Balanced Macros — Maintenance Diet",
        "description": "Consistent clean eating is the boring secret nobody talks about.",
        "meals"      : [
            {
                "timing": "Breakfast",
                "foods" : ["3 eggs (whole or 2 whole + 2 whites)",
                           "Whole-wheat toast",
                           "Glass of milk or dahi"],
                "macros": "~400 kcal | P: 28g | C: 40g | F: 12g",
            },
            {
                "timing": "Lunch",
                "foods" : ["Chicken or dal (lentil soup)",
                           "2 whole-wheat rotis or 1 cup rice",
                           "Salad or raita"],
                "macros": "~550 kcal | P: 35g | C: 60g | F: 10g",
            },
            {
                "timing": "Snack",
                "foods" : ["Mixed nuts 30g",
                           "Greek yogurt / plain dahi",
                           "Apple or banana"],
                "macros": "~300 kcal | P: 12g | C: 35g | F: 12g",
            },
            {
                "timing": "Dinner",
                "foods" : ["Baked / grilled chicken or fish",
                           "Vegetable stir-fry",
                           "Brown rice or whole-wheat roti"],
                "macros": "~550 kcal | P: 38g | C: 50g | F: 14g",
            },
        ],
        "hydration"    : "2.5–3 L water daily",
        "supplements"  : ["Whey Protein (if intake is short)", "Multivitamin"],
        "key_principle": "Track macros 2–3 days a week to spot gaps. Variety in vegetables.",
    },

    "Negative": {
        "mode"       : "🌿 Recovery & Comfort — Anti-Inflammatory Diet",
        "description": "Eat to heal. Nourish your body and protect your mood.",
        "meals"      : [
            {
                "timing": "Breakfast",
                "foods" : ["Oatmeal + berries + honey",
                           "Chamomile or ginger tea",
                           "Banana"],
                "macros": "~350 kcal | P: 10g | C: 65g | F: 5g",
            },
            {
                "timing": "Lunch",
                "foods" : ["Warm chicken soup OR dal (lentil)",
                           "Light roti or crackers",
                           "Steamed soft vegetables"],
                "macros": "~450 kcal | P: 28g | C: 50g | F: 10g",
            },
            {
                "timing": "Snack",
                "foods" : ["Dark chocolate 2–3 squares (70%+)",
                           "Mixed nuts",
                           "Herbal tea (no caffeine)"],
                "macros": "~250 kcal | P: 6g | C: 25g | F: 15g",
            },
            {
                "timing": "Dinner",
                "foods" : ["Khichdi (rice + dal — comfort meal)",
                           "Plain dahi / yogurt",
                           "Light kachumber salad"],
                "macros": "~450 kcal | P: 20g | C: 65g | F: 8g",
            },
        ],
        "hydration"    : "3 L water + ginger-honey tea + coconut water",
        "supplements"  : ["Vitamin D (mood support)", "Magnesium (stress & sleep)", "Omega-3"],
        "key_principle": "Dark chocolate → serotonin. Limit caffeine (raises cortisol). "
                         "Anti-inflammatory foods: turmeric, ginger, berries.",
    },
}

MESSAGES = {
    "Positive": (
        "🔥 BRO YOU'RE IN BEAST MODE! "
        "Go shatter that PR — make today legendary. Let's get it!"
    ),
    "Neutral": (
        "💪 Steady grind, bhai. "
        "Champions are forged on average days. Stay consistent — the gains are coming."
    ),
    "Negative": (
        "💙 Hey, it's okay. Even GOATs have tough days. "
        "Take care of yourself today — you'll be back stronger. This feeling is temporary."
    ),
}

LABELS = ["Negative", "Neutral", "Positive"]
