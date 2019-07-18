from praw import Reddit
import requests
import datetime, time

def download_thoughts(sub='showerThoughts'):
    '''r = Reddit(client_id=c_id,client_secret=c_s,user_agent=ua)
    sub = r.subreddit('Showerthoughts')
    thoughts = [i.title for i in list(sub.hot(limit=2000))][2:]
    return '|'.join(thoughts)'''
    out = []
    for i in range(24):
        start_date = datetime.date.today() - datetime.timedelta(weeks=4*(i+1))
        end_date = datetime.date.today() - datetime.timedelta(weeks=4*i)
        start_date = datetime.datetime(start_date.year,start_date.month,start_date.day)
        end_date = datetime.datetime(end_date.year,end_date.month,end_date.day)
        payload = {'subreddit':sub,'before':str(int(end_date.timestamp())),'after':str(int(start_date.timestamp())),'limit':100}
        r = requests.get('https://api.pushshift.io/reddit/search/submission/',params=payload)
        print(r.url)
        try:
            for i in r.json()['data']:
                out.append(i['title'])
        except:
            pass
    print(len(out))
    return '|'.join(out)

download_thoughts()


