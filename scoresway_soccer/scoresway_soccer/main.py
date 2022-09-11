import json

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':

    output = []
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
                comp_name = comp['name']
                team_logo_detail_page = requests.get(comp_url, headers=header)
                detail_soup = BeautifulSoup(team_logo_detail_page.content, 'html5lib')

                try:
                    all_seasons = [x['value'] for x in detail_soup.find(id="season-select").find_all('option')]
                except:
                    print("No season: ", comp_url)
                    all_seasons = [comp_url]

                team_data = []

                all_seasons = all_seasons[0:3]
                for season in all_seasons:
                    season_url = season.find('https://www.scoresway.com') == -1 and "https://www.scoresway.com" + season or season

                    print('Crawl logo from continent: {0}, organization: {1}, tournamentName: {2} and seasonUrl: {3}'
                          .format(continent['name'], country['name'], comp_name, season_url))

                    season_logo_detail_page = requests.get(season_url, headers=header)
                    detail_season_logo = BeautifulSoup(season_logo_detail_page.content, 'html5lib')
                    try:
                        all_image_data = detail_season_logo.find('ol',
                                                                 attrs={'class': 'teams-list striplist'}).find_all('a')
                    except:
                        continue

                    logos = []
                    for image_data in all_image_data:
                        if image_data.find('img'):
                            image_url = image_data.find('img')['src']
                            team = image_data.find('h2').contents[0]
                            logo_dict = {"image_url": image_url, "team": team}
                            logos.append(logo_dict)

                    data_dict = {"url": comp_url, "season": season_url, "logo": logos}
                    team_data.append(data_dict)
                    tournaments_dict = {"tournaments": comp_name, "data": team_data}
                    output.append(tournaments_dict)
                    # https://stackoverflow.com/questions/36021332/how-to-prettyprint-human-readably-print-a-python-dict-in-json-format-double-q
                    # json.dumps(data_dict)
                    # break
                # break
            # break
        # break

    # print(json.dumps(output))

    with open("/home/logbasex/Desktop/soccer.json", "w") as outfile:
        json.dump(output, outfile, indent=4, separators=(',', ': ')) # https://howtodoinjava.com/json/append-json-to-file/
