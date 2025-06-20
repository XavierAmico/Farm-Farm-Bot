import os
import discord
import pearls as p
from discord.ext import commands

authKey = os.environ["AUTH_KEY"]

intents = discord.Intents.default()
intents.message_content = True  # Needed to read message content

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.command()
async def addpearl(ctx, color: str, x: int, y: int):
    try:
        if ctx.channel.name != "pearl-chat":
            await ctx.send("❌ This command can only be used in #pearl-chat.")
            return
        color = color.capitalize()
        if color not in p.colors:
            await ctx.send("❌ Pearl color does not exists.")
        elif p.is_duplicate(color, x ,y):
            await ctx.send("❌ Pearl already logged today.")
        else:
            p.add(color,x,y)
            await ctx.send(f"✅ {color} pearl has been added.")
    except Exception as e:
        print("Error in addpearl: ", e)
        await ctx.send("❌ Failed to add pearl.")

@bot.command()
async def pearls(ctx):
    if ctx.channel.name != "pearl-chat":
        await ctx.send("❌ This command can only be used in #pearl-chat.")
        return
    pearls = p.get_today_pearls()

    if not pearls:
        await ctx.send("📭 No pearls logged yet today.")
        return

    # Group pearls by color
    from collections import defaultdict
    grouped = defaultdict(list)
    for pearl in pearls:
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
        if ctx.channel.name != "pearl-chat":
            await ctx.send("❌ This command can only be used in #pearl-chat.")
            return

        if p.remove(x, y):
            await ctx.send(f"✅ Pearl at ({x}, {y}) has been removed.")
        else:
            await ctx.send("⚠️ No matching pearl found to remove.")
    except Exception as e:
        print("Error in removepearl:", e)
        await ctx.send("❌ Failed to remove pearl.")


bot.run(authKey)
