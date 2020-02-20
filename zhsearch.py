import requests
from bs4 import BeautifulSoup
import datetime
import json
import urllib3


def scrape(event, context):
    qp = 0
    srchtext = 'HSBC'
    if 'queryStringParameters' in event and 'page' in event['queryStringParameters']:
      qp = int(event['queryStringParameters']['page'])
    if 'queryStringParameters' in event and 'srchtext' in event['queryStringParameters']:
      srchtext = event['queryStringParameters']['srchtext']
    data = deal_scrape(srchtext, qp)
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }


def deal_scrape(search, page):
  url = 'https://www.zerohedge.com/search-content?search_api_fulltext=' + search + '&sort_by=search_api_relevance'
  if page > 0:
    url = url + '&page=' + str(page)

  req = urllib3.PoolManager()
  res = req.request('GET', url, headers={
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
  })

  content = BeautifulSoup(res.data, 'html.parser')
  div = content.find(id="block-zerohedge-content")
  items = div.find_all("div", {"class": "views-row"})
  result = []
  for item in items:
    href = item.span.span.a['href']
    title = item.span.span.a.text
    teaser = item.findAll('div', {'class': 'views-field views-field-search-api-excerpt'})[0]
    introduction = ''.join(map(str, teaser.span.contents))
    updated = item.findAll('div', {'class': 'views-field views-field-created'})[0].span.text

    result.append({'reference': href, 'introduction': introduction, 'title': title, 'updated': updated})
  return result
