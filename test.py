import json
from riotwatcher import RiotWatcher, ApiError

watcher = RiotWatcher('RGAPI-5fa91070-74be-4244-a579-655fb2647af9')

my_region = 'eun1'

#me = watcher.summoner.by_name(my_region, 'Ramous213')
#my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])

try:
    response = watcher.summoner.by_name(my_region, 'this_is_probably_not_anyones_summoner_name')
except ApiError as err:
    if err.response.status_code == 429:
        print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
        print('this retry-after is handled by default by the RiotWatcher library')
        print('future requests wait until the retry-after time passes')
    elif err.response.status_code == 404:
        print('Summoner with that ridiculous name not found.')
    else:
        raise
