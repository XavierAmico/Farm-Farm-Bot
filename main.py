import os
import discord
import pearldb as p
from discord.ext import commands

authKey = os.environ["AUTH_KEY"]

pearl_chat = "pearl-chat"
intents = discord.Intents.default()
intents.message_content = True  # Needed to read message content

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@commands.has_role("Moderator")
@bot.command()
async def clearall(ctx):
    p.clear()
    await ctx.send("All pearls have been cleared!")

@bot.command()
async def cmds(ctx):
    help_text = (
        f"**🧭 Pearl Bot — Commands Help**\n"
        f"All commands must be used in the **#{pearl_chat}** channel.\n\n"
        "**🔹 !addpearl <color> <x> <y>**\n"
        "Logs a pearl’s color and coordinates for today (UTC).\n"
        "_Example: `!addpearl Blue 120 65`_\n\n"
        "**🔹 !removepearl <x> <y>**\n"
        "Removes a pearl at the specified coordinates from today.\n"
        "_Example: `!removepearl 34 77`_\n\n"
        "**🔹 !clearall**\n"
        "Moderator specific command that clears all pearls for the day.\n\n"
        "**🔹 !pearls**\n"
        "Lists all pearls logged for today, grouped by color.\n\n"
        "**🎨 Valid Colors:** Black, Blue, Cyan, Green, Magenta, Red, White, Yellow\n"
        "**🕐 Reset Time:** Pearl data resets daily at <t:1750723200:t> (00:00 UTC).\n\n"
        f"Use these commands only in #{pearl_chat} to avoid errors. 🧂"
    )
    await ctx.send(help_text)

@bot.command()
async def addpearl(ctx, color: str, x: int, y: int):
    server = ctx.guild.name
    color = color.capitalize()

    if ctx.channel.name != pearl_chat:
        await ctx.send("❌ This command can only be used in #pearl-chat. (Create a ticket to request access if needed.)")
        return

    if color not in p.colors:
        await ctx.send("❌ Pearl color does not exists.")
    elif p.is_duplicate(color, x ,y,server):
        await ctx.send("❌ Pearl already logged today.")
    else:
        p.add(color,x,y,server)
        await ctx.send(f"✅ {color} pearl has been added.")

@bot.command()
async def pearls(ctx):
    server = ctx.guild.name
    if ctx.channel.name != pearl_chat:
        await ctx.send("❌ This command can only be used in #pearl-chat. (Create a ticket to request access if needed.)")
        return

    pearl_list = p.get_pearls(server)

    if not pearl_list:
        await ctx.send("📭 No pearls logged yet today.")
        return

    # Group pearls by color
    from collections import defaultdict
    grouped = defaultdict(list)
    for pearl in pearl_list:
        color = pearl['color'].capitalize()
        grouped[color].append((pearl['x'], pearl['y']))

    # Sort by color name
    sorted_colors = sorted(grouped.keys())

    # Emoji mapping (optional, can add more!)
    emoji = {
        "Red": "🔴", "Blue": "🔵", "Green": "🟢", "Yellow": "🟡",
        "White": "⚪", "Black": "⚫", "Magenta": "🟣", "Cyan": "🔷"
    }

    lines = [f"## 📅 Pearls for {p.get_today()}:\n"]

    for color in sorted_colors:
        icon = emoji.get(color, "•")
        lines.append(f"{icon} {color}:")
        for x, y in grouped[color]:
            lines.append(f" - ({x}, {y})")
        lines.append("\n")

    await ctx.send("\n".join(lines))

@bot.command()
async def removepearl(ctx, x: int, y: int):
    try:
        server = ctx.guild.name
        if ctx.channel.name != pearl_chat:
            await ctx.send("❌ This command can only be used in #pearl-chat. (Create a ticket to request access if needed.)")
            return
        if p.remove(x, y, server):
            await ctx.send(f"✅ Pearl at ({x}, {y}) has been removed.")
        else:
            await ctx.send("⚠️ No matching pearl found to remove.")
    except Exception as e:
        print("Error in removepearl:", e)
        await ctx.send("❌ Failed to remove pearl.")

bot.run(authKey)
