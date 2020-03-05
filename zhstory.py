import requests
from bs4 import BeautifulSoup
import datetime
import json
import urllib3


def scrape(event, context):
    qp = '/political/coupgate-localized-civil-war-now-underway-doj'
    if 'queryStringParameters' in event and 'url' in event['queryStringParameters']:
      qp = event['queryStringParameters']['url']
    data = deal_scrape(qp)
    html = """
    <!DOCTYPE html>
    <html>
    <head>
      <title>{}</title>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    </head>
    <body>

    <h1>{}</h1>
    {}
    <p>{}</p>

    </body>
    </html>
    """
    return {
        'statusCode': 200,
        'headers': {"content-type": "text/html"},
        'body': html.format(data['title'], data['title'], data['body'], data['updated'])
    }

def deal_scrape(article):
  url = 'https://www.zerohedge.com' + str(article)
  req = urllib3.PoolManager()
  res = req.request('GET', url, headers={
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
  })

  content = BeautifulSoup(res.data, 'html.parser')
  div = content.find('div', {'class': "layout-content"})
  item = div
  title = ''.join(map(str, item.findAll('h1', {'class': "page-title"})[0].span.contents))

  body = ''.join(map(str,  item.findAll('div', {'class': "node__content"})[0].findAll('div', {'property': "schema:text"})[0].contents))

  updated = item.findAll('div', {'class': "submitted-datetime"})[0].span.text

  return {'body': body, 'title': title, 'updated': updated}
