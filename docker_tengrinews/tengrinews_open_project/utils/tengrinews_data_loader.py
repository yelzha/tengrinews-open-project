import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tengrinews_open_project.utils.date_utils import parse_russian_date


def __get_news_info(url) -> dict:
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return {}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_title = soup.find('h1', class_='head-single').get_text(strip=True)
    news_content_soup = soup.find('div', class_='content_main_text')
    
    p_tags = news_content_soup.find_all('p')
    last_p = p_tags[-1]
    last_p.decompose()

    hashtags_soup = news_content_soup.find('div', class_='content_main_text_tags')
    hashtags = ', '.join([i.text.lower() for i in hashtags_soup.find_all('a')])
    hashtags_soup.decompose()
    
    news_content = news_content_soup.get_text(strip=True)
    news_date = soup.find('div', class_='date-time').get_text(strip=True)

    return {
        'title': news_title,
        'content': news_content,
        'hashtags': hashtags,
        'date_txt': news_date
    }

def __get_views(news_id) -> int:
    response = requests.get(f'https://counter.tengrinews.kz/inc/tengrinews_ru/news/{news_id}')
    if response.status_code == 200:
        return response.json()['result']

    return None


def get_list_news(ingestion_date = None) -> list:
    news_list = []
    start_page = 1
    
    while start_page < 50:
        url = f'https://tengrinews.kz/news/page/{start_page}/'
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for content_main_item in soup.find_all('div', class_='content_main_item'):
    
                text_date = list(
                    content_main_item.find('div', class_='content_main_item_meta')
                )[1].text.strip()

                news_datetime = parse_russian_date(text_date).date()

                
                
                if ingestion_date.date() > news_datetime:
                    break
                
                if ingestion_date.date() == news_datetime:
                    href = content_main_item.find('a').get('href')
                    page_url = f'https://tengrinews.kz'+href
                    category = href.split('/')[1]
                    item_id = href[:-1].split('-')[-1]
                    news_info = __get_news_info(page_url)
                    news = {
                        'page_url': page_url,
                        'category': category,
                        'page_id': item_id
                    }
                    news.update(news_info)
                    news['views_count'] = __get_views(item_id)
                    news_list.append(news)
                
            if ingestion_date.date() > news_datetime:
                break
                    
        else:
            raise Exception(f'Failed to retrieve page {page_number}')
    
        start_page += 1
        # time.sleep(0.5)

    return news_list


def __expand_childs(comment_list, additional_data: dict=None) -> list:
    expanded_comment_list = []
    while comment_list:
        current_comment = comment_list.pop(0)
        comment_list += current_comment['child']
        if additional_data:
            current_comment = {**current_comment, **additional_data}
        del current_comment['child']
        expanded_comment_list.append(current_comment)
    return expanded_comment_list


def get_comments(comment_id = '511502', additional_data: dict=None) -> list:
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://tengrinews.kz/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    body = "{\"id\":\""+str(comment_id)+"\",\"type\":\"news\",\"lang\":\"ru\",\"sort\":\"best\"}"

    response = requests.post('https://c.tn.kz/comments/get/list/', data=body, headers=headers)

    if response.status_code == 200:
        response_json = response.json()

        return __expand_childs(response_json['list'], additional_data)
    return []