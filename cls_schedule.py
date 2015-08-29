# -*- coding: utf-8 -*-

import re
import urllib2
import alfred
from bs4 import BeautifulSoup

class CSLSCHEDULE(object):
    base_url = "http://csldata.sports.sohu.com/zsc.php"
    # ?season={season}&type=R&round={round}

    def get_page(self, season, round):
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers    = {'User-Agent' : user_agent}
        req = urllib2.Request(
                CSLSCHEDULE.base_url,
                headers= headers
            )
        page = urllib2.urlopen(req).read()

        return page

    def get_table_line(self, page):
        soup = BeautifulSoup(page)
        return soup.find_all('tr', class_=re.compile("even|odd"))

    def get_game_time(self, page):
        soup = BeautifulSoup(page)
        day  = soup.find('td', class_="w96")
        time = soup.find('td', attrs=None)
        return day.string + ' ' + time.string 

    def get_game_result(self, page):
        soup = BeautifulSoup(page)
        res = soup.find_all('td', class_="f_green")
        zhudui = BeautifulSoup(str(res[0])).find('a').string
        kedui  = BeautifulSoup(str(res[2])).find('a').string
        befin  = BeautifulSoup(str(res[1])).find('a')
        if not befin:
            befin = " - "
        else:
            befin = befin.string

        return zhudui + befin + kedui

if __name__ == "__main__":
    csl_sch = CSLSCHEDULE()
    page = csl_sch.get_page(2015, 19)
    lines = csl_sch.get_table_line(page)

    len_lines = len(lines)
    result = []

    for i in range(len_lines):
        result.append(alfred.Item( {"uid": alfred.uid(i)}, 
                csl_sch.get_game_result(str(lines[i])), 
                csl_sch.get_game_time(str(lines[i])), 
                None
                )
            )

    alfred.write(alfred.xml(result))


