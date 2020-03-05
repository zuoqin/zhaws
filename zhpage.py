import urllib3
from bs4 import BeautifulSoup
import datetime

def scrape(event, context):
    import json
    qp = 3
    if 'queryStringParameters' in event and 'page' in event['queryStringParameters']:
      qp = event['queryStringParameters']['page']
    data = deal_scrape(qp)
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }


def deal_scrape(page):
  url = 'https://www.zerohedge.com/?page=' + str(page)

  req = urllib3.PoolManager()
  res = req.request('GET', url, headers={
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
  })

  content = BeautifulSoup(res.data, 'html.parser')
  div = content.find(id="block-zerohedge-content")
  items = div.find_all("div", {"class": "views-row"})
  result = []
  for item in items:
    h2 = item.findAll('h2', {'class':"teaser-title"})[0]
    href = h2.a['href']
    title = h2.a.span.text
    teasers = item.findAll('div', {'class': 'teaser-text'})
    if len(teasers) < 1:
      introduction = ''
    else:
      introduction = ''.join(map(str, teasers[0].div.contents))

    image = item.findAll('div', {'class': 'teaser-image'})[0].img['src']
    image = image.replace('/s3/files', 'https://zerohedge.com/s3/files')
    for li in item.footer.ul:
        if li.get('class')[0] == 'extras__created':
            updated = li.span.text
            break

    result.append({'reference': href, 'introduction': introduction, 'picture': image, 'title': title, 'updated': updated})
  return result
