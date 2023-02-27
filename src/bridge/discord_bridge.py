from typing import Any, Dict
import discord
from util.request_tools import Request
from json import loads


def build_bridge(g: Dict[str, Any]) -> None:
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Started Discord Bridge {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        try:
            rjson = loads(message.content)
            tmp = Request(rjson["api_call"], rjson["data"])
            g["Q"].appendleft(tmp)
        except Exception as e:
            err = e

    client.run(g["discord_token"])
