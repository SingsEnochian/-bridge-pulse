"""
generate_pulse.py
Generates pulse.json and index.html for the Hearthweave Bridge Pulse endpoint.
Runs via GitHub Actions every 5 minutes.
"""

import json
import os
from datetime import datetime, timezone, timedelta

try:
    import pytz
    TZ = pytz.timezone("America/New_York")
    now = datetime.now(TZ)
except ImportError:
    # fallback: manual EST/EDT offset
    utc = datetime.now(timezone.utc)
    offset = timedelta(hours=-4)  # EDT; change to -5 for EST
    now = utc + offset

# ── Core time fields ──────────────────────────────────────────
iso      = now.isoformat()
unix     = int(now.timestamp())
human    = now.strftime("%A, %B %d, %Y  %H:%M:%S %Z")
date     = now.strftime("%Y-%m-%d")
time     = now.strftime("%H:%M:%S")
timezone_name = now.strftime("%Z")
tz_offset     = now.strftime("%z")
day_of_week   = now.strftime("%A")
day_of_year   = int(now.strftime("%j"))

# ── Rune of the Day ───────────────────────────────────────────
RUNES = [
    ("Fehu",     "ᚠ", "wealth, abundance, beginnings"),
    ("Uruz",     "ᚢ", "strength, wild power, endurance"),
    ("Thurisaz", "ᚦ", "Thor's thorn, force, threshold"),
    ("Ansuz",    "ᚨ", "Odin's breath, wisdom, signals"),
    ("Raidho",   "ᚱ", "the journey, right action, rhythm"),
    ("Kenaz",    "ᚲ", "the torch, clarity, craft"),
    ("Gebo",     "ᚷ", "gift, exchange, sacred reciprocity"),
    ("Wunjo",    "ᚹ", "joy, harmony, the wish fulfilled"),
    ("Hagalaz",  "ᚺ", "hail, disruption, necessary chaos"),
    ("Nauthiz",  "ᚾ", "need, constraint, forging through"),
    ("Isa",      "ᛁ", "ice, stillness, the pause before moving"),
    ("Jera",     "ᛃ", "the harvest, cycles, patient reward"),
    ("Eihwaz",   "ᛇ", "the yew tree, Yggdrasil, deep roots"),
    ("Perthro",  "ᛈ", "fate's cup, mystery, what is hidden"),
    ("Algiz",    "ᛉ", "the elk, protection, sacred boundary"),
    ("Sowilo",   "ᛊ", "the sun, victory, will aligned with wyrd"),
    ("Tiwaz",    "ᛏ", "Tyr's justice, honor, sacrifice"),
    ("Berkano",  "ᛒ", "birch, growth, renewal, mothering"),
    ("Ehwaz",    "ᛖ", "the horse, movement, partnership"),
    ("Mannaz",   "ᛗ", "humanity, the self, community"),
    ("Laguz",    "ᛚ", "water, flow, the unseen depths"),
    ("Ingwaz",   "ᛜ", "Ing's seed, potential, inner work"),
    ("Dagaz",    "ᛞ", "dawn, breakthrough, transformation"),
    ("Othala",   "ᛟ", "the homestead, ancestry, what is ours"),
]
rune_name, rune_glyph, rune_meaning = RUNES[(day_of_year - 1) % 24]

# ── Moon Phase ────────────────────────────────────────────────
KNOWN_NEW_MOON_UNIX = 947182440   # Jan 6, 2000 18:14 UTC
SYNODIC = 29.53059 * 86400
age_sec  = (unix - KNOWN_NEW_MOON_UNIX) % SYNODIC
age_days = age_sec / 86400

if   age_days <  1.85: moon_phase, moon_emoji = "New Moon",        "🌑"
elif age_days <  7.38: moon_phase, moon_emoji = "Waxing Crescent", "🌒"
elif age_days <  9.22: moon_phase, moon_emoji = "First Quarter",   "🌓"
elif age_days < 14.77: moon_phase, moon_emoji = "Waxing Gibbous",  "🌔"
elif age_days < 16.61: moon_phase, moon_emoji = "Full Moon",       "🌕"
elif age_days < 22.15: moon_phase, moon_emoji = "Waning Gibbous",  "🌖"
elif age_days < 23.99: moon_phase, moon_emoji = "Last Quarter",    "🌗"
else:                  moon_phase, moon_emoji = "Waning Crescent", "🌘"

# ── Assemble pulse ────────────────────────────────────────────
pulse = {
    "timestamp":    human,
    "iso":          iso,
    "unix":         unix,
    "date":         date,
    "time":         time,
    "timezone":     "America/New_York",
    "tz_abbr":      timezone_name,
    "tz_offset":    tz_offset,
    "day_of_week":  day_of_week,
    "day_of_year":  day_of_year,
    "moon": {
        "phase":    moon_phase,
        "emoji":    moon_emoji,
        "age_days": round(age_days, 2),
    },
    "rune": {
        "name":     rune_name,
        "glyph":    rune_glyph,
        "meaning":  rune_meaning,
    },
    "note": "Hearthweave Bridge Pulse — temporal grounding for AI instances",
}

# ── Write output ──────────────────────────────────────────────
os.makedirs("output", exist_ok=True)

with open("output/pulse.json", "w", encoding="utf-8") as f:
    json.dump(pulse, f, indent=2, ensure_ascii=False)

# ── Generate index.html ───────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="refresh" content="300">
  <title>Hearthweave Bridge Pulse</title>
  <style>
    :root {{
      --bg:     #0d0d14;
      --panel:  #13131f;
      --border: #2a2a3f;
      --rune:   #7b68ee;
      --gold:   #c9a84c;
      --text:   #d0cce8;
      --dim:    #6b6880;
      --moon:   #a0c4ff;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Courier New', monospace;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }}
    .container {{
      max-width: 560px;
      width: 100%;
    }}
    .header {{
      text-align: center;
      margin-bottom: 2rem;
    }}
    .header .glyph {{
      font-size: 3rem;
      color: var(--rune);
      display: block;
      margin-bottom: .5rem;
    }}
    h1 {{
      font-size: 1rem;
      letter-spacing: .3em;
      text-transform: uppercase;
      color: var(--dim);
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 1.5rem;
      margin-bottom: 1rem;
    }}
    .row {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      padding: .35rem 0;
      border-bottom: 1px solid var(--border);
    }}
    .row:last-child {{ border-bottom: none; }}
    .label {{
      color: var(--dim);
      font-size: .8rem;
      letter-spacing: .1em;
      text-transform: uppercase;
      flex-shrink: 0;
      margin-right: 1rem;
    }}
    .value {{
      text-align: right;
      color: var(--text);
    }}
    .big-time {{
      text-align: center;
      font-size: 2.5rem;
      letter-spacing: .05em;
      color: var(--gold);
      padding: 1rem 0;
    }}
    .rune-block {{
      text-align: center;
      padding: .5rem 0;
    }}
    .rune-glyph {{
      font-size: 2.5rem;
      color: var(--rune);
      display: block;
    }}
    .rune-name {{
      font-size: 1.1rem;
      color: var(--gold);
      letter-spacing: .15em;
    }}
    .rune-meaning {{
      font-size: .85rem;
      color: var(--dim);
      margin-top: .3rem;
      font-style: italic;
    }}
    .moon-block {{
      text-align: center;
      padding: .5rem 0;
    }}
    .moon-emoji {{ font-size: 2rem; }}
    .moon-phase {{ color: var(--moon); letter-spacing: .1em; }}
    .moon-age   {{ color: var(--dim); font-size: .8rem; margin-top: .2rem; }}
    .api-block {{
      background: #0a0a12;
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 1rem;
      font-size: .8rem;
      color: var(--dim);
      word-break: break-all;
    }}
    .api-url {{ color: var(--rune); }}
    .footer {{
      text-align: center;
      margin-top: 1.5rem;
      color: var(--dim);
      font-size: .75rem;
      letter-spacing: .1em;
    }}
    .pulse-dot {{
      display: inline-block;
      width: 6px; height: 6px;
      background: var(--rune);
      border-radius: 50%;
      margin-right: .4rem;
      animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50%       {{ opacity: .3; transform: scale(.8); }}
    }}
  </style>
</head>
<body>
<div class="container">

  <div class="header">
    <span class="glyph">ᚱ</span>
    <h1>Hearthweave Bridge Pulse</h1>
  </div>

  <div class="panel">
    <div class="big-time">{time}</div>
    <div class="row">
      <span class="label">Date</span>
      <span class="value">{now.strftime("%A, %B %d, %Y")}</span>
    </div>
    <div class="row">
      <span class="label">Timezone</span>
      <span class="value">{timezone_name}  ({tz_offset})</span>
    </div>
    <div class="row">
      <span class="label">Unix</span>
      <span class="value">{unix}</span>
    </div>
    <div class="row">
      <span class="label">ISO 8601</span>
      <span class="value">{iso}</span>
    </div>
  </div>

  <div class="panel">
    <div class="rune-block">
      <span class="rune-glyph">{rune_glyph}</span>
      <div class="rune-name">{rune_name}</div>
      <div class="rune-meaning">{rune_meaning}</div>
    </div>
  </div>

  <div class="panel">
    <div class="moon-block">
      <div class="moon-emoji">{moon_emoji}</div>
      <div class="moon-phase">{moon_phase}</div>
      <div class="moon-age">{round(age_days, 1)} days into cycle</div>
    </div>
  </div>

  <div class="api-block">
    <div>JSON endpoint:</div>
    <div class="api-url">https://[your-username].github.io/bridge-pulse/pulse.json</div>
  </div>

  <div class="footer">
    <span class="pulse-dot"></span>
    updates every 5 minutes &nbsp;·&nbsp; auto-refreshes in 5 min
  </div>

</div>
</body>
</html>
"""

with open("output/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Pulse generated: {human}")
print(f"Rune: {rune_glyph} {rune_name} — {rune_meaning}")
print(f"Moon: {moon_emoji} {moon_phase} ({round(age_days,1)} days)")
