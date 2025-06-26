from database import connect

def cmds(server):
    help_text = (
        f"**🧭 Pearl Bot — Commands Help**\n"
        f"All commands must be used in the **#{get_pearl_chat(server)}** channel.\n\n"
        "**🔹 !pearls**\n"
        "Lists all pearls logged for today, grouped by color.\n\n"
        "**🔹 !addpearl <color> <x> <y>**\n"
        "Logs a pearl’s color and coordinates for today (UTC).\n"
        "_Example: `!addpearl Blue 120 65`_\n\n"
        "**🔹 !removepearl <x> <y>**\n"
        "Removes a pearl at the specified coordinates from today.\n"
        "_Example: `!removepearl 34 77`_\n\n"
        "**🔹 !modcmds**\n"
        "Shows help for moderator specific commands.\n\n"
        "**🎨 Valid Colors:** Black, Blue, Cyan, Green, Magenta, Red, White, Yellow\n"
        "**🕐 Reset Time:** Pearl data resets daily at <t:1750723200:t> (00:00 UTC).\n\n"
        f"Use these commands only in #{get_pearl_chat(server)} to avoid errors. 🧂"
    )
    return help_text


def mod_cmds(server):
    pearl_chat = get_pearl_chat(server)
    help_text = (
        f"**🛠️ Pearl Bot — Moderator Commands**\n"
        f"These commands are restricted to users with the Moderator role.\n"
        f"All actions  should be used in **#{pearl_chat}** unless otherwise noted. (Though not restricted to it)\n\n"

        "🔹 **!modrole <role_name>**\n"
        "[Administrator only command]\n"
        "Sets which role has permission to use moderator-only bot commands.\n"
        "_Example: `!modrole PearlMaster`_\n\n"

        "🔹 **!pearlchat <channel_name>**\n"
        "Sets the name of the channel where pearl commands are allowed.\n"
        "_Example: `!pearlchat pearl-chat`_\n\n"

        "🔹 **!clearall**\n"
        "Removes **all logged pearls** for the current UTC day on this server.\n"
        "_Use with caution — this cannot be undone._\n\n"

        f"⚠️ These commands require the correct {get_mod_role(server)} role and should be used carefully in #{pearl_chat}.\n"
        f"For general commands, use `!cmds`. 🧭"
    )
    return help_text

def set_mod_role(role, server):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO settings (modrole, server)
            VALUES (%s, %s)
            ON CONFLICT (server) DO UPDATE
            SET modrole = EXCLUDED.modrole;         
            """, (role, server))
    conn.commit()

def get_mod_role(server):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT modrole
            FROM settings
            WHERE server = %s
            """, (server,))
            result = cur.fetchone()
            return result[0] if result else "Moderator"

def set_pearl_chat(pearl_chat, server):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO settings (pearl_chat, server)
                VALUES (%s, %s)
                ON CONFLICT (server) DO UPDATE
                SET pearl_chat = EXCLUDED.pearl_chat;           
            """, (pearl_chat, server))
    conn.commit()

def get_pearl_chat(server):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT pearl_chat
            FROM settings
            WHERE server = %s
            """, (server,))
            result = cur.fetchone()
            return result[0] if result else "pearl-chat"