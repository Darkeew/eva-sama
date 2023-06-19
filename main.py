import discord
from discord.ext import commands, tasks
import pyautogui
import check_rating as cr
import time
import final_check as fc
import check_stream as cs
import start_browser as sb
import translation
from io import BytesIO
from selenium import webdriver

client = commands.Bot(command_prefix=">", intents=discord.Intents.all())
client.remove_command('help')

try:
    def check_roles(ctx):
        moderator = discord.utils.get(ctx.guild.roles, id=574931772781887488)
        admin = discord.utils.get(ctx.guild.roles, id=574720716025626654)
        vedal = discord.utils.get(ctx.guild.roles, id=574724513376370691)
        roles = ctx.author.roles
        if moderator in roles or admin in roles or vedal in roles or ctx.author.id == 452436342841016341 or ctx.author.id == 278232398372798464 or ctx.author.id == 854064215354114088:
            return True
        else:
            return False
        
    #@client.event
    #async def on_message(message):
    #    moderator = discord.utils.get(message.guild.roles, id=574931772781887488)
    #    admin = discord.utils.get(message.guild.roles, id=574720716025626654)
    #    vedal = discord.utils.get(message.guild.roles, id=574724513376370691)
    #    roles = message.author.roles
    #    author = message.author.id
    #    if moderator in roles or admin in roles or vedal in roles or author == 452436342841016341 or author == 278232398372798464 or author == 854064215354114088:
    #        if message.channel.id == 1067638175478071307 and message.content.startswith('?unlock'):
    #            await message.reply('Dont forget to start <@!1083827019965546606> using `>start`!')
    #        if message.channel.id == 1067638175478071307 and message.content.startswith('?lock'):
    #            await message.reply('Dont forget to stop <@!1083827019965546606> using `>stop`!')
            
        
    @client.event
    async def on_ready():
        print("Hello World!")
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="out for neuro-sama's livestream"))
        await check_stream.start()
  
    @client.command()
    async def ss(ctx):
        if check_roles(ctx):
            ss = pyautogui.screenshot()
            bytes = BytesIO()
            ss.save(bytes, format='png')
            bytes.seek(0)
            channel = client.get_channel(1067638175478071307)
            thread = channel.get_thread(1085238141574713384)
            file = discord.File(bytes, 'result.png')
            timestamp = round(time.time())
            await thread.send(f'Timestamp: <t:{timestamp}:F>',file=file)

    @client.command()
    async def pause(ctx):
        global pause
        if check_roles(ctx):
            pause = True
            await ctx.reply('Paused capturing when Neuro is online.')

    @client.command()
    async def unpause(ctx):
        global pause
        if check_roles(ctx):
            pause = False
            await ctx.reply('Unpaused capturing when Neuro is online.')

    @client.command()
    async def start(ctx):
        if check_roles(ctx) and check_stream.is_running() == False:
            await ctx.reply('Now capturing when Neuro is online!')
            await check_stream.start()
        elif check_roles(ctx) and screenshotting.is_running():
            await ctx.reply('Already capturing screenshots.')
    
    @client.command()
    async def stop(ctx):
        if check_roles(ctx) and screenshotting.is_running():
            await ctx.reply('No longer capturing when Neuro is online!')
            check_stream.stop()
            screenshotting.stop()
            try:
                browser.quit()
            except: pass
        elif check_roles(ctx) and screenshotting.is_running() == False:
            await ctx.reply('Im not capturing anything!')

    #Default coords, Normal Template
    coords = 790, 900, 350, 100
    
    tmp = 'normal'
    @client.command()
    async def template(ctx, template):
        global coords, tmp
        if check_roles(ctx):
            if template == 'normal' and coords != (790, 900, 350, 100):
                coords = 790, 900, 350, 100
                tmp = template
                await ctx.reply('Changed to normal template!')
            elif template == 'dev' and coords != (1350, 975, 200, 75):
                coords = 1350, 975, 200, 75
                tmp = template
                await ctx.reply('Changed to dev template!')
            elif template == 'collab' and coords != (740, 900, 350, 100):
                coords = 740, 900, 350, 100
                tmp = template
                await ctx.reply('Changed to collab template!')
            elif template == 'karaoke' and coords != (790, 900, 350, 100):
                coords = 790, 900, 350, 100
                tmp = template
                await ctx.reply('Changed to karaoke template!')
            elif template == 'normal' or template == 'dev' or template == 'collab' or template == 'karaoke':
                await ctx.reply('That template is already being used!')
            else:
                await ctx.reply('Invalid template given.')

    templates = []
    counter = 0
    recentImage = True
    pause = False
    translation.start_browser()
    browser = None
    
    @tasks.loop()
    async def screenshotting():
        if check_stream.is_running():
            check_stream.stop()
        channel = client.get_channel(1067638175478071307)
        thread = channel.get_thread(1085238141574713384)
        global templates, counter, recentImage, browser, pause
        if cs.check_stream() == False:
            try:
                await check_stream.start()
            except:
                check_stream.stop()

        coords = 740, 900, 350, 100
        if cr.rating((coords), tmp) and recentImage == False and pause == False:
            print('[!] Found a result!')
            for template in templates:
                rating = fc.rating(template, coords[0], coords[1], coords[2], coords[3], tmp)
                print(f'[{counter}] Checking template...')
                if rating == False:
                    recentImage = True
                    bytes = BytesIO()
                    template.save(bytes, format='png')
                    bytes.seek(0)
                    print('[!] Sending to Discord...')
                    file = discord.File(bytes, filename='result.png')
                    timestamp = round(time.time())
                    await thread.send(f'Timestamp: <t:{timestamp}:F>',file=file)
                    try:
                        file = translation.translate(template, tmp)
                        jp_channel = client.get_channel(1074104294845972610)
                        jp_thread = jp_channel.get_thread(1106334613221167124)
                        await jp_thread.send(f'タイムスタンプ: <t:{timestamp}:F>',file=file)
                    except:
                        pass
                    templates = []
                    counter = 0
                    break
                elif counter == len(templates):
                    print('[!] Could not find a valid image.')
                    recentImage = True
                    templates = []
                    counter = 0
                else:
                    counter += 1
        else:
            if cr.rating((coords), tmp) == False:
                recentImage = False
            template = pyautogui.screenshot()
            templates.insert(0, template)
            
    @tasks.loop(seconds=2)
    async def check_stream():
        if screenshotting.is_running():
            screenshotting.stop()
        global browser
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="out for neuro-sama's livestream"))
        if browser != None:
            browser.quit()
        browser = None
        if cs.check_stream():
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="neuro-sama"))
            browser = webdriver.Firefox()
            browser.get('https://www.twitch.tv/vedal987')
            browser.fullscreen_window()
            sb.start(browser)
            try:
                await screenshotting.start()
            except:
                screenshotting.stop()

























    client.run("TOKEN")
except ValueError:
    print(f'There has been an error: {str(ValueError)}')
    
