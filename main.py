import cv2
import numpy as np
from PIL import Image
import pyautogui
import os
import mss
import discord
from discord.ext import commands, tasks
import pygetwindow as gw
import psutil as ps
import requests
from selenium import webdriver
import time
#import soundcard as sc
#import soundfile as sf

client = commands.Bot(command_prefix=">", intents=discord.Intents.all())

confirmArray = []
def check_live():
    global confirmArray
    channelName = 'vedal987'
    response =  requests.get('https://www.twitch.tv/' +channelName)
    contents = response.content.decode('utf-8')
    if 'isLiveBroadcast' in contents:
        confirmArray = []
        return True
    elif str(response) == '<Response [200]>':
        confirmArray.append(response)
        if len(confirmArray) >= 50:
            return False
        else:
            return None

isLoopActive = False
@client.event
async def on_ready():
    print('Hello World!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="out for neuro-sama's livestream"))
    await screenshotting.start()

def check_roles(ctx):
    moderator = discord.utils.get(ctx.guild.roles, id=574931772781887488)
    admin = discord.utils.get(ctx.guild.roles, id=574720716025626654)
    vedal = discord.utils.get(ctx.guild.roles, id=574724513376370691)
    roles = ctx.author.roles
    if moderator in roles or admin in roles or vedal in roles or ctx.author.id == 452436342841016341:
        return True
    else:
        return False


@client.command()
async def start(ctx):
    if check_roles(ctx):
        global isLoopActive, stop, function
        if isLoopActive:
            await ctx.reply('Im already capturing neuro quotes!')
        elif isLoopActive  == False and check_live():
            await ctx.reply('Now capturing neuro quotes.')
            function = 'normal_loop'
            isLoopActive = True
        elif isLoopActive == False and check_live() == False:
            await ctx.reply('Cannot start capturing if there isnt any livestream going on.')


@client.command()
async def stop(ctx):
    if check_roles(ctx):
        global isLoopActive, stop
        if isLoopActive == False:
            await ctx.reply('Im not capturing any neuro quotes yet!')
        elif isLoopActive and check_live():
            await ctx.reply('No longer capturing neuro quotes.')
            stop = True
            isLoopActive = False
        elif isLoopActive and check_live() == False:
            await ctx.reply('Cannot stop capturing if there isnt any livestream going on. Also, this error shouldnt exist as if there is no livestream, it automaticly stops capturing <@!452436342841016341>')


@client.command()
async def template(ctx, template):
    global function
    if check_roles(ctx):
        if template == 'dev' and function != 'dev_loop':
            function = 'dev_loop'
            await ctx.reply('Changed to dev template.')
        elif template == 'dev':
            await ctx.reply('Already on dev template.')
        elif template == 'normal' and function != 'normal_loop':
            function = 'normal_loop'
            await ctx.reply('Changed to normal loop.')
        elif template == 'normal':
            await ctx.reply('Already on normal loop.')
        elif template == 'collab' and function != 'collab_loop':
            function = 'collab_loop'
            await ctx.reply('Changed to collab loop.')
        elif template == 'collab':
            await ctx.reply('Already on collab loop.')
        else:
            await ctx.reply('Invalid template given.')


@client.command()
async def evaping(ctx):
    if check_roles(ctx):
        await ctx.reply('Evapong! (Im pretty alive)')
        

@client.command()
async def create_template(ctx, coords, preprocessing):
    if check_roles(ctx):
        if coords == 'max':
            pyautogui.screenshot('input.png')
        else:
            pyautogui.screenshot('input.png', (coords))
        if preprocessing == True:
            preprocessing('input.png')
            file = discord.File('output.png')
            await ctx.reply(file=file)
        else:
            file = discord.File('input.png')
            await ctx.reply(file=file)


for file in os.listdir(r'C:\Users\TC\Desktop\NeuroClipper'): 
        if file.startswith('result'):
            os.remove(r'C:\Users\TC\Desktop\NeuroClipper\\' + file )


def preprocessing(image, lower, upper):
    image = cv2.imread(image)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([lower])
    upper = np.array([upper])
    mask = cv2.inRange(hsv, lower, upper)
    result = 255 - mask
    cv2.imwrite('output.png', result)
    image = cv2.imread('output.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    return image


def create_input(x1, y1, x2, y2):
    pyautogui.screenshot('input.png', (x1, y1, x2, y2))
    output = preprocessing('input.png', (0,0,0),(0,0,0))
    rating = np.sum(output == 0)
    return rating

ratings = [500]
async def get_minmax():
    for i in ratings:
        if i == 0:
            array.pop(i)
    channel = client.get_channel(733642306565046346)
    await channel.send(f'> Maximum Pixel Count: {str(np.max(ratings))}\n > Mininum Pixel Count: {str(np.min(ratings))}')

async def screenshot_loop(x1, y1, x2, y2):
    channel = client.get_channel(1067638175478071307)
    thread = channel.get_thread(1085238141574713384)
    global counter, array, recentImage, ratings
    rating = create_input(x1, y1, x2, y2)
    if rating == 0:
        x = 1
        for input in array:
            image = input
            mss.tools.to_png(input.rgb, input.size, level=9, output='checking.png')
            image = Image.open('checking.png')
            image = image.crop((x1, y1, x1+x2, y1+y2))
            image.save('checking.png')
            image = preprocessing('checking.png', (0,0,0),(0,0,0))
            rating = np.sum(image == 0)
            print("Trying image " + str(x) + "...")
            if recentImage == False:
                if rating != 0:
                    mss.tools.to_png(input.rgb, input.size, level=9, output='result_' + str(counter) + '.png')
                    file = discord.File('result_' + str(counter) + '.png')
                    timestamp = round(time.time())
                    print('Got a result. Saving and sending to discord...')
                    await thread.send(f'Timestamp: <t:{timestamp}:F>',file=file)
                    recentImage = True
                    counter = counter + 1
                    array = []
                    break
                elif x == len(array):
                    print('Could not find an image!')
                    array = []
            x = x + 1
    elif rating > 0:
        with mss.mss() as sct:
            mon = sct.monitors[1]
            mon = {"top": mon["top"], "left": mon["left"], "width": mon["width"], "height": mon["height"], "mon": 1}
            placeholder = sct.grab(monitor=mon)
            array.insert(0, placeholder)
            ratings.append(rating)
        recentImage = False
    if len(ratings) % 150 == 0:
        await get_minmax()


def isBrowserAlive():
   try:
      browser.current_url
      return True
   except:
      return False


function = 'normal_loop'
counter = 0
array = []
stop = False
recentImage = False
isLoopActive = False
@tasks.loop(seconds=0.1)
async def screenshotting():
    general = client.get_channel(1059569601144442911)
    global isLoopActive, browser, stop
    if isLoopActive == True and check_live() == False and isBrowserAlive():
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="out for neuro-sama's livestream"))
        browser.quit()
        await general.send('Neuro is no longer live :(')
        stop = False
        isLoopActive = False
    if isLoopActive:
        if function == 'normal_loop':
            await screenshot_loop(790, 900, 350, 100)
        elif function == 'collab_loop':
            await screenshot_loop(950, 940, 450, 80)
        elif function == 'dev_loop':
            await screenshot_loop(1350, 975, 200, 75)
    if isLoopActive == False and check_live() and stop == False:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="neuro-sama"))
        isLoopActive = True
        #await general.send('Neuro is live! <#1067638175478071307>')
        browser = webdriver.Firefox()
        browser.get('https://www.twitch.tv/vedal987')
        browser.fullscreen_window()
        time.sleep(5)
        pyautogui.click(900,0)
        pyautogui.press('f')
        pyautogui.click(1862, 1054)
        time.sleep(0.2)
        pyautogui.click(1716, 833)
        time.sleep(0.2)
        pyautogui.click(1599, 888)
        time.sleep(0.2)
        pyautogui.click(918, 800)
        try:
            browser.execute_script("""
const liveTime = document.querySelector(".live-time");

const style = document.createElement("style");
style.id = "on-video-time-style";
style.textContent = `#on-video-time {
  position: absolute;
  padding: .5rem;
  top: 0;
  right: .3rem;
  z-index: 9999;

  color: black;
  font-size: 9rem;
  font-weight: bold;
  text-shadow: 0 0 4px white;
}`;

document.head.appendChild(style);

const onVideoTime = document.createElement("div");
onVideoTime.id = "on-video-time";
onVideoTime.textContent = liveTime.textContent;

const videoContainer = document.querySelector(".video-ref");
videoContainer.insertBefore(onVideoTime, videoContainer.children[0])

const observer = new MutationObserver((mutations) => {
  for (const mutation of mutations) {
    if (mutation.type === "characterData") {
      onVideoTime.textContent = mutation.target.textContent
    }
  }
});

observer.observe(liveTime, {
  characterData: true,
  subtree: true
});
""")
        except ValueError:
            isLoopActive = False
      

client.run("TOKEN")





        



