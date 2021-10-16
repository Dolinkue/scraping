import requests
import lxml.html as html
import os 
import datetime

from requests.models import Response



HOME_URL = 'https://www.infobae.com/'


XPATH_LINK_TO_ARTICLE = '//a[@class="cst_ctn"]/@href'
XPATH_TITLE = '//h1[@class="article-headline"]/text()'
XPATH_SUMMARY = '//h2[@class="article-subheadline"]/text()'
XPATH_BODY = '//div[@class="nd-body-article"]/p[@class="paragraph"]/text()'


def get_title(link):
    #separamos por "/" y nos quedamos con el ultimo que elemento 
    url = link.split('/')[-1]
    #separamos por "-" y eliminamos el ultimo elemento
    title_list=url.split('-')[:-1]
    #Unimos lo anterior
    title = " ".join(title_list)

    return(title)

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = get_title(link)
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                print("as")
                return
            
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
            
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notices)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notices:
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()
    

if __name__ == "__main__":
    run()