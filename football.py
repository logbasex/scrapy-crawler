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

    leagues_urls = [
        "https://www.scoresway.com/en_GB/football/ncaa-division-i-fbs-ncaa-division-i-fbs-2021-2022/eduyhr4uewgbugto7g7hlk00k/teams",
        "https://www.scoresway.com/en_GB/football/nfl-nfl-2021-2022/al1jihg0wvd8m27zgakgd3ndg/teams"
    ]

    for league_url in leagues_urls:
        team_logo_detail_page = requests.get(league_url, headers=header)
        detail_soup = BeautifulSoup(team_logo_detail_page.content, 'html5lib')

        try:
            all_seasons = [x['value'] for x in detail_soup.find(id="season-select").find_all('option')]
        except:
            print("No season: ", league_url)
            all_seasons = [league_url]

        team_data = []

        all_seasons = all_seasons[0:3]
        for season in all_seasons:
            season_url = season.find('https://www.scoresway.com') == -1 and "https://www.scoresway.com" + season or season

            season_logo_detail_page = requests.get(season_url, headers=header)
            detail_season_logo = BeautifulSoup(season_logo_detail_page.content, 'html5lib')
            try:
                all_image_data = detail_season_logo.find('ol', attrs={'class': 'teams-list striplist'}).find_all('a')
            except:
                continue

            logos = []
            for image_data in all_image_data:
                if image_data.find('img'):
                    image_url = image_data.find('img')['src']
                    team = image_data.find('h2').contents[0]
                    logo_dict = {"image_url": image_url, "team": team}
                    logos.append(logo_dict)

            output.append(logos)

    # print(json.dumps(output))

    with open("/home/logbasex/Desktop/scrapy/football.json", "w") as outfile:
        json.dump(output, outfile, indent=4, separators=(',', ': ')) # https://howtodoinjava.com/json/append-json-to-file/
