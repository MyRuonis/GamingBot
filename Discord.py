import discord
import random
import json
import requests

dataRead = open("keys.txt", 'r')
data = dataRead.read().splitlines()
dataRead.close()

discordKey = data[0]
lolApiKey = data[1]
lolRegion = data[2]
lolApiLink = "https://" + lolRegion + ".api.riotgames.com"
lolSummoner = "/lol/summoner/v4/summoners/by-name/"
lolLeague = "/lol/league/v4/entries/by-summoner/"

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

atsakymai = ["Yes", "No", "I do not know that", "<:CHALLENGER:666291097294733317>", "Try again"]

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
        emo = "<:" + info['tier'] + ":" + str(emojiIDs[info['tier']]) + ">"
        output = emo + " " + info['summonerName'] + " " + info['tier'] + " " + info['rank'] + " " + str(info['leaguePoints']) + "lp"
        return output

    def rankValue(self, info):
        val = int(info['leaguePoints'])

        if(info['rank'] == 'III'): val += 100
        elif(info['rank'] == 'II'): val += 200
        elif(info['rank'] == 'I'): val += 300

        if(info['tier'] == "IRON"): val += 0
        elif(info['tier'] == "BRONZE"): val += 500
        elif(info['tier'] == "SILVER"): val += 1000
        elif(info['tier'] == "GOLD"): val += 1500
        elif(info['tier'] == "PLATINUM"): val += 2000
        elif(info['tier'] == "DIAMOND"): val += 2500
        else: val += 3000

        return val

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if(message.content.startswith("?rt")):
            # returns randomized teams
            # ?rt player1 player2 player3 ...
            lst = message.content.split( )

            output = 'Team RED:\n'
            for i in range(int((len(lst)-1) /2)):
                place = random.randint(1, len(lst)-1)
                output += lst[place] + " "
                lst.remove(lst[place])

            output += "\nTeam BLUE:\n"
            i = 1
            while (i < len(lst)):
                output += lst[i] + " "
                i = i + 1

            await message.channel.send(output)

            return

        if(message.content.startswith("?rn")):
            # returns a random number between num1 and num2
            # ?rn num1 num2
            lst = message.content.split( )
            mess = random.randint(int(lst[1]), int(lst[2]))
            await message.channel.send(str(mess))
            return
        
        if(message.content.startswith("?elo")):
            # returns players rank info in eune
            # ?elo MyRuonis
            lst = message.content.split( )
            info = self.getPlayerInfo(lst[1])
            output = self.formPlayerOutput(info)

            await message.channel.send(output)
            return
        
        if(message.content.startswith("?rankings")):
            # returns players ranking in players.txt
            # ?rankings
            fr = open("players.txt", 'r')
            info = fr.read().splitlines()
            fr.close()

            arr = [dict() for x in range(len(info))]
            for i in range(len(info)):
                obj = self.getPlayerInfo(info[i])
                arr[i] = obj

            for item in arr:
                item["rankValue"] = self.rankValue(item)

            arr = sorted(arr, key = lambda i: i['rankValue'], reverse=True)

            output = ""
            for item in arr:
                output += self.formPlayerOutput(item) + "\n"

            await message.channel.send(output)
            return

        if(message.content.startswith("?q")):
            # returns a random answer to a question
            # ?q Question
            place = random.randint(1, len(atsakymai)-1)
            await message.channel.send(atsakymai[place])
            return

            

client = MyClient()
client.run(discordKey)
