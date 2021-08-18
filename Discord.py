import discord
import random
import json
import requests
from bs4 import BeautifulSoup

dataRead = open("keys.txt", 'r')
data = dataRead.read().splitlines()
dataRead.close()

discordKey = data[0]
lolApiKey = data[1]
lolRegion = data[2]
lolApiLink = "https://" + lolRegion + ".api.riotgames.com"
lolSummoner = "/lol/summoner/v4/summoners/by-name/"
lolLeague = "/lol/league/v4/entries/by-summoner/"

emojiIDs = {
    'IRON' : 666289575630602250,
    'BRONZE' : 666289348504715289,
    'SILVER' : 666289779041894408,
    'GOLD' : 666289959208091648,
    'PLATINUM' : 666290419797327892,
    'DIAMOND' : 666290693722865674,
    'MASTER' : 666290836656357376,
    'GRANDMASTER' : 666290969292963860,
    'CHALLENGER' : 666291097294733317
}

class MyClient(discord.Client):
    def getSummonerLink(self, name):
        return lolApiLink + lolSummoner + name + "?api_key=" + lolApiKey

    def getLeagueLink(self, id):
        return lolApiLink + lolLeague + id + "?api_key=" + lolApiKey

    def getPlayerInfo(self, nickName):
        req = requests.get(self.getSummonerLink(nickName))
        reqInfo = json.loads(req.content)
        req = requests.get(self.getLeagueLink(reqInfo['id']))
        reqInfo = json.loads(req.content)
        for item in reqInfo:
            if item['queueType'] == 'RANKED_SOLO_5x5':
                return item

    def formPlayerOutput(self, info):
        if('tier' not in info):
            return info['summonerName'] + " Unranked"
        emo = "<:" + info['tier'] + ":" + str(emojiIDs[info['tier']]) + ">"
        output = emo + " " + info['summonerName'] + " " + info['tier'] + " " + info['rank'] + " " + str(info['leaguePoints']) + "lp"
        return output

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if(message.content.startswith("?elo")):
            lst = message.content.split( )
            info = self.getPlayerInfo(lst[1])
            output = self.formPlayerOutput(info)

            await message.channel.send(output)
            return

client = MyClient()
client.run(discordKey)
