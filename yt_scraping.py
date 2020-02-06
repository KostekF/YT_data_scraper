import requests
import logging
from bs4 import BeautifulSoup
from datetime import date
import sys
import json

from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed as future_as_completed

logging.basicConfig(level=logging.INFO)


def get_site_html(search_phrase):
    base = 'https://www.youtube.com'
  
    r = requests.get(base+search_phrase)
    
    try:
        r.raise_for_status()
        return r
    except:
        print('site not found, requests failed')
        return None
    
def get_video_links(search_phrase):
    
    r = get_site_html('/results?search_query='+search_phrase)
    soup = BeautifulSoup(r.text,'html.parser')
    #open("video.html", "w", encoding='utf8').write(r.text)

    video_links = []
    all_videos = soup.find_all("a", class_="yt-uix-tile-link")

    for link in all_videos:
        video_link = link.get('href')
        if 'watch' in video_link:
            video_links.append(video_link)
    return video_links


def get_title_info(link, search_phrase):
    title_dict = {}
    title_dict['link'] = link
    r = get_site_html(link + '/')

    soup = BeautifulSoup(r.text, 'html.parser')
    description_html = soup.find(id='eow-description')
    description = description_html.text
    title_dict['description'] = description

    name = soup.find(class_='watch-title').text.strip()
    title_dict['name'] = name

    category_html = soup.find_all('a', class_='yt-uix-sessionlink spf-link')
    category = category_html[-1].text
    title_dict['category'] = category

    today = date.today()
    access_date = today.strftime("%d-%m-%Y")
    title_dict['access_date'] = access_date

    add_date_unformated = soup.find(class_='watch-time-text').text[-11:].strip()
    add_date = ''
    months = {'sty': '01', 'lut': '02', 'mar': '03', 'kwi': '04', 'maj': '05', 'cze': '06',
              'lip': '07', 'sie': '08', 'wrz': '09', 'paź': '10', 'lis': '11', 'gru': '12'}
    for month_key, month_num in months.items():
        if month_key in add_date_unformated:
            add_date_unformated = add_date_unformated.replace(month_key, month_num)
            add_date = add_date_unformated.replace(' ', '-')

    title_dict['add_date'] = add_date

    search_key = search_phrase
    title_dict['search_key'] = search_key

    return title_dict


if __name__ == "__main__":

    search_phrase = 'itil/'
    if len(sys.argv) > 1:
        search_phrase = '+'.join(sys.argv[1:])

    video_links = get_video_links(search_phrase)
    videos = []
    titles = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_url = {executor.submit(get_title_info, link, search_phrase): link for link in video_links}
        for future in future_as_completed(future_to_url):
            url = future_to_url[future]
            try:
                title_dict = future.result()
                titles.append(title_dict)
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
           #else:
                #print('%r page is %d bytes' % (url, len(data)))

    json_dp = json.dumps(titles)
    print(json_dp)







