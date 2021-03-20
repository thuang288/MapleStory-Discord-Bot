import discord
import time
import os
from lxml import etree
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

PATH = os.environ.get('CHROMEDRIVER_PATH')
TOKEN = os.environ.get('TOKEN')

options = webdriver.ChromeOptions()
#options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

# discord bot commands 
client = commands.Bot(command_prefix = '.')
client.remove_command('help')

@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms')

@client.command(pass_context=True)
async def rank(ctx, name):

    driver = webdriver.Chrome(PATH, options=options)
    driver.get('https://maplestory.nexon.net/rankings/overall-ranking/legendary?rebootIndex=0')
    
    # get character info
    search = driver.find_element_by_xpath("//input[@placeholder='Character Name']")
    search.send_keys(name)
    search.send_keys(Keys.ENTER)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'lxml')
  
    charInfo = soup.find_all('div', class_='c-rank-list__table-cell-text')
    Name = charInfo[8].text
    Rank = charInfo[6].text 
    world = charInfo[9]
    Level = charInfo[11].contents[0].strip()
    
    for i in soup.find_all('div', class_='c-rank-list__item-character-image'):
        charImg = i.img['src']

    for World in world:
        World = World['class'][1].capitalize()
    
    for Job in soup.find('div', attrs={'class':'c-rank-list__item-job-image'}):
        Job = Job.get('title')
       
    embed = discord.Embed(
        color = discord.Color.orange(),
        title = Name,
    )
    
    embed.set_thumbnail(url=charImg)
    embed.add_field(name='World', value= World, inline=True)
    embed.add_field(name='Job', value= Job, inline=True)
    embed.add_field(name='Level', value= Level, inline=True)
    embed.add_field(name='Rank', value= Rank, inline=True)

    await ctx.send(embed=embed)

client.run(TOKEN)