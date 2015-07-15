# -*- coding: utf-8 -*-

import urllib2
from sgmllib import SGMLParser

class GameList(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_tr = False
        self.is_td = False
        self.tr_list = []
        self.td_list = []

    def start_td(self, attrs):
        self.is_td = True

    def end_td(self):
        self.is_td = False

    def handle_data(self, text):
        if self.is_td:
            print text
            self.td_list.append(text)




class CSLSCHEDULE(object):
    base_url = "http://csldata.sports.sohu.com/zsc.php?season={season}&type=R&round={round}"

    def get_page(self, season, round):
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers    = {'User-Agent' : user_agent}
        req = urllib2.Request(
                CSLSCHEDULE.base_url.format(season=season, round=round),
                headers= headers
            )
        try:
            page = urllib2.urlopen(req).read()
        except:
            page = None

        return page.decode('utf-8')

    def get_time(self, page):
        time_pattern = """<td class="w96">(.*?)</td>.*?<td>(.*?)</td>"""
        times = re.findall(time_pattern, page, re.S)

        print times 

    def get_teams(self, page):
        team_pattern = """<a href="team.php\?teamid.*?>(.*?)</a>"""
        teams = re.findall(team_pattern, page, re.S)

        for team in teams:
            print team.encode('utf-8')

    def get_bifen(self, page):
        bifen_pattern = """<td class="f_green">\s*?<*?.*?>*?(.*?-.*?)<*?.*?>*?\s*?</td>"""
        bifens = re.findall(bifen_pattern, page, re.S)
        for bf in bifens:
            print bf 

    def get_any(self, page):
        pattern = """<td class="w96">(.*?)</td>.*?<td>(.*?)
            </td>.*?<td.*?><a.*?>(.*?)</a></td>.*?<td.*?>
            .*?<*?.*?>*?(.*?)<*?.*?>*?</td>.*?<td.*?>(.*?)</a></td>"""
        things = re.findall(pattern, page, re.S)
        print things


if __name__ == "__main__":
    csl_sch = CSLSCHEDULE()
    page = csl_sch.get_page(2015, 18)

    gamelist = GameList()
    gamelist.feed(page)
    print gamelist.td_list

    # csl_sch.get_time(page)
    # csl_sch.get_teams(page)
    # csl_sch.get_bifen(page)

