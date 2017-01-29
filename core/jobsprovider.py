from datetime import datetime
import re
import urllib
from bs4 import BeautifulSoup as Soup
from core.models import Job
from django.core.exceptions import ObjectDoesNotExist


class JobsProvider(object):

    publisher = '3025890005972088'
    query = 'software+engineer'
    location = 'Minneapolis%2cMN'
    count = 500
    url = ''


    def buildUrl(self):
        urlparams = {
            "publisher": self.publisher,
            "q": self.query,
            "l": self.location,
            "jk": "fulltime",
            "limit": str(self.count),
            "latlong": "1",
            "userip": "1.2.3.4",
            "useragent": "Mozilla//4.0(Firefox",
            "v": "2"
        }
        return 'http://api.indeed.com/ads/apisearch?' + urllib.urlencode(urlparams)


    def getJobs(self):
        pagesize = 25
        page_count = self.count / pagesize
        self.url = self.buildUrl()
        print "url: " + self.url

        for page in range(0, page_count):
            nextpageurl = self.url + '&start=' + str(page * pagesize)
            print nextpageurl
            rawdata = Soup(urllib.urlopen(nextpageurl), "lxml")

            for i in range(0, pagesize):
                print "getting next job: " + str(datetime.now())
                result = rawdata.results.contents[i]
                jobtitle = result.find({'jobtitle'}).getText()
                company = result.find({'company'}).getText()
                location = result.find({'formattedlocation'}).getText()
                # city = result.find({'city'}).getText()
                # state = result.find({'state'}).getText()
                date_text = result.find({'date'}).getText()
                date_posted = datetime.strptime(date_text, '%a, %d %b %Y %H:%M:%S %Z')
                # snippet = result.find({'snippet'}).getText()
                joburl = result.find({'url'}).getText()

                try:
                    j_exist = Job.objects.get(date_posted=date_posted, \
                                              company=company, \
                                              title=jobtitle)
                except ObjectDoesNotExist:
                    # access url and grab full job description
                    wordsoup = Soup(urllib.urlopen(joburl), "lxml")
                    description = wordsoup.find('span', attrs={'id':'job_summary'})\
                                          .getText().strip()
                    sponsored = result.find({'sponsored'}).getText().title()
                    expired = result.find({'expired'}).getText().title()

                    j = Job(date_posted=date_posted,
                            query=self.query,
                            company=company,
                            location=location,
                            title=jobtitle,
                            description=description,
                            url=joburl,
                            sponsored=sponsored,
                            expired=expired)
                    j.save()
