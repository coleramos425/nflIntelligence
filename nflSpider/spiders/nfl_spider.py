from ..items import PlayerItem

import scrapy
from scrapy import Request

class QuotesSpider(scrapy.Spider):
    name = "nflData"

    start_urls = [
        'https://www.footballdb.com/teams/nfl/arizona-cardinals/roster/2019',
        'https://www.footballdb.com/teams/nfl/atlanta-falcons/roster/2019',
        'https://www.footballdb.com/teams/nfl/baltimore-ravens/roster/2019',
        'https://www.footballdb.com/teams/nfl/buffalo-bills/roster/2019',
        'https://www.footballdb.com/teams/nfl/carolina-panthers/roster/2019',
        'https://www.footballdb.com/teams/nfl/chicago-bears/roster/2019',
        'https://www.footballdb.com/teams/nfl/cincinnati-bengals/roster/2019',
        'https://www.footballdb.com/teams/nfl/cleveland-browns/roster/2019',
        'https://www.footballdb.com/teams/nfl/dallas-cowboys/roster/2019',
        'https://www.footballdb.com/teams/nfl/denver-broncos/roster/2019',
        'https://www.footballdb.com/teams/nfl/detroit-lions/roster/2019',
        'https://www.footballdb.com/teams/nfl/green-bay-packers/roster/2019',
        'https://www.footballdb.com/teams/nfl/houston-texans/roster/2019',
        'https://www.footballdb.com/teams/nfl/indianapolis-colts/roster/2019',
        'https://www.footballdb.com/teams/nfl/jacksonville-jaguars/roster/2019',
        'https://www.footballdb.com/teams/nfl/kansas-city-chiefs/roster/2019',
        'https://www.footballdb.com/teams/nfl/oakland-raiders/roster/2019',
        'https://www.footballdb.com/teams/nfl/los-angeles-chargers/roster/2019',
        'https://www.footballdb.com/teams/nfl/los-angeles-rams/roster/2019',
        'https://www.footballdb.com/teams/nfl/miami-dolphins/roster/2019',
        'https://www.footballdb.com/teams/nfl/minnesota-vikings/roster/2019',
        'https://www.footballdb.com/teams/nfl/new-england-patriots/roster/2019',
        'https://www.footballdb.com/teams/nfl/new-orleans-saints/roster/2019',
        'https://www.footballdb.com/teams/nfl/new-york-giants/roster/2019',
        'https://www.footballdb.com/teams/nfl/new-york-jets/roster/2019',
        'https://www.footballdb.com/teams/nfl/philadelphia-eagles/roster/2019',
        'https://www.footballdb.com/teams/nfl/pittsburgh-steelers/roster/2019',
        'https://www.footballdb.com/teams/nfl/san-francisco-49ers/roster/2019',
        'https://www.footballdb.com/teams/nfl/seattle-seahawks/roster/2019',
        'https://www.footballdb.com/teams/nfl/tampa-bay-buccaneers/roster/2019',
        'https://www.footballdb.com/teams/nfl/tennessee-titans/roster/2019',
        'https://www.footballdb.com/teams/nfl/washington-redskins/roster/2019'
    ]

    def parse(self, response):
        for player in response.css('div.tr'):

            number = player.css('div.td.w10.m20.rostercell_num::text').get()
            name = player.css('div.td.w20.m80.rostercell_name').css('span.rostplayer').css('b').css('a::text').get()
            position = player.css('div.td.w10.rostercell_pos.hidden-xs::text').get()
            age = player.css('div.td.w10.rostercell_age.hidden-xs::text').get()
            college = player.css('div.td.w30.rostercell_coll.hidden-xs::text').get()
            team = response.url.split("/")[-3]
            
           
            next_page = player.css('div.td.w20.m80.rostercell_name').css('span.rostplayer').css('b').css('a::attr(href)').get()

            absolute_url = response.urljoin(next_page)

            request = Request(absolute_url, callback=self.fetch_stats, cb_kwargs={'number': number, 'name': name, 'position': position, 'age': age, 'college': college, 'team': team})
            yield request
  
            

    def fetch_stats(self, response, number, name, position, age, college, team):

        # GET DEFENSIVE STATS
        if (position == "DE" or position == "DT" or position == "LB" or position == "DB" or position == "OT" or position == "OG"):
            stats = response.css('div.divToggle_D_reg').css('tbody').css('tr')[-1].css('td')[3:].css('td::text').getall()
        
        # GET Punter STATS
        elif (position == "P"):
            stats = response.css('div.divToggle_U_reg').css('tbody').css('tr')[-1].css('td')[3:].css('td::text').getall()
            
        # GET Kicker STATS
        elif (position == "K"):
            stats = response.css('div.divToggle_K_reg').css('tbody').css('tr')[-1].css('td')[3:].css('td::text').getall()
            
        # GET Reciever STATS
        elif (position == "WR" or position == "TE"):
            stats = response.css('div.divToggle_C_reg').css('tbody').css('tr')[-1].css('td')[3:].css('td::text').getall()
            
        # GET Runner STATS
        elif (position == "RB"):
            stats = response.css('div.divToggle_R_reg').css('tbody').css('tr')[-1].css('td')[3:].css('td::text').getall()
            
        # GET QB STATS
        elif (position == "QB"):
            stats = response.css('div.divToggle_P_reg').css('tbody').css('tr')[-1].css('td')[3:].css('td::text').getall()
            
        # GET center STATS
        else :
            stats = response.css('div.divToggle_M_reg').css('tbody').css('tr')[-1].css('td')[3:].css('td::text').getall()
            
        
        yield {
            'number': number, 
            'name': name, 
            'position': position, 
            'age': age,
            'college': college,
            'team': team,
            'stats': stats
         }


