from scrapy import Spider
from bs4 import BeautifulSoup
import requests
import json
from scoresway_soccer.scoresway_soccer.items import ScoreswaySoccerItem


# https://stackoverflow.com/questions/21788939/how-to-use-pycharm-to-debug-scrapy-projects
# https://viblo.asia/p/crawl-du-lieu-trang-web-voi-scrapy-E375zWr1KGW
# https://dev.to/iankerins/how-to-scrape-amazon-at-scale-with-python-scrapy-and-never-get-banned-44cm
# https://www.geeksforgeeks.org/saving-scraped-items-to-json-and-csv-file-using-scrapy/
# DEBUG: https://stackoverflow.com/a/51949702/10393067

class CrawlerSpider(Spider):
    name = "scoresway_soccer"
    allowed_domains = ["scoresway.com"]
    start_urls = []
    data_dict = {}

    # https://stackoverflow.com/questions/62422172/error-you-dont-have-permission-to-access-url-on-this-server-in-beautiful-so
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36',
    }
    page = requests.get("https://www.scoresway.com/en_GB/soccer/competitions", headers=header)
    soup = BeautifulSoup(page.content, 'html5lib')

    # https://stackoverflow.com/questions/61217541/how-to-extract-json-from-script-tag-using-beautiful-soup
    json_data = json.loads(soup.find('script', attrs={'id': 'compData'}).contents[0])
    continents = json_data['continents']
    for continent in continents:
        countries = continent['countries']
        for country in countries:
            comps = country['comps']
            for comp in comps:
                comp_url = comp['url']
                comp_url = "https://www.scoresway.com" + comp_url[:comp_url.rfind('/')] + "/teams"
                start_urls.append(comp_url)

                # comp_name = comp['name']
                # team_logo_detail_page = requests.get(comp_url, headers=header)
                # detail_soup = BeautifulSoup(team_logo_detail_page.content, 'html5lib')
                # all_seasons = [x['value'] for x in detail_soup.find(id="season-select").find_all('option')]
                #
                # for season in all_seasons:
                #     season_url = "https://www.scoresway.com" + season
                #
                #     season_logo_detail_page = requests.get(season_url, headers=header)
                #     detail_season_logo = BeautifulSoup(season_logo_detail_page.content, 'html5lib')
                #     all_image_data = detail_season_logo.find('ol', attrs={'class': 'teams-list striplist'}).find_all('a')
                #
                #     logos = []
                #     for image_data in all_image_data:
                #         image_url = image_data.find('img')['src']
                #         team = image_data.find('h2').contents[0]
                #         logo_dict = {"image_url": image_url, "team": team}
                #         logos.append(logo_dict)
                #
                #     data_dict["url"] = comp_url
                #     data_dict["name"] = comp_name
                #     data_dict["season"] = season_url
                #     data_dict["logo"] = logos

                    # https://stackoverflow.com/questions/36021332/how-to-prettyprint-human-readably-print-a-python-dict-in-json-format-double-q
                    # json.dumps(data_dict)
                    # start_urls.append(season_url)
                #     break
                # break
            break
        break

    def parse(self, response, **kwargs):

        # https://stackoverflow.com/questions/62422172/error-you-dont-have-permission-to-access-url-on-this-server-in-beautiful-so
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/39.0.2171.95 Safari/537.36',
        }

        comp_url = response.url
        team_logo_detail_page = requests.get(comp_url, headers=header)
        detail_soup = BeautifulSoup(team_logo_detail_page.content, 'html5lib')
        all_seasons = [x['value'] for x in detail_soup.find(id="season-select").find_all('option')]

        for season in all_seasons:
            season_url = "https://www.scoresway.com" + season

            season_logo_detail_page = requests.get(season_url, headers=header)
            detail_season_logo = BeautifulSoup(season_logo_detail_page.content, 'html5lib')
            all_image_data = detail_season_logo.find('ol', attrs={'class': 'teams-list striplist'}).find_all('a')

            logos = []
            for image_data in all_image_data:
                image_url = image_data.find('img')['src']
                team = image_data.find('h2').contents[0]
                logo_dict = {"image_url": image_url, "team": team}
                logos.append(logo_dict)

            item = ScoreswaySoccerItem()
            item['tournament_url'] = comp_url
            item['name'] = comp_url
            item['season_url'] = season_url
            item['logos'] = logos

            yield item
