# stock_trading_news_alert_SMS_sender
This is a SMS sender that alerts stock trading news when stock price increase/decreases by 5% between yesterday and the day before yesterday

## Function
- Send sms when stock price increase/decreases by 5% between yesterday and the day before yesterday

## Usage
- To run, replace API_KEY to your own api key (registration needed)
- Set your own api key of OpenWeather: https://www.alphavantage.co
  - Replace ```os.environ.get('ALPHA_VANTAGE_KEY')``` to your own api key
- Set your own api key of news api: https://newsapi.org
  - Replace ```os.environ.get('NEWS_API_KEY')``` to your own api key
- Set your own authentification token of Twilio: https://console.twilio.com/
  - Replace ```os.environ.get('AUTH_TOKEN')``` to your own api token
- To run automatically, Python anywhere is recommended: https://www.pythonanywhere.com/
  - Set to run the main.py as the the daily task

## Environment
- MacOS (11.52)
- PyCharm 2021.02 (Community Edition)
