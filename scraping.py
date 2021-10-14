import requests
import lxml.html as html

HOME_URL = 'https://www.infobae.com/'


XPATH_LINK_TO_ARTICLE = '//a[@class="cst_ctn"]/@href'
XPATH_TITLE = '//h1[@class="article-headline"]/text()'
XPATH_SUMMARY = '//h2[@class="article-subheadline"]/text()'
XPATH_BODY = '//div[@class="nd-body-article"]/p[@class="paragraph"]/text()'

def parse_home():
    try:
        response = requests.get(HOME_URL)
        
        if response.status_code == 200: #para saber el estado de la pagina con .status_code
            home = response.content.decode('utf-8') # response.content responde el documnto html de la respuesta y decode modifica los caracteres para que no de error
            parsed = html.fromstring(home) #esta lina toma el contenido de html lo transforma en un documento especial para usar xpath
    
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE) #obtiene una lista de todo el resultadod de aplicar xpath
            print(len(links_to_notices))
            print(links_to_notices)
            
        else:
            raise ValueError(f"Error: {response.status_code}")


    except ValueError as ve: 
        print(ve)

def main():
    parse_home()

if __name__ == '__main__':
    main()

