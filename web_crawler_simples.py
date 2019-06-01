# FONTE: https://www.youtube.com/playlist?list=PLp55XiVzZ1_iUYan9C3NsWhdkw4Gbnovx

from lxml import html
import requests

class Crawler:

    def __init__(self, starting_url, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.current_depth = 0
        self.depth_links = []
        self.pursued_objects = []

    def crawl(self):
        object = self.get_object_from_link(self.starting_url)
        self.pursued_objects.append(object)
        self.depth_links.append(object.links)

        while self.current_depth < self.depth:
            current_links = []
            for link in self.depth_links[self.current_depth]:
                current_object = self.get_object_from_link(link)
                self.pursued_objects.append(current_object)
                current_links.extend(current_object.links)
                
            self.depth_links.append(current_links)
            self.current_depth +=1

        return print('\n Crawler status | Rodou Belezinha! : ) \n')


    def get_object_from_link(self, link):
        start_page = requests.get(link)
        tree = html.fromstring(start_page.text)

        name = tree.xpath('//h1[@class="product-header__title app-header__title"]/text()')[0]
        developer = tree.xpath('//dd[@class="information-list__item__definition l-column medium-9 large-6"]/text()')[0]
        price = tree.xpath('//dd[@class="information-list__item__definition l-column medium-9 large-6"]/text()')[6]
        links = tree.xpath('//div[@class="l-row l-row--peek"]//a/@href')

        object = PursuedObjects(name, developer, price, links)

        return object


class PursuedObjects:

    def __init__(self, name, developer, price, links):
        self.name = name
        self.developer = developer
        self.price = price
        self.links = links

    def __str__(self):

        return( '\n --------------------------------' +
                '\n Name: ' + self.name + 
                '\n Developer: ' + self.developer + 
                '\n Price: ' + self.price + '\n' +
                '\n --------------------------------')


## crawleando a pagina do candy crush saga para obter os aplicativos (jogos) do mesmo desenvolvedor ##

crawler = Crawler(starting_url = 'https://itunes.apple.com/br/app/candy-crush-saga/id553834731?mt=8', depth = 1) #inicializando o crawler
crawler.crawl() #executando o processo de crawler

#visualizando resultados obtidos
for object in crawler.pursued_objects:
    print(object)