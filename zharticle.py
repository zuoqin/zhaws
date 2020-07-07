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
    return {
        'statusCode': 200,
        'body': json.dumps(data)
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

  body = ''.join(map(str,  item.findAll('div', {'class': "node__content"})[0].contents))

  body = body.replace("https://www.zerohedge.com/news", "https://news.ehedge.xyz/story?url=%2Fnews")
  body = body.replace("https://www.zerohedge.com/article", "https://news.ehedge.xyz/story?url=%2Farticle")
  body = body.replace("https://www.zerohedge.com/markets", "https://news.ehedge.xyz/story?url=%2Fmarkets")
  body = body.replace("https://www.zerohedge.com/health", "https://news.ehedge.xyz/story?url=%2Fhealth")
  body = body.replace("https://www.zerohedge.com/economics", "https://news.ehedge.xyz/story?url=%2Feconomics")
  body = body.replace("/s3/files", "https://www.zerohedge.com/s3/files")
  updated = item.findAll('div', {'class': "submitted-datetime"})[0].span.text

  return [{'body': body, 'title': title, 'updated': updated}]
