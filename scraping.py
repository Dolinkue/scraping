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
root = 'https://www.infobae.com'




def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                print(title)
                title = title.replace('\"', "") 
                title = title.replace('?', "") 
                title = title.replace('¿', "")
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError: # puede que hay noticias que no tienen summary o algo entonces con esto salgo 
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
        if response.status_code == 200: #para saber el estado de la pagina con .status_code
            home = response.content.decode('utf-8') # response.content responde el documnto html de la respuesta y decode modifica los caracteres para que no de error
            parsed = html.fromstring(home) #esta lina toma el contenido de html lo transforma en un documento especial para usar xpath  
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE) #obtiene una lista de todo el resultadod de aplicar xpath
            links_to_notices =[root + x for x in links_to_notices]
            #print(len(links_to_notices))
            #print(links_to_notices)
            today = datetime.date.today().strftime('%d-%m-%Y') #te nos trae la fecha today la de hoy, con strftime nos da el formato de como la queremos
            if not os.path.isdir(today): #estoy preguntando si no exite os.path nos trae un T o F si esta today si no esta la creamos
                os.mkdir(today)

            for link in links_to_notices: # a partit de cada link entro en cada nota y extraigo la info               
                
                parse_notice(link, today)    

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()
    

if __name__ == "__main__":
    run()
