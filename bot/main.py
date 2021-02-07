import discord 
import os
import sqlalchemy
import psycopg2
import pandas as pd 
import sqlalchemy
## Discord Clinet ##
client = discord.Client()

## Postgres Client
engine = sqlalchemy.create_engine(os.getenv('DATABASE_URL'))
con = engine.connect()
portfolio = pd.read_sql_table(
    'portfolio',
    con=engine
)


### ###
## Initiate IEX 
import pyEX as p 
iex = p.Client(api_token=os.getenv('iex_key'), version='stable')
# iex = p.Client(api_token=iex_key, version='stable')

## Get Quote

## Get News 
## Date 
import datetime
def convert_date(x):
    stamp = x
    date = datetime.datetime.fromtimestamp(stamp / 1e3)
    date = date.strftime("%Y-%m-%d")
    return date 


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    msg = message.content
    
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send(msg)
        await message.channel.send('Hello!')
    
    ### Portfolio 
    if message.content.startswith('$Portfolio add'): # Portfolio -name -add/remove tkr
        mes = msg.split()
        name = mes[1]
        tkr = mes[3].upper()

 
        
        quote = iex.quote(symbol=tkr)
        price = quote['latestPrice']
        
        local_df = pd.DataFrame({"name" : name,
            "ticker": tkr,
            'orig_price' : price, 
            'new_price': 0}, index = [0])
        #
        connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        cursor = connection.cursor()
        cursor.execute("INSERT INTO PORTFOLIO (name, ticker, orig_price, new_price) VALUES ('{0}', '{1}', '{2}', '{3}')".format(name, tkr, price, 0));
        connection.commit()
        
        print("Record inserted successfully")
        connection.close()
        del(local_df)
        await message.channel.send('Ticker has been added to the portfolio:')


# if message.content.startswith('$Portfolio remove'): # Portfolio -name -add/remove tkr
#     mes = msg.split()
#     name = mes[1]
#     tkr = mes[3].upper()

    # if message.content.startswith('$Portfolio'): # Portfolio -name -add/remove tkr
    #     await message.channel.send(portfolio['name'][0])
            # await message.channel.send(portfolio['tckr'][0])
            # await message.channel.send(portfolio['orig_price'][0])
    
    ### Quote 
    if message.content.startswith('$Quote'):
        mes = msg.split()
        tkr = mes[1]
        print(mes, tkr)
        quote = iex.quote(symbol=tkr)
        price = quote['latestPrice']
        await message.channel.send(price)

    ### News 
    if message.content.startswith('$News'):
        mes = msg.split()
        tkr = mes[1]
        news = iex.news(count = 1,symbol = tkr)
        news = pd.DataFrame(news)
        news = news.rename(columns = {'datetime': 'Date'})
        for i in range(len(news)): 
            news['Date'][i] = convert_date(news['Date'][i])
        news['Date'] = pd.to_datetime(news['Date'])
        news = news.sort_values(by = 'Date')
        news = news[:1]
        news = news.reset_index()
        headline = news['headline'][0]
        date = news['Date'][0].strftime('%Y-%m-%d')
        
        summary = news['summary'][0]
        if len(summary) > 100: 
            summary = summary[:100]
        else: 
            summary = summary
        embedVar = discord.Embed(title=tkr.upper(), description=str(headline),color=0x00ff00)
        embedVar.add_field(name="Source", value=news['source'][0], inline=False)
        embedVar.add_field(name="Pusblish Date", value=date, inline=False)
        embedVar.add_field(name="Summary", value= summary , inline=False)
        embedVar.add_field(name="url", value=news['url'][0], inline=False)
        await message.channel.send(embed=embedVar)

# client.run(disc_key)
client.run(os.getenv('disc_key'))