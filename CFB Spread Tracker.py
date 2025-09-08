#!/usr/bin/env python
# coding: utf-8

# In[114]:


import cfbd
import pandas as pd
import numpy as np
import datetime as dt
#from github import Github
import os

TOKEN = "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"

FILE_PATH = "/CFB/cfbspread/CFB_Spread_Database.csv"
REPO = "itskleb/cfbspread"
GIT_Path = "CFB_Spread_Database.csv"

#g = Github(TOKEN)

#repo = g.get_repo(REPO)

configuration = cfbd.Configuration(access_token='cfBzp2RbdkBIYhq0ZYQ6wxbpDUWgIbIJ8Let+jDNSIaobtaHslr7jsIYFP2uT9bL')
#configuration.api_key['Authorization'] = 'Bearer cfBzp2RbdkBIYhq0ZYQ6wxbpDUWgIbIJ8Let+jDNSIaobtaHslr7jsIYFP2uT9bL'
#configuration.api_key_prefix['Authorization'] = 'Bearer'


def grabSpreadDiff(x):
    try:
        diff = x['spreadOpen']-x['spread']
    except:
        diff = np.nan
    return (diff)

def grabHMoney(x):
    try:
        money = x['homeMoneyline']
    except:
        money = np.nan
    return (money)

def grabAMoney(x):
    try:
        money = x['awayMoneyline']
    except:
        money = np.nan
    return (money)

def grabTeam(x):
    try:
        team = x['formattedSpread'].split(" -")[0]
    except:
        team = np.nan
    return (team)
    
def grabSpread(x):
    try:
        sp = x['spread']
    except:
        sp = np.nan
    return (sp)

def grabSpreadO(x):
    sp = x['spreadOpen']
    return (sp)

def colorOfMoney(x):
    if x['favorite'] == x['homeTeam'] and x['spreadDiffmean'] > 0:
        clr = 'HomeFavGoingAway'
    elif x['favorite'] == x['homeTeam'] and x['spreadDiffmean'] < 0:
        clr = 'HomeFavImprobableLuck'
    elif x['favorite'] == x['awayTeam'] and x['spreadDiffmean'] > 0:
        clr = 'AwayFavGoingAway'
    elif x['favorite'] == x['awayTeam'] and x['spreadDiffmean'] < 0:
        clr = 'AwayFavImprobableLuck'
    else:
        clr = 'Flat'
        
    return (clr)


def grabNewLines(week,year,config):
    now = dt.datetime.now()

    
    lines = cfbd.BettingApi(cfbd.ApiClient(config))
    cols = lines.get_lines(year=year,week=week)[0].to_dict().keys()
    updf = pd.DataFrame(columns=cols)
    games = lines.get_lines(year=year,week=week)
    
    for i in games:
        cdf = pd.DataFrame(i.to_dict(),columns=cols)
        updf = pd.concat([updf,cdf])
    
    updf = updf.reset_index().drop('index',axis=1)
    
    updf['date'] = now
    updf['spreadDiff'] = updf['lines'].apply(grabSpreadDiff)
    updf['spread'] = updf['lines'].apply(grabSpread)
    updf['spreadOpen'] = updf['lines'].apply(grabSpreadO)
    updf['homeMoney'] = updf['lines'].apply(grabHMoney)
    updf['awayMoney'] = updf['lines'].apply(grabAMoney)
    updf['favorite'] = updf['lines'].apply(grabTeam)
    updf['uniqID'] = updf['id'].astype('str')+updf['date'].astype('str')

    updf = updf.join(updf.groupby(by='id').mean(),on='id',rsuffix='mean')
    updf['color'] = updf.apply(colorOfMoney,axis=1)
    updf = updf.drop_duplicates(['uniqID'])
    updf = updf.sort_values(by=['startDate','id'],ascending = True)
    updf = updf.set_index('uniqID')
    return (updf)



oldf = pd.read_csv('~/CFB/cfbspread/CFB_Spread_Database.csv',index_col='uniqID').sort_values(by=['startDate','id'])
oldf['date'] = pd.to_datetime(oldf['date'])

#for i in oldf.columns.tolist():

#	print(i)


gameDate = pd.to_datetime(oldf.sort_values(by='startDate',ascending = False)['startDate'])[0]
print(gameDate, type(gameDate))

if dt.datetime.now().replace(tzinfo=None) > gameDate.replace(tzinfo=None):
	wk = int(oldf['week'][len(oldf)-1])+1
else:
	wk = int(oldf.sort_values(by='startDate',ascending=False)['week'][0])

print(f'Week == {wk}')

newdf = grabNewLines(week=wk,year=2025,config=configuration)

#for i in newdf.columns.tolist():
#	print(i)

last_run = pd.to_datetime(oldf.date.unique()[-1])

print(last_run)

holder = oldf[oldf['date']==last_run][['id','spreadmean']].set_index('id')['spreadmean']*(-1)+newdf[['id','spreadmean']].set_index('id')['spreadmean']

newdf['spreadchg'] = newdf['id'].map(holder)

full_monty = pd.concat([oldf,newdf])
print(full_monty)
full_monty.to_csv('~/CFB/cfbspread/CFB_Spread_Database.csv')

#full_monty.set_index('home_team').filter(like='Florida State',axis=0)['date']

"""
# Read CSV file
with open(FILE_PATH, "r") as f:
    content = f.read()

# Check if file already exists
try:
    file = repo.get_contents(GITHUB_FILE_PATH)
    # Update if exists
    repo.update_file(file.path, "Update CSV via Python", content, file.sha, branch="main")
    print("✅ File updated on GitHub.")
except:
    # Create if not exists
    repo.create_file(GITHUB_FILE_PATH, "Add CSV via Python", content, branch="main")
    print("✅ File uploaded to GitHub.")

f.close()
"""
# In[94]:


"""dates = oldf['date'].unique().tolist()
punter = pd.DataFrame()
for i in range(0,len(dates)):
    d = pd.to_datetime(dates[i])
    try:
        y = pd.to_datetime(dates[i+1])
        oldf[oldf['date']==d]
        holder=pd.DataFrame()
        holder['spreadchg'] = oldf[oldf['date']==y][['id','spreadmean']].set_index('id')['spreadmean']*(-1)+oldf[oldf['date']==d][['id','spreadmean']].set_index('id')['spreadmean']
        holder['uniqID'] = holder.index.map(oldf[oldf['date']==d].reset_index().set_index('id')['uniqID'])
        holder.set_index('uniqID', inplace=True)
        punter = pd.concat([punter,holder])
    except IndexError:
        pass

oldf = oldf.join(punter)
oldf.to_csv('CFB_Spread_Database.csv')"""

#Just here to fix the old data frame, other should no longer be needed.


# In[116]:





# In[ ]:




