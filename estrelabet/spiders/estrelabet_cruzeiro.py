import scrapy
import json
from datetime import datetime
from scrapy_splash import SplashRequest


class EstrelabetCruzeiroSpider(scrapy.Spider):
    name = "estrelabet_cruzeiro"
    allowed_domains = ["wwww.estrelabet.com", "estrelabet.com"]
    start_urls = [
        "https://estrelabet.com/api-v2/name-search/d/23/estrelabet/cruzeiro"]
    ODDS_HEADERS = ["Resultado", "Ambas equipes marcam"]

    script = """
    function main(splash, args)
    	splash:set_user_agent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

        assert(splash:go(args.url))
        assert(splash:wait(0.5))
        return {
            cookies = splash:get_cookies()
        }
        end
    """

    def start_requests(self):
        yield SplashRequest(
            url="https://www.estrelabet.com/",
            callback=self.get_game_data,
            endpoint="execute",
            args={"lua_source": self.script}
        )

    def get_game_data(self, response):
        print(response.request.headers.getlist('Set-Cookie'))
        print(response.cookiejar)
        yield scrapy.Request(
            method="POST",
            url=self.start_urls[0],
            callback=self.parse,
            headers={
                "Bragiurl": "https://bragi.sportingtech.com/"
            },
            body=json.dumps({
                "requestBody": {
                    "name": "cruzeiro",
                    "bragiUrl": "https://bragi.sportingtech.com/"
                },
                "device": "d",
                "languageId": 23
            })
        )

    def parse(self, response):
        # with open("initial_response.json", "wb") as f:
        #     f.write(response.body)
        print(response.headers)

        search_response = json.loads(response.body)
        games_data = self.filter_and_process_relevant_data(search_response)
        next_game = self.get_next_game(games_data)
        self.print_next_game_details(next_game)

    def filter_and_process_relevant_data(self, search_response):
        return [game for sport in search_response["data"][0]["cs"] for game in self.process_sport(sport)]

    def process_sport(self, sport):
        return [game for league in sport["sns"] for game in self.process_league(league)]

    def process_league(self, league):
        return [self.process_game(game) for game in league["fs"] if "acN" in game and game["acN"]]

    def process_game(self, game):
        relevant_raw_odds = [odd for odd in game["btgs"]
                             if odd["btgNO"] in self.ODDS_HEADERS]
        return {
            "datetime": game["fsd"],
            "homeContestant": game["hcN"],
            "awayContestant": game["acN"],
            "odds": [self.process_odd(odd) for odd in relevant_raw_odds],
        }

    def process_odd(self, odd):
        return {
            "headerDescription": odd["btgNO"],
            "data": [{"value": odd_data["hO"], "subDescription": odd_data["oc"]} for odd_data in odd["fos"]],
        }

    def get_next_game(self, games_data):
        return min(games_data, key=lambda game: game["datetime"])

    def print_next_game_details(self, game):
        timestamp_in_seconds = game['datetime'] / 1000
        game_date = datetime.fromtimestamp(timestamp_in_seconds)

        formatted_date = game_date.strftime("%d/%m/%Y - %H:%M")

        print(
            f"\nPróximo jogo: {game['homeContestant']} x {game['awayContestant']} - {formatted_date}")
        for odd in game["odds"]:
            print(f"\n{odd['headerDescription']}")
            for odd_data in odd["data"]:
                print(f"\t{odd_data['subDescription']}: {odd_data['value']}")
