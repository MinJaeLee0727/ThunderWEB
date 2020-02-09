import requests
from django.shortcuts import render


# from .models import matches


# Create your views here.

# for inter-functions
def switch_queue(x):
    return \
        {900: "URUF",
         31: "Co-op vs AI Intro Bot",
         32: "Co-op vs AI Beginner Bot",
         33: "Co-op vs AI Intermediate Bot",
         450: "ARAM",
         440: "Flex",
         430: "Blind Pick",
         420: "SOLO RANK"
         }.get(x, "None")


def switch_champions(x):
    return\
        {
        266: "Aatrox",
        412: "Thresh",
        23: "Tryndamere",
        79: "Gragas",
        69: "Cassiopeia",
        136: "Aurelion Sol",
        13: "Ryze",
        78: "Poppy",
        14: "Sion",
        1: "Annie",
        202: "Jhin",
        43:  "Karma",
        111:  "Nautilus",
        240:  "Kled",
        99:  "Lux",
        103:  "Ahri",
        2:  "Olaf",
        112:  "Viktor",
        34:  "Anivia",
        27:  "Singed",
        86:  "Garen",
        127:  "Lissandra",
        57:  "Maokai",
        25:  "Morgana",
        28:  "Evelynn",
        105:  "Fizz",
        74:  "Heimerdinger",
        238:  "Zed",
        68:  "Rumble",
        82:  "Mordekaiser",
        37:  "Sona",
        96:  "Kog'Maw",
        55:  "Katarina",
        117:  "Lulu",
        22:  "Ashe",
        30:  "Karthus",
        12:  "Alistar",
        122:  "Darius",
        67:  "Vayne",
        110:  "Varus",
        77:  "Udyr",
        89:  "Leona",
        126:  "Jayce",
        134:  "Syndra",
        80:  "Pantheon",
        92:  "Riven",
        121:  "Kha'Zix",
        42:  "Corki",
        268:  "Azir",
        51:  "Caitlyn",
        76:  "Nidalee",
        85:  "Kennen",
        3:  "Galio",
        45:  "Veigar",
        432:  "Bard",
        150:  "Gnar",
        90:  "Malzahar",
        104:  "Graves",
        254:  "Vi",
        10:  "Kayle",
        39:  "Irelia",
        64:  "Lee Sin",
        420:  "Illaoi",
        60:  "Elise",
        106:  "Volibear",
        20:  "Nunu",
        4:  "Twisted Fate",
        24:  "Jax",
        102:  "Shyvana",
        429:  "Kalista",
        36:  "Dr. Mundo",
        427:  "Ivern",
        131:  "Diana",
        223:  "Tahm Kench",
        63:  "Brand",
        113:  "Sejuani",
        8:  "Vladimir",
        154:  "Zac",
        421:  "Rek'Sai",
        133:  "Quinn",
        84:  "Akali",
        163:  "Taliyah",
        18:  "Tristana",
        120:  "Hecarim",
        15:  "Sivir",
        236:  "Lucian",
        107:  "Rengar",
        19:  "Warwick",
        72:  "Skarner",
        54:  "Malphite",
        157:  "Yasuo",
        101:  "Xerath",
        17:  "Teemo",
        75:  "Nasus",
        58:  "Renekton",
        119:  "Draven",
        35:  "Shaco",
        50:  "Swain",
        91:  "Talon",
        40:  "Janna",
        115:  "Ziggs",
        245:  "Ekko",
        61:  "Orianna",
        114:  "Fiora",
        9:  "Fiddlesticks",
        31:  "Cho'Gath",
        33:  "Rammus",
        7:  "LeBlanc",
        16:  "Soraka",
        26:  "Zilean",
        56:  "Nocturne",
        222:  "Jinx",
        83:  "Yorick",
        6:  "Urgot",
        203:  "Kindred",
        21:  "Miss Fortune",
        62:  "Wukong",
        53:  "Blitzcrank",
        98:  "Shen",
        201:  "Braum",
        5:  "Xin Zhao",
        29:  "Twitch",
        11:  "Master Yi",
        44:  "Taric",
        32:  "Amumu",
        41:  "Gangplank",
        48:  "Trundle",
        38:  "Kassadin",
        161:  "Vel'Koz",
        143:  "Zyra",
        267:  "Nami",
        59:  "Jarvan IV",
        81:  "Ezreal",
        875: "Sett",
        523: "Aphelios",
        350: "Yuumi",
        246: "Qiyana"
    }.get(x, "New")


# for web
def index(request):
    return render(request, 'search/index.html', {})


def results(request):
    if request.method == "GET":
        summoner_name = request.GET.get('summonerName')


        #Variables
        # {}: dic []: List
        summoner_exist = False
        sum_result = {}
        solo_tier = {}
        team_tier = {}
        store_summoner_list = []
        match_data = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]   #50
        max_match_number = 50

        api_key = 'RGAPI-b408538f-4a26-4d36-a2bb-8f888adfd9cc'

        summoner_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(
            summoner_name)  # 소환사 정보 검색
        params = {'api_key': api_key}
        res = requests.get(summoner_url, params=params)

        # summoners_result = json.loads(((res.text).encode('utf-8')))
        if res.status_code == requests.codes.ok:  # 결과값이 정상적으로 반환되었을때만 실행하도록 설정
            summoner_exist = True
            summoners_result = res.json()  # response 값을 json 형태로 변환시키는 함수
            if summoners_result:

                # 소환사 기본 정보
                sum_result['name'] = summoners_result['name']
                sum_result['level'] = summoners_result['summonerLevel']
                sum_result['profileIconId'] = summoners_result['profileIconId']
                sum_result['accountId'] = summoners_result['accountId']

                tier_url = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + summoners_result[
                    'id']  # 소환사 티어 검색
                tier_info = requests.get(tier_url, params=params)
                tier_info = tier_info.json()

                if len(tier_info) == 1:  # 자유랭크 또는 솔로랭크 둘중 하나만 있는경우
                    tier_info = tier_info.pop()
                    if tier_info['queueType'] == 'RANKED_FLEX_SR':  # 자유랭크인 경우
                        team_tier['rankWithTier'] = tier_info['tier'] + " " + tier_info['rank']
                        team_tier['rank_type'] = '자유랭크 5:5'
                        team_tier['tier'] = tier_info['tier']
                        team_tier['rank'] = tier_info['rank']
                        team_tier['points'] = tier_info['leaguePoints']
                        team_tier['wins'] = tier_info['wins']
                        team_tier['losses'] = tier_info['losses']
                        team_tier['winRate'] = "%.2f%%" % ((tier_info['wins'] / (tier_info['wins'] + tier_info['losses'])) * 100)
                    else:  # 솔로랭크인 경우
                        solo_tier['rank_type'] = '솔로랭크 5:5'
                        solo_tier['rankWithTier'] = tier_info['tier'] + " " + tier_info['rank']
                        solo_tier['tier'] = tier_info['tier']
                        solo_tier['rank'] = tier_info['rank']
                        solo_tier['points'] = tier_info['leaguePoints']
                        solo_tier['wins'] = tier_info['wins']
                        solo_tier['losses'] = tier_info['losses']
                        solo_tier['winRate'] = "%.2f%%" % ((solo_tier['wins'] / (solo_tier['wins'] + solo_tier['losses'])) * 100)

                elif len(tier_info) == 2:  # 자유랭크, 솔로랭크 둘다 전적이 있는경우
                    for item in tier_info:
                        store_summoner_list.append(item)

                    solo_tier['rank_type'] = '솔로랭크 5:5'
                    solo_tier['tier'] = store_summoner_list[1]['tier']
                    solo_tier['rank'] = store_summoner_list[1]['rank']
                    solo_tier['rankWithTier'] = store_summoner_list[1]['tier'] + " " + store_summoner_list[1]['rank']
                    solo_tier['points'] = store_summoner_list[1]['leaguePoints']
                    solo_tier['wins'] = store_summoner_list[1]['wins']
                    solo_tier['losses'] = store_summoner_list[1]['losses']
                    solo_tier['winRate'] = "%.2f%%" % (
                            (store_summoner_list[1]['wins'] / (store_summoner_list[1]['wins'] + store_summoner_list[1]['losses'])) * 100)

                    team_tier['rank_type'] = '자유랭크 5:5'
                    team_tier['tier'] = store_summoner_list[0]['tier']
                    team_tier['rank'] = store_summoner_list[0]['rank']
                    team_tier['rankWithTier'] = store_summoner_list[0]['tier'] + " " + store_summoner_list[0]['rank']
                    team_tier['points'] = store_summoner_list[0]['leaguePoints']
                    team_tier['wins'] = store_summoner_list[0]['wins']
                    team_tier['losses'] = store_summoner_list[0]['losses']
                    team_tier['winRate'] = "%.2f%%" % (
                            (store_summoner_list[0]['wins'] / (store_summoner_list[0]['wins'] + store_summoner_list[0]['losses'])) * 100)

                # 소환사 매치 정보
                matches_url = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + summoners_result[
                    'accountId']
                matches_info = requests.get(matches_url, params=params)
                matches_info = matches_info.json()

                if matches_info:
                    matchNumber = len(matches_info["matches"])

                    if matchNumber > max_match_number:
                        matchNumber = max_match_number

                    for i in range(matchNumber):
                        others = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                        rich = True

                        match_data[i]["queue"] = switch_queue(matches_info["matches"][i]["queue"])
                        match_data[i]["champion"] = switch_champions(matches_info["matches"][i]["champion"])
                        match_data[i]['gameId'] = matches_info["matches"][i]['gameId']

                        match_url = "https://na1.api.riotgames.com/lol/match/v4/matches/" + str(
                            match_data[i]['gameId'])
                        match_info = requests.get(match_url, params=params)
                        match_info = match_info.json()

                        # if match_info["status"][2]:
                        #     del match_data[:]
                        #     global status
                        #     status = match_info
                        #     print(match_info)
                        #     break

                        for k in range(10):  # k = participantId
                            if summoner_name == match_info['participantIdentities'][k]['player']['summonerName']:
                                global participantId
                                participantId = k
                                others.remove(k)

                        for item in others:
                            if match_info['participants'][participantId]['stats']['goldEarned'] < match_info['participants'][item]['stats']['goldEarned']:
                                rich = False

                        if rich:
                            match_data[i]['rich'] = 'rich'

                        if participantId < 5:
                            # match_data[i]['team'] = 100
                            if match_info['teams'][0]['win'] == "Win":
                                match_data[i]['wl'] = 'win'
                            else:
                                match_data[i]['wl'] = 'lose'
                        else:
                            # match_data[i]['team'] = 200
                            if match_info['teams'][0]['win'] == "Win":
                                match_data[i]['wl'] = 'lose'
                            else:
                                match_data[i]['wl'] = 'win'



                #
                # if match_data[i]['team'] == 100:
                #     if match_info['teams'][0]['win'] == "Win":
                #         match_data[i]['win'] = 'win'
                #     else:
                #         match_data[i]['win'] = 'lose'
                # else:
                #     if match_info['teams'][0]['win'] == "Win":
                #         match_data[i]['win'] = 'lose'
                #     else:
                #         match_data[i]['win'] = 'win'

        return render(request, 'search/results.html',
                      {'summoner_exist': summoner_exist, 'summoners_result': sum_result, 'solo_tier': solo_tier,
                       'team_tier': team_tier, 'match_data': match_data})
