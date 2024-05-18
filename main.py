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
# Retrieve bot token from environment variable
TOKEN = os.environ.get('TOKEN')

# Replace 'channel_id_here' with the ID of the channel where you want the bot to respond
CHANNEL_ID = '1241258662237044777'
HOMEWORK_ID = '1241258296392945666'

# Define the intents
intents = discord.Intents.all()
intents.messages = True  # Enable the messages intent

# Create a bot instance with specified intents and command prefix
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Define the file path for storing the homework data
HOMEWORK_FILE = "homework.json"


# Function to load homework data from file
def load_homework():
  if os.path.exists(HOMEWORK_FILE):
    with open(HOMEWORK_FILE, "r") as file:
      return json.load(file)
  else:
    return {}


# Function to save homework data to file
def save_homework(data):
  with open(HOMEWORK_FILE, "w") as file:
    json.dump(data, file)


# Homework tracker dictionary
homework_tracker = load_homework()


@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}')
  activity = Activity(type=ActivityType.playing,
                      name="Helping SSRU Community Server")
  await bot.change_presence(activity=activity)


@bot.command()
async def add_homework(ctx, subject: str, *, assignment: str):
  # Check if the command was sent in the specified channel
  if str(ctx.channel.id) != HOMEWORK_ID:
    return

  # Add the homework assignment to the tracker
  if subject.lower() not in homework_tracker:
    homework_tracker[subject.lower()] = [assignment]
  else:
    homework_tracker[subject.lower()].append(assignment)

  await ctx.send(f'Homework assignment added for {subject}: {assignment}')

  # Save the updated homework data
  save_homework(homework_tracker)


@bot.command()
async def list_homework(ctx):
  # Check if the command was sent in the specified channel
  if str(ctx.channel.id) != HOMEWORK_ID:
    return

  # List all homework assignments
  if homework_tracker:
    for subject, assignments in homework_tracker.items():
      await ctx.send(f'📑**{subject.capitalize()} Homework:**\n' +
                     '\n'.join(assignments))
  else:
    await ctx.send('No homework assignments tracked.')


@bot.command()
async def remove_homework(ctx, subject: str, *, assignment: str):
  # Check if the command was sent in the specified channel
  if str(ctx.channel.id) != HOMEWORK_ID:
    return

  # Remove the specified homework assignment
  if subject.lower() in homework_tracker and assignment in homework_tracker[
      subject.lower()]:
    homework_tracker[subject.lower()].remove(assignment)
    await ctx.send(f'Homework assignment removed for {subject}: {assignment}')

    # Save the updated homework data
    save_homework(homework_tracker)
  else:
    await ctx.send('Homework assignment not found.')


# Make sure to save the homework data when the bot shuts down
@bot.event
async def on_disconnect():
  save_homework(homework_tracker)


@bot.command()
async def hi(ctx):
  # Check if the command was sent in the specified channel
  if str(ctx.channel.id) != CHANNEL_ID:
    return

  # Create an embed message
  embed = discord.Embed(
      title="Hello I'm the Assistant bot for SSRU-M6 Community Server!!!",
      description="this bot made by @__xtzzz",
      color=discord.Color.blue())
  embed.set_author(
      name=ctx.author.name,
      icon_url=ctx.author.avatar.url)  # Use avatar.url instead of avatar_url
  embed.add_field(name="About me",
                  value="https://xt1z.github.io/xtzzz-aboutme/",
                  inline=False)
  embed.add_field(name="Objective for this bot",
                  value="help our community",
                  inline=True)
  embed.set_footer(text="© 2024 __xtzzz's")

  # Send the embed message
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
async def hello(ctx):
  # Check if the command was sent in the specified channel
  if str(ctx.channel.id) != CHANNEL_ID:
    return

  # Create an embed message
  embed = discord.Embed(title="🤓 Assistant xtz!",
                        description="this bot made by @__xtzzz",
                        color=discord.Color.blue())
  embed.set_author(name=ctx.author.name,
                   icon_url=ctx.author.avatar.url
                   if ctx.author.avatar else discord.Embed.Empty)
  embed.add_field(name="version 1.0.0", value="", inline=False)
  embed.add_field(name="🤖", value="", inline=True)
  embed.set_footer(text="© 2024 __xtzzz's")

  # Send the embed message
  await ctx.send(embed=embed)


@bot.command()
async def ssru(ctx):
  # Check if the command was sent in the specified channel
  if str(ctx.channel.id) != CHANNEL_ID:
    return

  # Create an embed message
  embed = discord.Embed(title="SSRU Website & Facebook!",
                        description="this bot made by @__xtzzz",
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
    return

  # Create an embed message
  embed = discord.Embed(title="🕶 Bot Commands 🤖",
                        description="Here are the available commands:",
                        color=discord.Color.blue())

  # Add the list of commands
  embed.add_field(name="!hi", value="Greets the user.", inline=False)
  embed.add_field(name="!cls [amount]",
                  value="Clears the specified number of messages.",
                  inline=False)
  embed.add_field(name="!kick [member] [reason]",
                  value="Kicks the specified member with an optional reason.",
                  inline=False)
  embed.add_field(name="!ban [member] [reason]",
                  value="Bans the specified member with an optional reason.",
                  inline=False)
  embed.add_field(name="!timeout [member] [duration]",
                  value="Timeout the specified member",
                  inline=False)
  embed.add_field(name="!ssru", value="Information about SSRU", inline=False)
  embed.add_field(name="!coinflip", value="Flip the coin.", inline=False)
  embed.add_field(name="!diceroll", value="roll the dice.", inline=False)
  embed.add_field(name="!add_homework [subject] [work]",
                  value="Add the homework assignment.",
                  inline=False)
  embed.add_field(name="!list_homework",
                  value="list all of the homework.",
                  inline=False)
  embed.add_field(name="!remove_homework [subject] [work]",
                  value="Remove the homework.",
                  inline=False)
  embed.add_field(name="!google [anything]",
                  value="let it search for you",
                  inline=False)
  embed.add_field(name="!play[youtube url]",
                  value="play the youtube video/music",
                  inline=False)
  embed.add_field(name="!stop", value="stop playing video/music", inline=False)
  embed.add_field(name="!hello",
                  value="Information about the bot",
                  inline=False)
  embed.add_field(name="!help",
                  value="Displays this help message.",
                  inline=False)

  # Send the embed message
  await ctx.send(embed=embed)


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


@bot.command()
async def play(ctx, url):
  voice_channel = ctx.author.voice.channel
  if voice_channel is None:
    await ctx.send("You need to be in a voice channel to use this command.")
    return

  voice_client = await voice_channel.connect()

  try:
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    if not stream:
      await ctx.send("Error: No audio stream available for this URL.")
      return

    audio_source = await discord.FFmpegOpusAudio.from_probe(
        stream.url, executable="ffmpeg")
    voice_client.play(audio_source)
    await ctx.send(f"Now playing 🎧: {yt.title}")
  except Exception as e:
    await ctx.send(f"Error: {e}")


@bot.command()
async def stop(ctx):
  voice_client = ctx.voice_client
  if voice_client is not None:
    await voice_client.disconnect()
  else:
    await ctx.send("I'm not connected to a voice channel.")

# Run the bot
bot.run(TOKEN)
