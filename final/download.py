from praw import Reddit

def download_thoughts(c_id,c_s,ua):
    r = Reddit(client_id=c_id,client_secret=c_s,user_agent=ua)
    sub = r.subreddit('Showerthoughts')
    thoughts = [i.title for i in list(sub.hot(limit=2000))][2:]
    return '|'.join(thoughts)

#download_thoughts('aKqi4PTcNaX3yQ','VBYcbJbY28f4Tucd4agH4-5-UsE','ShowerThinker v1.0.0 by u/iTecX')


