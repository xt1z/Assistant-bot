import asyncio
import os
import random
from datetime import datetime, timedelta
from pytube import YouTube
import discord
import ffmpeg
import json
from discord.ext import commands
from discord import Activity, ActivityType
from keep_alive import keep_alive
keep_alive()

TOKEN = os.environ.get('TOKEN')
CHANNEL_ID = '1241258662237044777'
HOMEWORK_ID = '1241258296392945666'

intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

HOMEWORK_FILE = "homework.json"

def load_homework():
    if os.path.exists(HOMEWORK_FILE):
        try:
            with open(HOMEWORK_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error: Unable to decode JSON file. Returning empty dictionary.")
            return {}
    else:
        print("Homework file not found. Returning empty dictionary.")
        return {}

def save_homework(data):
    with open(HOMEWORK_FILE, "w") as file:
        json.dump(data, file)

homework_tracker = load_homework()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    activity = Activity(type=ActivityType.playing,
                        name="Skibidi toilet")
    await bot.change_presence(activity=activity)

@bot.command()
async def add_homework(ctx, subject: str, *, assignment: str):
    if str(ctx.channel.id) != HOMEWORK_ID:
        return
    if subject.lower() not in homework_tracker:
        homework_tracker[subject.lower()] = [assignment]
    else:
        homework_tracker[subject.lower()].append(assignment)

    await ctx.send(f'Homework assignment added for {subject}: {assignment}')
    save_homework(homework_tracker)

@bot.command()
async def list_homework(ctx):
    if str(ctx.channel.id) != HOMEWORK_ID:
        return
    if homework_tracker:
        for subject, assignments in homework_tracker.items():
            await ctx.send(f'📒**{subject.capitalize()}:**\n\n' +
                           '\n'.join(assignments))
    else:
        await ctx.send('No homework assignments tracked.')

@bot.command()
async def remove_homework(ctx, subject: str, *, assignment: str):
    if str(ctx.channel.id) != HOMEWORK_ID:
        return
    if subject.lower() in homework_tracker and assignment in homework_tracker[subject.lower()]:
        homework_tracker[subject.lower()].remove(assignment)
        await ctx.send(f'Homework assignment removed for {subject}: {assignment}')
        save_homework(homework_tracker)
    else:
        await ctx.send('Homework assignment not found.')

@bot.command()
async def hi(ctx):
    if str(ctx.channel.id) != CHANNEL_ID:
        return
    embed = discord.Embed(
        title="Hello I'm Assistant bot👻",
        description="this bot made by @__xtzzz",
        color=discord.Color.blue())
    embed.add_field(name="「👀」About me",
                    value="https://xt1z.github.io/araiwa/",
                    inline=False)
    embed.add_field(name="「📌」Objective for this bot",
                    value="help our community",
                    inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def cls(ctx, amount: int):
  # Check if the command was sent in the specified channel
  await ctx.channel.purge(limit=amount + 1)


@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
  # Check if the command was sent in the specified channel
  if str(ctx.channel.id) != CHANNEL_ID:
    return

  # Check if the user has the required permissions
  if ctx.author.guild_permissions.kick_members:
    await member.kick(reason=reason)
    if reason:
      await ctx.send(f'{member.mention} has been kicked for {reason}.')
    else:
      await ctx.send(f'{member.mention} has been kicked.')
  else:
    await ctx.send("You don't have permission to use this command.")


@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
  # Check if the command was sent in the specified channel
  if str(ctx.channel.id) != CHANNEL_ID:
    return

  # Check if the user has the required permissions
  if ctx.author.guild_permissions.ban_members:
    await member.ban(reason=reason)
    if reason:
      await ctx.send(f'{member.mention} has been banned for {reason}.')
    else:
      await ctx.send(f'{member.mention} has been banned.')
  else:
    await ctx.send("You don't have permission to use this command.")


@bot.command()
async def version(ctx):
  # Check if the command was sent in the specified channel
  if str(ctx.channel.id) != CHANNEL_ID:
    return

  # Create an embed message
  embed = discord.Embed(title="Version 1.2.0",
                      description="this bot made by @__xtzzz",
                      color=discord.Color.red())

  # Send the embed message
  await ctx.send(embed=embed)


@bot.command()
async def ssru(ctx):
  # Check if the command was sent in the specified channel
  if str(ctx.channel.id) != CHANNEL_ID:
    return

  # Create an embed message
  embed = discord.Embed(title="SSRU Website & Facebook!",
                        description="-----",
                        color=discord.Color.blue())
  embed.set_author(
      name=ctx.author.name,
      icon_url=ctx.author.avatar.url)  # Use avatar.url instead of avatar_url
  embed.add_field(name="Facebook",
                  value="https://www.facebook.com/sd.ssru",
                  inline=False)
  embed.add_field(name="Website",
                  value="http://secondary.sd.ssru.ac.th/home",
                  inline=True)
  embed.set_footer(text="© 2024 __xtzzz's")

  # Send the embed message
  await ctx.send(embed=embed)


@bot.command()
async def timeout(ctx, member: discord.Member, duration: int, *, reason=None):
  # Check if the command was sent in the specified channel
  if str(ctx.channel.id) != CHANNEL_ID:
    return

  # Check if the user has the required permissions
  if ctx.author.guild_permissions.manage_roles:
    # Get the role named "Timeout" or create it if it doesn't exist
    timeout_role = discord.utils.get(ctx.guild.roles, name="Timeout")
    if not timeout_role:
      timeout_role = await ctx.guild.create_role(
          name="Timeout", reason="Role for timeout command")

    # Add the timeout role to the member
    await member.add_roles(timeout_role, reason=reason)

    # Send a message confirming the timeout
    await ctx.send(
        f'{member.mention} has been timed out for {duration} minutes.')

    # Wait for the specified duration
    await asyncio.sleep(duration * 60)

    # Remove the timeout role from the member after the duration has passed
    await member.remove_roles(timeout_role, reason="Timeout duration expired.")
  else:
    await ctx.send("You don't have permission to use this command.")


@bot.command()
async def help(ctx):
    # Check if the command was sent in the specified channel
    if str(ctx.channel.id) != CHANNEL_ID:
        return await ctx.send("This command is only available in a specific channel.")

    # Create embed messages for each category of commands
    embed_commands = discord.Embed(title="🧠 Normal Commands 🤖", color=discord.Color.green())
    embed_commands.add_field(name="!hi", value="Greets the user.", inline=False)
    embed_commands.add_field(name="!cls [amount]", value="Clears the specified number of messages.", inline=False)
    embed_commands.add_field(name="!version", value="Information about the bot", inline=False)
    embed_commands.add_field(name="!help", value="Displays this dawg message.", inline=False)

    embed_school_commands = discord.Embed(title="🏫 School Commands 🎓", color=discord.Color.blue())
    embed_school_commands.add_field(name="!ssru", value="Information about SSRU", inline=False)
    embed_school_commands.add_field(name="!add_homework [subject] [work]", value="Add the homework assignment.", inline=False)
    embed_school_commands.add_field(name="!list_homework", value="List all of the homework.", inline=False)
    embed_school_commands.add_field(name="!remove_homework [subject] [work]", value="Remove the homework.", inline=False)

    embed_fun_commands = discord.Embed(title="🎉 Fun Commands 🎲", color=discord.Color.orange())
    embed_fun_commands.add_field(name="!coinflip", value="Flip the coin.", inline=False)
    embed_fun_commands.add_field(name="!diceroll", value="Roll the dice.", inline=False)
    embed_fun_commands.add_field(name="!google [anything]", value="Let it search for you", inline=False)

    # Send the embed messages
    await ctx.send(embed=embed_commands)
    await ctx.send(embed=embed_school_commands)
    await ctx.send(embed=embed_fun_commands)


@bot.command()
async def coinflip(ctx):
  # Check if the command was sent in the specified channel
  if str(ctx.channel.id) != CHANNEL_ID:
    return

  # Flip a coin
  result = random.choice(['Heads', 'Tails'])

  # Send the result
  await ctx.send(f"🪙 The coin landed on 🪙: {result}")


@bot.command()
async def diceroll(ctx, sides: int = 6):
  # Check if the command was sent in the specified channel
  if str(ctx.channel.id) != CHANNEL_ID:
    return

  # Roll the dice
  result = random.randint(1, sides)

  # Send the result
  await ctx.send(f"🎲 The dice rolled 🎲: {result}")


@bot.command()
async def google(ctx, query: str):
  # Check if the command was sent in the specified channel
  if str(ctx.channel.id) != CHANNEL_ID:
    return

  # Generate a Google search link with the given query
  google_link = f"https://www.google.com/search?q={query.replace(' ', '+')}"

  # Send the Google search link as a message
  await ctx.send(f"Google search for 🔎 '{query}': {google_link}")



# Run the bot
bot.run(TOKEN)
