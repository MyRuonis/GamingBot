import discord
import random
import json
from riotwatcher import RiotWatcher, ApiError

dataRead = open("keys.txt", 'r')
data = dataRead.read().splitlines()
dataRead.close()

discordKey = data[0]
lolKey = data[1]
region = data[2]

riotGamesApi = RiotWatcher(lolKey)
my_region = region

emojiIDs = {}
emojiIDs['IRON'] = 666289575630602250
emojiIDs['BRONZE'] = 666289348504715289
emojiIDs['SILVER'] = 666289779041894408
emojiIDs['GOLD'] = 666289959208091648
emojiIDs['PLATINUM'] = 666290419797327892
emojiIDs['DIAMOND'] = 666290693722865674
emojiIDs['MASTER'] = 666290836656357376
emojiIDs['GRANDMASTER'] = 666290969292963860
emojiIDs['CHALLENGER'] = 666291097294733317

class MyClient(discord.Client):
    def getStats(self, nickname):
        try:
            player = riotGamesApi.summoner.by_name(my_region, nickname)
            ranked_stats = riotGamesApi.league.by_summoner(my_region, player['id'])

            if(not ranked_stats):
                return {}
            for stat in ranked_stats:
                if stat['queueType'] == "RANKED_SOLO_5x5":
                    return stat
                
        except ApiError as err:
            if err.response.status_code == 429:
                print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            elif err.response.status_code == 404:
                print('Name not found')

        return {}
    
    def output(self, **info):
        return info['summonerName'] + " <:" + info['tier'].lower() + ":" + str(emojiIDs[info['tier']]) + "> " + info['rank'] + " (" + str(info['leaguePoints']) + "lp) (" + str(info['sortValue']) + ")"

    def convert(self, number):
        if(len(number) != 2):
            if(len(number) == 3): return 1
            else: return 3
        if(number[1] == 'V'): return 0
        return 2
        
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if(message.content.startswith("RANDOM")):
            lst = message.content.split( )

            await message.channel.send('Team RED: ')
            for i in range(int((len(lst)-1) /2)):
                place = random.randint(2, len(lst)-1)
                await message.channel.send(lst[place] + " ")
                lst.remove(lst[place])

            await message.channel.send('Team BLUE: ')
            i = 1
            while (i < len(lst)):
                await message.channel.send(lst[i] + " ")
                i = i + 1

            return

        if(message.content.startswith("RandNMB")):
            lst = message.content.split( )
            mess = random.randint(int(lst[1]), int(lst[2]))
            await message.channel.send(str(mess))
            return
        
        if(message.content.startswith("?elo")):
            lst = message.content.split( )
            mess = message.content
            name = ""

            for i in range(0, len(mess)-5):
                name += mess[i+5]            

            statistics = self.getStats(name)

            if(statistics == {}): await message.channel.send("No Solo/Duo rank found")
            else: await message.channel.send(self.output(**statistics))

            return

        if(message.content.startswith("?rankings")):
            dataRead = open("players.txt", 'r')
            data = dataRead.read().splitlines()

            stats = []
            for player in data:
                info = self.getStats(player)
                if(info != {}): stats.append(info)
            
            ranks = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER', 'GRAND MASTER', 'CHALLENGER']
            
            for stat in stats:
                for i in range(len(ranks)-1):
                    if ranks[i] == stat['tier']:
                        stat['sortValue'] = i*404 + self.convert(stat['rank'])*101 + stat['leaguePoints']
                        break
            
            stats = sorted(stats, key=lambda k: k['sortValue'], reverse=True)

            out = ""
            
            for stat in stats:
                out += self.output(**stat) + "\n"

            if(out == ""): await message.channel.send("No ranks")
            else: await message.channel.send(out)
            
            return
            

client = MyClient()
client.run(discordKey)
