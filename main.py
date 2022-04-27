import discord
import os
import asyncio
from discord.ext import tasks, commands
from keep_alive import keep_alive
from badwords import badwordslist
import random
from datetime import datetime, timedelta
import nacl
import ffmpeg
import opus
import re

#meowdy, everypony, all se.1-16

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='cultdev', intents=intents, help_command=None)
bot.trollsent = datetime.now()

beanslist = ["cultist","beans","beance"]
wronglist = [r'\baram\b', "wrong", "league of legends", "fortnite", "meowdy", "everypony"]
trolllist = [140265857615003648]

general = 765369488030957620
officer = 961839000354717696
quote_channel = 776547555903012904

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    bot.trollsent = datetime.now()
    await bot.change_presence(activity=discord.Game(name="in the basement..."))
 
@bot.event
async def on_message(message):
  text=message.content

  #React to sesh reply
  if message.author == bot.user:
    if text == "Have the mount but willing to fill? React here.":
      DPS = discord.utils.get(bot.emojis, name='DPS')
      Tank = discord.utils.get(bot.emojis, name='Tank')
      Healer = discord.utils.get(bot.emojis, name='Healer')
      Flex = discord.utils.get(bot.emojis, name='Flex')
      await message.add_reaction(Tank)
      await message.add_reaction(DPS)
      await message.add_reaction(Healer)
      await message.add_reaction(Flex)
      return

  #Reply to sesh farm posts
  if message.author.id == 616754792965865495:
    text2 = message.embeds[0].fields[1].name;
    
    print(message.embeds[0])
    print(text2)
      
    if text2.find('Tank') != -1:
      await asyncio.sleep(.2)
      await message.channel.send("Have the mount but willing to fill? React here.")
    return

  #Beans react
  for x in beanslist:
    if text.lower().find(x) !=-1:
      beans = discord.utils.get(bot.emojis, name='beans')
      await message.add_reaction(beans)

  #Random beans react
  if random.randint(1,100) == 1:
    selector = random.randint(1,2)
    if selector==1:
      beans = discord.utils.get(bot.emojis, name='beans')
    else:
      beans = discord.utils.get(bot.emojis, name='beance')
    await message.add_reaction(beans)

  #Wrong react
  for x in wronglist:
    if re.search(x,text.lower()):
      wrong = discord.utils.get(bot.emojis, name='wrong')
      await message.add_reaction(wrong)

  #Ban gamer messages
  for x in badwordslist:
    if text.lower().find(x.lower()) != -1:
      idiot = message.author
      await idiot.ban(reason="Gamer word")
      officer_chat = message.guild.get_channel(officer)
      await officer_chat.send(f"<@&961839566938075216> Auto-banned {idiot.mention} ({idiot.display_name}) for saying a gamer word.")

  #Annoy nira 
  if message.author.id == 140265857615003648:
    if random.randint(1,50) == 1:
      wrong = discord.utils.get(bot.emojis, name='wrong')
      await message.add_reaction(wrong)

  #Troll Icy
  if message.author.id == 98468309900476416:
    if random.randint(1,50) == 1:
      vuln = discord.utils.get(bot.emojis, name='vuln')
      await message.add_reaction(vuln)

  #Troll League and Fortnite players
  if bot.trollsent < datetime.now() - timedelta(minutes = 10):
    playing = message.author.activity
    print(playing)
    if playing is not None:
      pname = playing.name
      print(pname)
      if pname is not None:
        if pname.lower().find("league of legends")!=-1:
          await message.reply("Thanks for your message! \n\nHowever, it has come to my attention that you're currently playing League of Legends. This is unfortunate. However, there is a solution! Kindly follow this link to make the lives of yourself and everyone else better! \n\nhttps://youtu.be/EjHKIJ90FtY")
          bot.trollsent = datetime.now()
        if pname.lower().find("fortnite")!=-1:
          await message.reply("Thanks for your message! \n\nHowever, it has come to my attention that you're currently playing Fortnite. This is unfortunate. However, there is a solution! Kindly follow this link to make the lives of yourself and everyone else better! \n\nhttps://www.youtube.com/watch?v=cL6dtRYgSGs")
          bot.trollsent = datetime.now()
      
  await bot.process_commands(message)
  
@bot.event
async def on_member_update(before, after):

  #Send reminder/welcome
  beforeroles = before.roles
  afterroles = after.roles
  brole = discord.utils.get(beforeroles, name="Adept")
  arole = discord.utils.get(afterroles, name="Adept")
  if arole is None:
    arole = discord.utils.get(afterroles, name="Outsider")
  if brole is None:
    brole = discord.utils.get(beforeroles, name="Outsider")
  if (brole is None) and (arole is not None):
    generalchan = after.guild.get_channel(general)
    worm = discord.utils.get(bot.emojis, name='worm')
    fatcatroll = discord.utils.get(bot.emojis, name='fatcatroll')
    await generalchan.send(f"{after.mention}\nWelcome to the **CULT!** {worm}\n\nDon't forget to change your Discord nickname to include your in-game name; read up on our rules (<#765391688863973387>); and get yourself some shiny optional roles (<#810208652736593930>)\n\nEnjoy your stay! {fatcatroll}")

  await gamernameban(after)

@bot.event
async def on_member_join(member):
  await gamernameban(member)

#Double beans
@bot.event
async def on_reaction_add(reaction, user):
  if reaction.custom_emoji:
    if reaction.emoji.name.lower() == "beans" or reaction.emoji.name.lower() == "beance":
      await reaction.message.add_reaction(reaction.emoji)
  
#Ban people with gamer names
async def gamernameban(member):
  for x in badwordslist:
    if member.display_name.lower().find(x) != -1:
      await member.ban(reason="Gamer word in name")
      officer_chat = member.guild.get_channel(officer)
      await officer_chat.send(f"<@&961839566938075216> Auto-banned {member.mention} ({member.display_name}) for having a gamer word in their name.")

@bot.command()
async def rps(ctx, arg):
  members = ctx.guild.members
  mem = discord.utils.get(members, display_name=arg)
  if mem is not None:
    rock = '🪨'
    scissors = '✂️'
    paper = '📜'
    rpslist = [rock, paper, scissors]
    callhand = rpslist[random.randint(0,2)]
    opphand = rpslist[random.randint(0,2)]
    winner = determinerps(callhand, opphand)
  
    if ctx.author.id in trolllist:
      winner = 2
      if opphand == rock:
        callhand = scissors
        
      elif opphand == scissors:
        callhand = paper
        
      elif opphand == paper:
        callhand = rock

    if mem.id in trolllist:
      winner = 1
      if callhand == rock:
        opphand = scissors
        
      elif callhand == scissors:
        opphand = paper
        
      elif callhand == paper:
        opphand = rock  
        
    winstring = f"{ctx.author.mention} wins!"
    if winner == 2:
      winstring = f"{mem.mention} wins!"
    elif winner ==3:
      winstring = "Tie..."
      
    await ctx.send(f"Rock Paper Scissors! \n\n{ctx.author.mention}\'s hand: " + callhand + f"\n{mem.mention}\'s hand: "+ opphand+ "\n\n"+ winstring)

@bot.command()
async def botrps(ctx):
  rock = '🪨'
  scissors = '✂️'
  paper = '📜'
  rpslist = [rock, paper, scissors]
  culthand = rpslist[random.randint(0,2)]
  userhand = rpslist[random.randint(0,2)]
  winner = determinerps(culthand, userhand)

  if ctx.author.id in trolllist:
    winner = 1
    if culthand == rock:
      userhand = scissors
      
    elif culthand == scissors:
      userhand = paper
      
    elif culthand == paper:
      userhand = rock
    
  winstring = "I win!"
  if winner == 2:
    winstring = "You win..."
  elif winner ==3:
    winstring = "Tie..."
    
  await ctx.send(f"{ctx.author.mention} Rock Paper Scissors! \n\nMy hand: " + culthand + "\nYour hand: "+ userhand+ "\n\n"+ winstring)
    
def determinerps(hand1, hand2):
  rock = '🪨'
  scissors = '✂️'
  paper = '📜'
  if hand1 == hand2:
    return 3
  if hand1 == rock and hand2 == scissors:
    return 1
  if hand1 == scissors and hand2 == paper:
    return 1
  if hand1 == paper and hand2 == rock:
    return 1
  return 2

@bot.command()
async def beans(ctx):
  beans = discord.utils.get(bot.emojis, name='beans')
  await ctx.send(beans)

@bot.command()
async def rand(ctx):
  emojis = bot.emojis
  await ctx.send(emojis[random.randint(0, len(emojis))])

@bot.command()
async def memquote(ctx, arg):
  members = ctx.guild.members
  mem = discord.utils.get(members, display_name=arg)
  if mem is not None:
    channels = ctx.guild.text_channels
    all_messages = []
    for tc in channels:
      if bot.user in tc.members:
        chanmessages= await tc.history().flatten()
      for m in chanmessages:
        all_messages.append(m)
    messages = []
    for m in all_messages:
      if m.author==mem:
        messages.append(m)
    chosen = messages[random.randint(0,len(messages)-1)]
    ref = chosen.to_reference()
    await ctx.send(ref.jump_url)
  else:
    await ctx.send(f"Member \"{arg}\" not found.")

@bot.command()
async def quote(ctx):
  chan = ctx.guild.get_channel(quote_channel)
  all_messages = await chan.history().flatten()
  messages = []
  for m in all_messages:
    if m.content.find(':')!=-1 or m.content.find('-')!=-1:
      messages.append(m)
  chosen = messages[random.randint(0,len(messages)-1)]
  ref = chosen.to_reference()
  await ctx.send(ref.jump_url)

@bot.command()
async def se11(ctx):
  vc = ctx.author.voice
  if vc is not None:
    vcn = vc.channel
    if vcn is not None:
      voiceclient = await vcn.connect()
      voiceclient.play(discord.FFmpegOpusAudio('se-11.mp3'))
      await asyncio.sleep(2.5)
      await voiceclient.disconnect()
  else:
    await ctx.send("Can't play sound effects if you're not in a voice channel.")

@bot.command()
async def help(ctx):
  await ctx.send("Hi! \nI'm the mysterious entity in the basement! Here's a list of what I can do:\n\n**cultrps** \"name\"- Play your friend in a game of rock paper scissors that is 100% fair for everyone!\n**cultbotrps** - Play me in a game of rock paper scissors that is 100% fair for everyone!\n**cultbeans** - I will send beans\n**cultrand** - I will send a random emoji\n**cultquote** - I will send a link to a random quote from <#776547555903012904>\n**cultmemquote** \"name\"- I will send a link to a random message from a specific member\n**cultse11** - I will come into the vc and <se.11> you\n\nWherever you need to enter a name, use the member's current nickname.\nI do some other stuff but you'll just have to figure that out")
      
#@bot.command()
#async def rand(ctx):
#user_id = "201909896357216256"
#await message.channel.send(f"Happy birthday!<@{user_id}>!!!!!!!!!!!!!!!!!!!!!!")
  
keep_alive()
bot.run(os.getenv('CULTIST_DEV_TOKEN'))