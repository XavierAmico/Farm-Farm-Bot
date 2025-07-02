import os
import discord
import pearldb as p
import servercommands as sc
from discord.ext import commands

# Instantiates the bot using these intents, name and calls for the discord bot's key
authKey = os.environ["AUTH_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]
intents = discord.Intents.default()
intents.message_content = True  # Needed to read message content
bot = commands.Bot(command_prefix="!", intents=intents)

# info sent to console to confirm bot is up and running
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

# General Commands

# cmds, makes a call to the message that displays the info regarding use of the bot
@bot.command()
async def cmds(ctx):
    server = ctx.guild.name
    await ctx.send(sc.cmds(server))

@bot.command()
async def modcmds(ctx):
    server = ctx.guild.name
    await ctx.send(sc.mod_cmds(server))
# Pearl Commands

# Add pearl, first makes checks to ensure user is in the correct channel, using a color, and is not a duplicate
# Then makes a call to the SQL database using the color, x and y coordinates, and server name

@bot.command()
async def addpearl(ctx, color: str, x: int, y: int):
    server = ctx.guild.name
    color = color.capitalize()

    if correct_channel(ctx):
        if color not in p.colors:
            await ctx.send("❌ Pearl color does not exists.")
        elif p.is_duplicate(color, x ,y, server):
            await ctx.send("❌ Pearl already logged today.")
        else:
            p.add(color,x,y,server)
            await ctx.send(f"✅ {color} pearl has been added.")
    else:
        await ctx.send(f"❌ This command can only be used in #{sc.get_pearl_chat(server)}. (Request Access if needed).")
@bot.command()
async def ap(ctx, color: str, x: int, y: int):
    await addpearl(ctx,color,x,y)

# Remove Pearl, checks to make sure that the channel is correct, then that the pearl exist
# It then removes the pearl from the SQL table and sends back a message
@bot.command()
async def removepearl(ctx, x: int, y: int):
    server = ctx.guild.name
    if correct_channel(ctx):
        if p.remove(x, y, server):
            await ctx.send(f"✅ Pearl at ({x}, {y}) has been removed.")
        else:
            await ctx.send("⚠️ No matching pearl to remove.")
    else:
        await ctx.send(f"❌ This command can only be used in #{sc.get_pearl_chat(server)}. (Request Access if needed).")

@bot.command()
async def rmp(ctx, x: int, y: int):
    await removepearl(ctx,x,y)

# Mod Command
@bot.command()
async def clearall(ctx):
    server = ctx.guild.name
    if any(role.name == sc.get_mod_role(server) for role in ctx.author.roles):
        p.clear(server)
        await ctx.send("All pearls have been cleared!")
    else:
        await ctx.send(f"❌ You do not have permissions to do this. ({sc.get_mod_role(server)})")

# Pearls, checks the channel, makes a call to the SQL db to create a list of pearls for that server
# The pearls are then grouped by color, sorted, and presented as groups in the message sent to the user
@bot.command()
async def pearls(ctx):
    server = ctx.guild.name
    if correct_channel(ctx):
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
    else:
        await ctx.send(f"❌ This command can only be used in #{sc.get_pearl_chat(server)}. (Request Access if needed).")

@bot.command()
async def pl(ctx):
    await pearls(ctx)
#Admin Command
@bot.command()
@commands.has_permissions(administrator=True)
async def modrole(ctx, role: str):
    server = ctx.guild.name
    sc.set_mod_role(role, server)
    await ctx.send(f"The Moderator role has been updated to {sc.get_mod_role(server)}!")

#Mod Command
@bot.command()
async def pearlchat(ctx, chat: str):
    server = ctx.guild.name
    if any(role.name == sc.get_mod_role(server) for role in ctx.author.roles):
        sc.set_pearl_chat(chat, server)
        await ctx.send(f"Pearl Chat has been updated to #{sc.get_pearl_chat(server)}!")
    else:
        await ctx.send(f"❌ You do not have permissions to do this. ({sc.get_pearl_chat(server)})")

# Utility
def correct_channel(ctx):
    server = ctx.guild.name
    if ctx.channel.name != sc.get_pearl_chat(server):
        return False
    else:
        return True
# I mean yeah bro it runs the bot

bot.run(authKey)
