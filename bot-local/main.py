
import discord 
import os
import pandas as pd 

client = discord.Client()


## Initiate IEX 
import pyEX as p 
iex = p.Client(api_token=iex_key, version='stable')
## Get Quote

## Get News 
## Date 
import datetime
def convert_date(x):
    stamp = x
    date = datetime.datetime.fromtimestamp(stamp / 1e3)
    date = date.strftime("%Y-%m-%d")
    return date 



    
    ### Quote 

tkr = 'amd'
quote = iex.quote(symbol=tkr)
print(quote['iexRealtimePrice'])

### News 
# tkr = 'amd'
# news = iex.news(count = 1,symbol = tkr)
# news = pd.DataFrame(news)
# news = news.rename(columns = {'datetime': 'Date'})
# for i in range(len(news)): 
#     news['Date'][i] = convert_date(news['Date'][i])
# news['Date'] = pd.to_datetime(news['Date'])
# news = news.sort_values(by = 'Date')
# news = news[:1]


# news = news.reset_index()
# headline = news['headline'][0]
# date = news['Date'][0].strftime('%Y-%m-%d')


# embedVar = discord.Embed(title=tkr.upper(), description=str(headline),color=0x00ff00)
# embedVar.add_field(name="Source", value=news['source'][0], inline=False)
# embedVar.add_field(name="Pusblish Date", value=date, inline=False)
# embedVar.add_field(name="Summary", value=news['summary'][0], inline=False)
# embedVar.add_field(name="url", value=news['url'][0], inline=False)
# await message.channel.send(embed=embedVar)


client.run(disc_key)