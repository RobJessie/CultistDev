import discord
import os
import asyncio
from discord.ext import tasks, commands
# from keep_alive import keep_alive
from badwords import badwordslist
import random
from datetime import datetime, timedelta
import re
import openai
import base64
import tiktoken

# meowdy, everypony, all se.1-16, clean up aram detection, fix perms for memquote


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='cult', intents=intents, help_command=None)

beanslist = ["cultist", "beans", "beance"]
wronglist = [r'\baram\b', "league of legends", "fortnite", "meowdy", "everypony"]
trolllist = [140265857615003648, 76599561069527040]

general = 765369488030957620
officer = 961839000354717696
quote_channel = 776547555903012904
zola = 295643156031209473

openai.organization= os.getenv('OPENAIORG')
openai.api_key = os.getenv('OPENAIKEY')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    bot.trollsent = datetime.now()
    bot.trollme = datetime.now() - timedelta(hours=1)
    bot.streamcd = []
    bot.imgctr=0
    bot.chat = {}
    await bot.change_presence(activity=discord.Game(name="in the basement..."))

@bot.event
async def on_message(message):
    text = message.content

    # React to sesh reply
    if message.author == bot.user:
        if text == "Have the mount but willing to fill? React here.":
            DPS = discord.utils.get(bot.emojis, name='DPS')
            Tank = discord.utils.get(bot.emojis, name='Tank')
            Healer = discord.utils.get(bot.emojis, name='Healer')
            Flex = discord.utils.get(bot.emojis, name='Flex')
            TankHeal = discord.utils.get(bot.emojis, name='TankHeal')
            TankDPS = discord.utils.get(bot.emojis, name='TankDPS')
            HealDPS = discord.utils.get(bot.emojis, name='HealDPS')
            await message.add_reaction(Tank)
            await message.add_reaction(DPS)
            await message.add_reaction(Healer)
            await message.add_reaction(TankHeal)
            await message.add_reaction(TankDPS)
            await message.add_reaction(HealDPS)
            await message.add_reaction(Flex)
            return

    # Reply to sesh farm posts
    if message.author.id == 616754792965865495:
        text2 = message.embeds[0].fields[1].name;

        print(message.embeds[0])
        print(text2)

        if text2.find('Tank') != -1:
            await asyncio.sleep(.2)
            await message.channel.send("Have the mount but willing to fill? React here.")
        return

    # Beans react
    for x in beanslist:
        if text.casefold().find(x) != -1:
            beans = discord.utils.get(bot.emojis, name='beans')
            await message.add_reaction(beans)

    # Random beans react
    if random.randint(1, 1000) == 1:
        selector = random.randint(1, 2)
        if selector == 1:
            beans = discord.utils.get(bot.emojis, name='beans')
        else:
            beans = discord.utils.get(bot.emojis, name='beance')
        await message.add_reaction(beans)

    if random.randint(1, 2000) == 1:
        dmgdown = discord.utils.get(bot.emojis, name='dmgdown')
        await message.add_reaction(dmgdown)

    # Wrong react
    if message.author != bot.user:
        for x in wronglist:
            if re.search(x, text.casefold()):
                wrong = discord.utils.get(bot.emojis, name='wrong')
                await message.add_reaction(wrong)

    # Ban gamer messages
    for x in badwordslist:
        if text.casefold().find(x.casefold()) != -1:
            idiot = message.author
            await idiot.ban(reason="Gamer word")
            officer_chat = message.guild.get_channel(officer)
            await officer_chat.send(f"<@&961839566938075216> Auto-banned {idiot.mention} ({idiot.display_name}) for saying a gamer word")

    # Annoy nira
    if message.author.id == 140265857615003648:
        if random.randint(1, 300) == 1:
            wrong = discord.utils.get(bot.emojis, name='wrong')
            await message.add_reaction(wrong)

    # Troll Icy
    if message.author.id == 98468309900476416 or message.author.id == 140265857615003648:
        if random.randint(1, 300) == 1:
            vuln = discord.utils.get(bot.emojis, name='vuln')
            await message.add_reaction(vuln)

    # Troll myself
    if bot.trollme < datetime.now() - timedelta(hours=1):
        if text.casefold().find("crystalline") != -1 or text.casefold().find(
                "crystaline") != -1 or text.casefold().find("crysstalline") != -1:
            bot.trollme = datetime.now()
            await message.reply(
                "I see you like Crystalline Conflict! It just so happens that <@204948060491481089> does as well! Please be sure to ask <@204948060491481089> to queue with you for your next Crystalline Conflict match. Crystalline Conflict courses through <@204948060491481089>'s veins, and he would be utterly distraught if 24 hours went by without having his Afflatus purged.")

    # Troll League and Fortnite players
    if bot.trollsent < datetime.now() - timedelta(minutes=10):
        playing = message.author.activity
        if hasattr(message.author, 'activity'):
            playing = message.author.activity
            if hasattr(playing, 'name'):
                pname = playing.name
                if pname is not None:
                    if pname.casefold().find("league of legends") != -1:
                        await message.reply(
                            "Thanks for your message! \n\nHowever, it has come to my attention that you're currently playing League of Legends. This is unfortunate. However, there is a solution! Kindly follow this link to make the lives of yourself and everyone else better! \n\nhttps://youtu.be/EjHKIJ90FtY")
                        bot.trollsent = datetime.now()
                    if pname.casefold().find("fortnite") != -1:
                        await message.reply(
                            "Thanks for your message! \n\nHowever, it has come to my attention that you're currently playing Fortnite. This is unfortunate. However, there is a solution! Kindly follow this link to make the lives of yourself and everyone else better! \n\nhttps://www.youtube.com/watch?v=cL6dtRYgSGs")
                        bot.trollsent = datetime.now()

    await bot.process_commands(message)

@bot.event
async def on_member_update(before, after):
    # Send reminder/welcome
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
        await generalchan.send(
            f"{after.mention}\nWelcome to the **CULT!** {worm}\n\nDon't forget to change your Discord nickname to include your in-game name, and enjoy your stay! {fatcatroll}")

    await gamernameban(after)

@bot.event
async def on_member_join(member):
    await gamernameban(member)

# Double beans
@bot.event
async def on_reaction_add(reaction, user):
    if hasattr(reaction, 'custom_emoji'):
        if reaction.emoji.name.casefold() == "beans" or reaction.emoji.name.casefold() == "beance":
            await reaction.message.add_reaction(reaction.emoji)

# Ban people with gamer names
async def gamernameban(member):
    for x in badwordslist:
        if member.display_name.casefold().find(x) != -1:
            await member.ban(reason="Gamer word in name")
            officer_chat = member.guild.get_channel(officer)
            await officer_chat.send(
                f"<@&961839566938075216> Auto-banned {member.mention} ({member.display_name}) for having a gamer word in their name.")

@bot.event
async def on_presence_update(before, after):
  go = False
  bac = None
  if hasattr(before, 'activity'):
    bac = before.activity
  if hasattr(after, 'activity'):
    ac = after.activity
    if isinstance(ac, discord.Streaming):
      if bac is None:
        go = True
      elif bac is not None:
        if isinstance(bac, discord.Streaming):
          go = False
        else:
          go = True

      for x in bot.streamcd:
        if x[0].id == after.id:
          if x[1] > datetime.now() - timedelta(hours=1):
            go = False
            bot.streamcd.remove(x)
            bot.streamcd.append([after, datetime.now()])

      if discord.utils.get(after.roles, name="Streamer") is not None and go:
        print('success')
        await after.guild.get_channel(867949767102177380).send(f'Check out {after.mention}\'s stream: \n **{ac}** \n {ac.url}')
        bot.streamcd.append([after, datetime.now()])

@bot.command()
async def bigrps(ctx, memb, num):
    members = ctx.guild.members
    pin = memb.strip('<').strip('>').strip('@')
    mem = discord.utils.get(members, display_name=memb)
    if mem is None:
        mem = discord.utils.get(members, id=int(pin))
    if mem is not None:
        nnum = int(num)
        if isinstance(nnum, int):
                callwins = 0
                oppwins = 0
                ties = 0

                if mem.id in trolllist and ctx.author in trolllist:
                    ties = nnum
                elif ctx.author.id in trolllist:
                    oppwins = nnum
                elif mem.id in trolllist:
                    callwins = nnum
                else:
                    a = random.random()
                    b = random.random()
                    c = random.random()

                    d = a+b+c
                    e = float(nnum/d)

                    callwins = int(a*e)
                    oppwins = int(b*e)
                    ties = int(c*e)

                winstring = f"{ctx.author.mention} wins!"
                if oppwins > callwins:
                    winstring = f"{mem.mention} wins!"
                elif oppwins == callwins:
                    winstring = "Tie..."

                await ctx.send(
                    f"Rock Paper Scissors TIMES {num}!!! \n\n{ctx.author.mention}\'s wins: {callwins}" + f"\n{mem.mention}\'s wins: {oppwins}" + f"\nTies: {ties}" + "\n\n" + winstring)
        else:
            await ctx.send("Enter a whole number.")

@bot.command()
async def rps(ctx, arg):
    members = ctx.guild.members
    pin = arg.strip('<').strip('>').strip('@')
    mem = discord.utils.get(members, display_name=arg)
    if mem is None:
        mem = discord.utils.get(members, id=int(pin))
    if mem is not None:
        rock = '🪨'
        scissors = '✂'
        paper = '📜'
        rpslist = [rock, paper, scissors]
        callhand = rpslist[random.randint(0, 2)]
        opphand = rpslist[random.randint(0, 2)]
        winner = determinerps(callhand, opphand)

        if mem.id in trolllist and ctx.author in trolllist:
            winner = 3
            opphand = callhand

        elif ctx.author.id in trolllist:
            winner = 2
            if opphand == rock:
                callhand = scissors

            elif opphand == scissors:
                callhand = paper

            elif opphand == paper:
                callhand = rock

        elif mem.id in trolllist:
            winner = 1
            if callhand == rock:
                opphand = scissors

            elif callhand == scissors:
                opphand = paper

            elif callhand == paper:
                opphand = rock

        if ctx.author.id == zola:
            if winner != 1:
                callhand = rpslist[random.randint(0, 2)]
                opphand = rpslist[random.randint(0, 2)]
                winner = determinerps(callhand, opphand)
                if winner != 1:
                    if mem.id == 98468309900476416:
                        callhand = rpslist[random.randint(0, 2)]
                        opphand = rpslist[random.randint(0, 2)]
                        winner = determinerps(callhand, opphand)

        elif mem.id == zola:
            if winner != 2:
                callhand = rpslist[random.randint(0, 2)]
                opphand = rpslist[random.randint(0, 2)]
                winner = determinerps(callhand, opphand)
                if winner != 2:
                    if ctx.author.id == 98468309900476416:
                        callhand = rpslist[random.randint(0, 2)]
                        opphand = rpslist[random.randint(0, 2)]
                        winner = determinerps(callhand, opphand)

        winstring = f"{ctx.author.mention} wins!"
        if winner == 2:
            winstring = f"{mem.mention} wins!"
        elif winner == 3:
            winstring = "Tie..."

        await ctx.send(
            f"Rock Paper Scissors! \n\n{ctx.author.mention}\'s hand: " + callhand + f"\n{mem.mention}\'s hand: " + opphand + "\n\n" + winstring)


@bot.command()
async def botrps(ctx):
    rock = '🪨'
    scissors = '✂'
    paper = '📜'
    rpslist = [rock, paper, scissors]
    culthand = rpslist[random.randint(0, 2)]
    userhand = rpslist[random.randint(0, 2)]
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
    elif winner == 3:
        winstring = "Tie..."

    await ctx.send(
        f"{ctx.author.mention} Rock Paper Scissors! \n\nMy hand: " + culthand + "\nYour hand: " + userhand + "\n\n" + winstring)


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
async def quote(ctx):
    chan = ctx.guild.get_channel(quote_channel)
    all_messages = await chan.history(limit=None).flatten()
    messages = []
    for m in all_messages:
        if m.content.find(':') != -1 or m.content.find('-') != -1:
            messages.append(m)
    chosen = messages[random.randint(0, len(messages) - 1)]
    ref = chosen.to_reference()
    await ctx.send(ref.jump_url)


# **cultmemquote** \"name\"- I will send a link to a random message from a specific member\n
@bot.command()
async def help(ctx):
    await ctx.send(
        "Hi! \nI'm the mysterious entity in the basement! Here's a list of what I can do:\n\n**cultrps** \"name\"- Play your friend in a game of rock paper scissors that is 100% fair for everyone!\n**cultbigrps** \"name\" \"whole number below 100000\"- Play your friend in a game of rock paper scissors that is 100% fair for everyone as many times as you want (assuming it's below 100000)!\n**cultbotrps** - Play me in a game of rock paper scissors that is 100% fair for everyone!\n**cultbeans** - I will send beans\n**cultrand** - I will send a random emoji\n**cultquote** - I will send a link to a random quote from <#776547555903012904>\n**cultplay** \"effect name\" - I will come into the vc and play the sound effect of your choice\n**cultpinax** - I will give you a random Pinax variation\n**cultspeak** \"your message\" - Speak to me directly!\n**cultimage** \"prompt\" - I will draw for you!\n\nWherever you need to enter a name, use the member's current nickname or @ them.\nI do some other stuff but you'll just have to figure that out")


@bot.command()
async def pinax(ctx):
    firsts = ['lightning edge', 'water knockback']
    seconds = ['fire stack', 'poison spread']
    directions = ['north', 'south', 'east', 'west']
    capesword = ['sword cleave', 'cape knockback']

    f1 = random.randint(0, 1)
    f2 = 1 if f1 == 0 else 0
    s1 = random.randint(0, 1)
    s2 = 1 if s1 == 0 else 0

    await ctx.send(
        firsts[f1] + " " + seconds[s1] + " " + directions[random.randint(0, 3)] + " " + firsts[f2] + " " + capesword[
            random.randint(0, 1)] + " " + seconds[s2])


@bot.command()
async def speak(ctx, arg):
    if ctx.author.id not in bot.chat.keys():
        messages=[
            {"role": "system", "content": "You are Cultist, a highly sarcastic assistant of the Totally Not A Cult free company."}
        ]
        bot.chat[ctx.author.id]= messages

    bot.chat[ctx.author.id].append({"role": "user", "content":arg})

    while num_tokens_message(bot.chat[ctx.author.id]) > 3250:
        bot.chat[ctx.author.id].pop(1)

    airesponse = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=bot.chat[ctx.author.id],
        temperature=0.2,
        max_tokens = 750,
        frequency_penalty=1,
    )

    reply=airesponse.choices[0].message.content

    bot.chat[ctx.author.id].append(airesponse.choices[0].message)

    n = 1500
    replylist = [reply[i:i+n] for i in range(0, len(reply), n)]

    for r in replylist:
        await ctx.reply(r)

# @bot.command()
# async def speak(ctx, arg):
#     airesponse = openai.Completion.create(
#         model="text-curie-001",
#         prompt=arg,
#         max_tokens=1024,
#         temperature=0.3,
#         presence_penalty=1.5
#     )
#
#     reply=airesponse.choices[0].text
#
#     n = 1500
#     replylist = [reply[i:i+n] for i in range(0, len(reply), n)]
#
#     for r in replylist:
#         await ctx.reply(r)

def num_tokens_message(messages):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-0301")
    num_tokens = 0
    for message in messages:
        num_tokens += 4
    for key, value in message.items():
        num_tokens += len(encoding.encode(value))
        if key == "name":
            num_tokens += -1
    num_tokens += 2
    return num_tokens

@bot.command()
async def image(ctx, arg):
    try:
        airesponse = await openai.Image.acreate(
            prompt=arg,
            size="512x512",
            response_format="b64_json"
        )

        b64str = airesponse.data[0].b64_json
        b64bytes = b64str.encode('ascii')

        bot.imgctr = bot.imgctr+1
        if (bot.imgctr>10):
            bot.imgctr = 0

        imgname = "image{ctr}.png".format(ctr=bot.imgctr)

        with open(imgname, "wb") as fh:
            fh.write(base64.decodebytes(b64bytes))

        file = discord.File(imgname, filename=imgname)
        await ctx.reply(file=file)

    except openai.InvalidRequestError as e:
        print(e)
        await ctx.reply("One or more words are not allowed.")
    except Exception as e:
        print(e)
        await ctx.reply("Something went wrong, try again.")

@bot.command()
async def sync(ctx):
    await bot.tree.sync()

bot.run(os.getenv('TOKEN'))

