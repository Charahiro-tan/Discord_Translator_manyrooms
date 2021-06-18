import asyncio
import re
import os

from async_google_trans_new import AsyncTranslator, constant
import aiohttp
import discord

client = discord.Client(activity=discord.Game(name='neko2.net/juroom_ug'))
g = AsyncTranslator(url_suffix='co.jp')

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
HOME_LANG     = os.environ['HOME_LANG']
HOME_TO_LANG  = os.environ['HOME_TO_LANG']

try:
    send_embed = int(os.environ['SEND_EMBED'])
    if send_embed == 1:
        send_embed = True
    else:
        send_embed = False
except:
    send_embed = False

try:
    GAS_URL = os.environ['GAS_URL']
except:
    GAS_URL = ''

try:
    IGNORE_ID = os.environ['IGNORE_ID']
    l = IGNORE_ID.split(':')
    if len(l) >= 1:
        ignore_ids = [int(id) for id in l]
    else:
        ignore_ids = []
except:
    ignore_ids = []

del_word = [r"<a?:\w+?:\d+?>",r"<@! \d+>",r"^(.)\1+$",r"https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+",
    r"^!.*",r"^w$",r"^ｗ$",r"ww+",r"ｗｗ+",r"^\s+"]

langlist = list(constant.LANGUAGES.keys())
del_word_compiled = [re.compile(w) for w in del_word]

async def gas_translate(msg, lang_tgt, lang_src):
    gas_use = False
    params = {
        'text' : msg,
        'target' : lang_tgt,
        'source' : lang_src
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(GAS_URL, params=params) as r:
            if r.status == 200:
                js = await r.json()
                if js['code'] == 200:
                    translated_text = js.get('text')
                    gas_use = True
            return translated_text, gas_use

@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.author.id in ignore_ids:
        return
    
    msg = message.content
    display_name = message.author.display_name
    author_thumbnail = message.author.avatar_url.BASE + message.author.avatar_url._url
    
    for r in del_word_compiled:
        msg = r.sub('', msg)
    
    if len(msg) <= 1:
        return
    
    ###################################
    
    lang_src = None
    lang_tgt = None
    
    split_msg = msg.split(':')
    if len(split_msg) >= 2:
        if split_msg[0].lower() in langlist:
            lang_tgt = split_msg[0]
            msg = ':'.join(split_msg[1:])
            detect_task = asyncio.create_task(g.detect(msg))
            lang_src = await detect_task
            lang_src = lang_src[0]
        else:
            msg = ':'.join(split_msg[0:])
    else:
        msg = ':'.join(split_msg[0:])
    
    if lang_tgt is None:
        detect_task = asyncio.create_task(g.detect(msg))
        lang_src = await detect_task
        lang_src = lang_src[0]
        
        if lang_src == HOME_LANG:
            lang_tgt = HOME_TO_LANG
        else:
            lang_tgt = HOME_LANG
    
###########################################################

    translated = ''
    gas_use = False
    
    if GAS_URL:
        translated, gas_use = await gas_translate(msg, lang_tgt, lang_src)
    if not translated:
        trans_task = asyncio.create_task(g.translate(msg, lang_tgt,lang_src))
        translated = await trans_task
    
    if not translated:
        return
    
    p = f'({display_name}){message.content}({lang_src}):{translated}({lang_tgt})'
    if gas_use:
        p = p + '(GAS)'
    else:
        p = p + '(No GAS)'
    print(p)
    
    if send_embed:
        embed_color = int
        if gas_use:
            embed_color = 0x4169e1
        else:
            embed_color = 0xdc143c
        
        embed = discord.Embed(description=translated, color=embed_color)
        # embed = discord.Embed(title=translated, description=msg, color=embed_color)
        embed.set_author(name=display_name, icon_url=author_thumbnail)
        # embed.set_footer(text=f'({lang_src} > {lang_tgt})')
        
        await message.channel.send(embed=embed)
    else:
        send_msg = f'{translated} 〔{display_name}〕'
        await message.channel.send(send_msg)

client.run(DISCORD_TOKEN)