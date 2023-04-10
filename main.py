import discord
from discord.ext import commands, tasks
import pyautogui
import check_rating as cr
import time
import final_check as fc
import check_stream as cs
import start_browser as sb
from io import BytesIO
from selenium import webdriver

client = commands.Bot(command_prefix=">", intents=discord.Intents.all())

try:
    def check_roles(ctx):
        moderator = discord.utils.get(ctx.guild.roles, id=574931772781887488)
        admin = discord.utils.get(ctx.guild.roles, id=574720716025626654)
        vedal = discord.utils.get(ctx.guild.roles, id=574724513376370691)
        roles = ctx.author.roles
        if moderator in roles or admin in roles or vedal in roles or ctx.author.id == 452436342841016341:
            return True
        else:
            return False

    @client.event
    async def on_ready():
        print("Hello World!")
        await check_stream.start()
    
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
        elif check_roles(ctx) and screenshotting.is_running() == False:
            await ctx.reply('Im not capturing anything!')

    #Default coords, Normal Template
    coords = 790, 900, 350, 100

    @client.command()
    async def template(ctx, template):
        global coords
        if check_roles(ctx):
            if template == 'normal' and coords != (790, 900, 350, 100):
                coords = 790, 900, 350, 100
                await ctx.reply('Changed to normal template!')
            elif template == 'dev' and coords != (1350, 975, 200, 75):
                coords = 1350, 975, 200, 75
                await ctx.reply('Changed to dev template!')
            elif template == 'collab' and coords != (950, 940, 450, 80):
                coords = 950, 940, 450, 80
                await ctx.reply('Changed to collab template!')
            elif template == 'normal' or template == 'dev' or template == 'collab':
                await ctx.reply('That template is already being used!')
            else:
                await ctx.reply('Invalid template given.')


    templates = []
    channel = client.get_channel(1094701982507348079)
    thread = channel.get_thread(1085238141574713384)
    
    def isBrowserAlive():
        try:
           browser.current_url
           return True
        except:
           return False

    @tasks.loop()
    async def screenshotting():
        global templates, counter, recentImage, browser
        if cs.check_stream == False and isBrowserAlive():
            screenshotting.stop()
            browser.quit()

        recentImage = False
        counter = 0
        coords = 790, 900, 350, 100
        if cr.rating((coords)) and recentImage == False:
            print('[!] Found a result!')
            for template in templates:
                rating = fc.rating(template, coords[0], coords[1], coords[2], coords[3])
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
                    templates = []
                    break
                elif counter == len(templates):
                    print('[!] Could not find a valid image.')    
                else:
                    counter =+ 1
        else:
            recentImage = False
            template = pyautogui.screenshot()
            templates.insert(0, template)
            
    @tasks.loop(seconds=2)
    async def check_stream():
        if cs.check_stream():
            browser = webdriver.Firefox()
            browser.get('https://www.twitch.tv/vedal987')
            browser.fullscreen_window()
            sb.start(browser)
            await screenshotting.start()

    client.run("TOKEN")
except ValueError:
    print(f'There has been an error: {str(ValueError)}')
    
