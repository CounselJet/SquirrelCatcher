"""
Database module for Squirrel Catcher bot.
Uses asyncpg with PostgreSQL for persistent player data storage.
"""

import json
import asyncpg

pool: asyncpg.Pool | None = None

DEFAULT_PLAYER = {
    "acorns": 0,
    "silver_acorns": 0,
    "emerald_acorns": 0,
    "golden_acorns": 0,
    "catches": {},
    "total_catches": 0,
    "junk_catches": 0,
    "level": 1,
    "xp": 0,
    "last_daily": None,
}


async def init_db(database_url: str):
    """Create connection pool and ensure the players table exists."""
    global pool
    pool = await asyncpg.create_pool(database_url)
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS players (
                user_id TEXT PRIMARY KEY,
                acorns INTEGER DEFAULT 0,
                silver_acorns INTEGER DEFAULT 0,
                emerald_acorns INTEGER DEFAULT 0,
                golden_acorns INTEGER DEFAULT 0,
                total_catches INTEGER DEFAULT 0,
                junk_catches INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                last_daily TIMESTAMPTZ,
                catches JSONB DEFAULT '{}'
            )
        """)


def _row_to_dict(row: asyncpg.Record) -> dict:
    """Convert a database row to a player dict matching the old JSON format."""
    catches = row["catches"]
    if isinstance(catches, str):
        catches = json.loads(catches)
    return {
        "acorns": row["acorns"],
        "silver_acorns": row["silver_acorns"],
        "emerald_acorns": row["emerald_acorns"],
        "golden_acorns": row["golden_acorns"],
        "total_catches": row["total_catches"],
        "junk_catches": row["junk_catches"],
        "level": row["level"],
        "xp": row["xp"],
        "last_daily": row["last_daily"].isoformat() if row["last_daily"] else None,
        "catches": catches,
    }


async def get_player(user_id: str) -> dict:
    """Fetch a player by user_id. Creates a default row if not found."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM players WHERE user_id = $1", user_id)
        if row is None:
            await conn.execute("INSERT INTO players (user_id) VALUES ($1)", user_id)
            return dict(DEFAULT_PLAYER)
        return _row_to_dict(row)


async def update_player(user_id: str, player: dict):
    """Upsert a player row from a player dict."""
    last_daily = None
    if player.get("last_daily"):
        from datetime import datetime, timezone
        ld = player["last_daily"]
        if isinstance(ld, str):
            dt = datetime.fromisoformat(ld)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            last_daily = dt
        else:
            last_daily = ld

    catches_json = json.dumps(player.get("catches", {}))

    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO players (user_id, acorns, silver_acorns, emerald_acorns, golden_acorns,
                                 total_catches, junk_catches, level, xp, last_daily, catches)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11::jsonb)
            ON CONFLICT (user_id) DO UPDATE SET
                acorns = EXCLUDED.acorns,
                silver_acorns = EXCLUDED.silver_acorns,
                emerald_acorns = EXCLUDED.emerald_acorns,
                golden_acorns = EXCLUDED.golden_acorns,
                total_catches = EXCLUDED.total_catches,
                junk_catches = EXCLUDED.junk_catches,
                level = EXCLUDED.level,
                xp = EXCLUDED.xp,
                last_daily = EXCLUDED.last_daily,
                catches = EXCLUDED.catches
            """,
            user_id,
            player.get("acorns", 0),
            player.get("silver_acorns", 0),
            player.get("emerald_acorns", 0),
            player.get("golden_acorns", 0),
            player.get("total_catches", 0),
            player.get("junk_catches", 0),
            player.get("level", 1),
            player.get("xp", 0),
            last_daily,
            catches_json,
        )


async def load_all_players() -> dict:
    """Load all players as a dict keyed by user_id (for leaderboard)."""
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM players")
    return {row["user_id"]: _row_to_dict(row) for row in rows}


async def close_db():
    """Close the connection pool."""
    global pool
    if pool:
        await pool.close()
        pool = None
