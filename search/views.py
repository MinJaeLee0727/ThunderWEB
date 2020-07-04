import requests
from django.shortcuts import render
from search.interFunctions import switch_champions, switch_queue

# from .models import matches


# Create your views here.

# for web
def index(request):
    rotation_champions = []
    api_key = 'RGAPI-b408538f-4a26-4d36-a2bb-8f888adfd9cc'
    champion_rotation_url = "https://na1.api.riotgames.com/lol/platform/v3/champion-rotations"
    params = {'api_key': api_key}
    res = requests.get(champion_rotation_url, params=params)

    if res.status_code == requests.codes.ok:
        rotation_result = res.json()
        if rotation_result:
            for i in range(len(rotation_result["freeChampionIds"])):
                rotation_champions.append(switch_champions(rotation_result["freeChampionIds"][i]))
            print(rotation_champions)
        return render(request, 'search/index.html', {'rotation_champions': rotation_champions})


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


def transfer():
    return

