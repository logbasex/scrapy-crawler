from scrapy import Spider
from scrapy.selector import Selector
from hanoicomputer_crawler.items import HanoicomputerCrawlerItem
from bs4 import BeautifulSoup
import requests


# https://stackoverflow.com/questions/21788939/how-to-use-pycharm-to-debug-scrapy-projects
# https://viblo.asia/p/crawl-du-lieu-trang-web-voi-scrapy-E375zWr1KGW
# https://dev.to/iankerins/how-to-scrape-amazon-at-scale-with-python-scrapy-and-never-get-banned-44cm
# https://www.geeksforgeeks.org/saving-scraped-items-to-json-and-csv-file-using-scrapy/
class CrawlerSpider(Spider):
    name = "crawler"
    allowed_domains = ["hanoicomputer.vn"]
    start_urls = []
    category_dict = {}
    page = requests.get("https://www.hanoicomputer.vn/")
    soup = BeautifulSoup(page.content, 'html5lib')

    category_list = soup.find('div', attrs={'class': 'homepage-slider-left'})
    all_categories = category_list.findAll('li', attrs={'class': 'js-hover-menu'})

    # https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/
    for category in all_categories:
        category_url = "https://www.hanoicomputer.vn" + category.a['href']
        category_dict[category_url] = category.a.get_text()
        detail_page = requests.get(category_url)
        detail_soup = BeautifulSoup(detail_page.content, 'html5lib')
        all_pages = detail_soup.findAll("div", attrs={'class': 'paging'})
        for page in all_pages:
            page_url = "https://www.hanoicomputer.vn" + page.a['href']
            start_urls.append(page_url)

    def parse(self, response, **kwargs):
        # products = Selector(response).xpath('//*[@id="159"]/div[7]/div[2]/div/div[3]/div/div[3]/div')
        products = Selector(response).xpath('/html/body/div[7]/div[2]/div/div[3]/div/div[3]/div')

        i = 1
        for product in products:
            item = HanoicomputerCrawlerItem()

            item['category'] = self.category_dict[response.url]
            # https://stackoverflow.com/a/36282538
            product_link_xpath = '/html/body/div[7]/div[2]/div/div[3]/div/div[3]/div[' + str(i) + ']/div[2]/a/@href'
            item['link'] = "https://www.hanoicomputer.vn" + product.xpath(product_link_xpath).extract_first()

            product_image_xpath = '/html/body/div[7]/div[2]/div/div[3]/div/div[3]/div[' + str(i) + ']/div[2]/a/img/@data-src'
            item['image'] = product.xpath(product_image_xpath).extract_first()
            # item['image'] = product.xpath('/html/body/div[7]/div[2]/div/div[3]/div/div[3]/div[5]/div[2]/a/img/@data-src').extract_first()

            product_name_xpath = '/html/body/div[7]/div[2]/div/div[3]/div/div[3]/div[' + str(i) + ']/div[4]/h3/a/text()'
            item['product_name'] = product.xpath(product_name_xpath).extract_first()
            # item['product_name'] = product.xpath('/html/body/div[7]/div[2]/div/div[3]/div/div[3]/div[11]/div[3]/p').extract_first()

            product_code_xpath = '/html/body/div[7]/div[2]/div/div[3]/div/div[3]/div[' + str(i) + ']/div[3]/p/text()'
            item['product_code'] = product.xpath(product_code_xpath).extract_first().replace("Mã: ", "")
            # item['product_code'] = product.xpath('/html/body/div[7]/div[2]/div/div[3]/div/div[3]/div[1]/div[3]/p/text()').extract_first()

            product_price_xpath = '/html/body/div[7]/div[2]/div/div[3]/div/div[3]/div[' + str(i) + ']/div[4]/span[3]/@data-price'
            price = product.xpath(product_price_xpath).extract_first()
            # https://stackoverflow.com/a/67391888/10393067
            # item['price'] = format(int(price), ',').replace(',', '.')
            item['price'] = price
            # item['price'] = product.xpath('/html/body/div[7]/div[2]/div/div[3]/div/div[3]/div[35]/div[4]/span[3]').extract_first()

            i = i + 1
            yield item
