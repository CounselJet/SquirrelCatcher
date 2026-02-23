# 🐿️ Squirrel Catcher Bot

A Discord bot where you catch squirrels, collect acorns, and compete with friends!

## Quick Setup (5 minutes)

### 1. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application** → name it "Squirrel Catcher"
3. Go to **Bot** tab → click **Add Bot**
4. Turn ON **Message Content Intent** (under Privileged Gateway Intents)
5. Click **Reset Token** → copy your bot token

### 2. Invite to Your Server

1. Go to **OAuth2 → URL Generator**
2. Check scopes: `bot`, `applications.commands`
3. Check permissions: `Send Messages`, `Embed Links`, `Read Message History`
4. Copy the URL → open in browser → add to your server

### 3. Run the Bot

```bash
# Install dependency
pip install discord.py

# Set your token (Linux/Mac)
export DISCORD_BOT_TOKEN="your-token-here"

# Or on Windows
set DISCORD_BOT_TOKEN=your-token-here

# Run it!
python bot.py
```

Or just edit `bot.py` line 14 and paste your token directly (don't share the file after!).

## Commands

| Command | What it does |
|---------|-------------|
| `!sq catch` | Set a trap and catch a squirrel (or junk) |
| `!sq bag` | View your caught squirrels |
| `!sq balance` | Check your acorn currencies |
| `!sq profile` | Full player profile |
| `!sq exchange <amount>` | Convert 100 acorns → 1 silver acorn |
| `!sq exchange_silver <amount>` | Convert 10 silver → 1 emerald |
| `!sq exchange_emerald <amount>` | Convert 10 emerald → 1 golden |
| `!sq sell <squirrel name>` | Sell a squirrel for acorns |
| `!sq daily` | Claim daily acorn bonus |
| `!sq leaderboard` | Top catchers |
| `!sq bestiary` | All squirrel species + discovery status |
| `!sq help` | Show all commands |

## Squirrel Rarities

| Rarity | Examples | Drop Rate |
|--------|----------|-----------|
| ⬜ Common | Grey Squirrel, Red Squirrel, Chipmunk | ~70% |
| 🟢 Uncommon | Black Squirrel, White Squirrel, Fox Squirrel | ~20% |
| 🔵 Rare | Flying Squirrel, Albino Squirrel, Giant Squirrel | ~7% |
| 🟣 Epic | Crystal Squirrel, Shadow Squirrel | ~2% |
| 🟡 Legendary | Golden Squirrel, Cosmic Squirrel | ~0.5% |
| 🔴 Mythic | Mythic Nutcracker | ~0.1% |

## Currency

- 🌰 **Acorns** — base currency
- 🥈🌰 **Silver Acorns** — 100 acorns each
- 💚🌰 **Emerald Acorns** — 1,000 acorns each
- ✨🌰 **Golden Acorns** — 10,000 acorns each

## Features

- **Leveling system** — XP from catches, better loot at higher levels
- **Bestiary** — track all 14 species discoveries
- **Junk catches** — sometimes you get a stick instead of a squirrel
- **Cooldowns** — 10 second catch cooldown
- **Daily bonus** — scales with your level
- **Leaderboard** — compete with friends
- **Persistent data** — saved to `player_data.json`

## Hosting Tips

For 24/7 uptime, run on any cheap VPS, a Raspberry Pi, or use a free tier from Railway/Render/Fly.io.

---

*Happy squirrel hunting!* 🐿️🌰
