import csv
from dateutil.parser import parse
from dateutil.tz import gettz
from ics import Calendar, Event
from pytz import timezone
import sys

from bs4 import BeautifulSoup


def find_sessions(soup):
    "Parse HTML file and extract session info"
    sessions = soup.findAll('div', class_="xExpand")
    for session in sessions:
        date = session.find('div', {"class": "xDate"})
        title = session.find('div', {"class": "xTitle"})
        abstract = session.find('div', {"class": "xAbstract"})
        a = list(abstract.strings)
        yield {
            'date': parse(date.text, tzinfos={"MDT": -6 * 3600}),
            'title': title.text,
            'author': a[0].lstrip(':'),
            'abstract': "".join(a[1:])
        }


def main(args):
    with open(args[1], 'r') as f:
        soup = BeautifulSoup(f.read(), features="html.parser")
        # sessions = soup.findAll('div', {"class": "xExpand"})

        try:
            calendar = Calendar()
            with open('idv2020.csv', 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['date', 'title', 'author', 'abstract'])
                for session in find_sessions(soup):
                    e = Event()
                    e.name = session['title']
                    e.begin = session['date'].astimezone(timezone('US/Pacific'))  #.strftime("%Y%m%d %H:%M:%S")      # '20140101 00:00:00'
                    calendar.events.add(e)
                    csvwriter.writerow(session.values())
        finally:
            with open('idv2020.ics', 'w') as f1:
                f1.writelines(calendar)


if __name__ == "__main__":
    main(sys.argv)


# <div class="xDate"
# <div class="xTitle"
# <div class="xAbstract"
#    "Speaker: Richard Bird"
#    <br>
#    <br>
#    10 years ago no one was interested in the notion of “digital identity”. You had accounts and passwords and it was an irritating administrative function to manage all those accounts for customers, citizens, and humans in general. In the last two years the war for the hearts, minds, and wallets attached to a humans’ digital identity have set the stage for open warfare in 2020 and beyond by organizations and industries that see that value in being the creator and manager of a digital identity standard. What does it mean for the US and the world when champions for SSI and banks and payment processors and social media and governments and healthcare networks are all racing to create an operationally sustainable unique digital identity? Will there be tensions and challenges between these different actors when it comes time to recognize the credibility and authenticity of each other’s standards? Richard Bird regularly spends time across 5 continents working with governments and large companies, navigating the complexities of the rising interest and demand for true digital identities. He’ll share his observations in an effort to prepare you for the disruption this will create in our practices, designs and architectures for security, privacy and consumer and citizen rights.