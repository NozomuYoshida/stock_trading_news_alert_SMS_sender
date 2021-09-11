# APIs
# https://www.alphavantage.co/
# https://newsapi.org/docs/endpoints/everything
# https://www.twilio.com

import os
import datetime as dt
import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

URL_NEWS_API = 'https://newsapi.org/v2/everything'
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

URL_ALPHA_VANTAGE = 'https://www.alphavantage.co/query'
ALPHA_VANTAGE_API_KEY =  os.environ.get('ALPHA_VANTAGE_API_KEY')

ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')

# Replace to Twilio / your phone number
FROM_PHONE_NUMBER = [Twilio phone number]
TO_PHONE_NUMBER = [Your phone number]


def send_sms(message_body):
    # Switch the statement below if you use python anywhere
    # client = Client(account_sid, auth_token, http_client=proxy_client)
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    sms_message = client.messages.create(
        body=message_body,
        from_=FROM_PHONE_NUMBER,
        to=TO_PHONE_NUMBER
    )
    print(sms_message.status)


today = dt.datetime.now().date()
delta_1day = dt.timedelta(days=1)
yesterday = today - delta_1day
the_day_before_yesterday = yesterday - delta_1day

# Get the stock information
parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': 'TSLA',
    'apikey': ALPHA_VANTAGE_API_KEY
}

response = requests.get(url=URL_ALPHA_VANTAGE, params=parameters)
response.raise_for_status()
data = response.json()['Time Series (Daily)']
yesterday_close = float(data[yesterday.__str__()]['4. close'])
the_day_before_yesterday_close = float(data[the_day_before_yesterday.__str__()]['4. close'])
change_rate = (the_day_before_yesterday_close - yesterday_close) * 100 / the_day_before_yesterday_close
change_rate = 5

# Get the first 3 news pieces for the COMPANY_NAME.
parameters = {
    # 'q': COMPANY_NAME,
    'qInTitle': COMPANY_NAME,
    'apiKey': NEWS_API_KEY
}

response = requests.get(url=URL_NEWS_API, params=parameters)
response.raise_for_status()
news_data = response.json()
first_3_news = news_data['articles'][0:3]

# Send sms When STOCK price increase/decreases by 5% between yesterday and the day before yesterday
if abs(change_rate) >= 5:
    print('Get News')
    mark = None
    if change_rate > 0:
        mark = f'🔺{change_rate: 2}%'
    else:
        mark = f'🔻{change_rate: 2}%'

    for news in first_3_news:
        source = news['source']['name']
        title = news['title']
        description = news['description']
        url = news['url']
        published_date = news['publishedAt']
        content = news['content']
        # There seems to be string number limitation for twilio trial plan
        message = f'{COMPANY_NAME}: {mark}\n' \
                  f'Headline: {title}\n' \
                  f'Url: {url}\n' \
                  f'Published Date: {published_date}\n'
        print(message)
        send_sms(message)

else:
    print('Change rate did not exceed 5%')

