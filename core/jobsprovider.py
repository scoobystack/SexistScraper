from datetime import datetime
import re
import urllib
from bs4 import BeautifulSoup as Soup
from core.models import Job

class JobsProvider(object):

    publisher = '3025890005972088'
    query = 'software+engineer'
    location = 'Minneapolis%2cMN'
    count = 500

    url = 'http://api.indeed.com/ads/apisearch?publisher=' + publisher + '&q=' + query + \
          '&l=' + location + '&jt=fulltime&limit=' + str(count) + \
          '&latlong=1&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2'

    def getJobs(self):

        pagesize = 25
        page_count = self.count / pagesize
        jobs_all = list(Job.objects.all())

        for page in range(0, page_count):

            nextpageurl = self.url + '&start=' + str(page * pagesize)
            rawdata = Soup(urllib.urlopen(nextpageurl), "lxml")

            for i in range(0, pagesize):
                result = rawdata.results.contents[i]
                jobtitle = result.find({'jobtitle'}).getText()
                company = result.find({'company'}).getText()
                location = result.find({'formattedlocation'}).getText()
                # city = result.find({'city'}).getText()
                # state = result.find({'state'}).getText()
                date = result.find({'date'}).getText()
                # snippet = result.find({'snippet'}).getText()
                joburl = result.find({'url'}).getText()

                # access url and grab full job description
                wordsoup = Soup(urllib.urlopen(joburl), "lxml")
                description = wordsoup.find('span', attrs={'id':'job_summary'}).getText().strip()
                sponsored = result.find({'sponsored'}).getText().title()
                expired = result.find({'expired'}).getText().title()
                uniqueid = company[0:2]+location[0:2]+date[8:10]+date[5:7]+joburl[37:42]

                j = Job(
                    date_posted=datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z'),
                    keywords=self.query,
                    company=company,
                    location=location,
                    title=jobtitle,
                    description=description,
                    url=joburl,
                    sponsored=sponsored,
                    expired=expired
                )

                '''
                    We can likely make some assumptions regarding query and date posted to improve
                    performance here. I'm thinking we...
                        1) determine the latest date_posted value for jobs in the database
                           based on the query
                        2) assume we have all job descriptions prior to the date posted found in
                           (1). This only works if we then search by date posted rather than
                           relevancy, but searching by relevancy is more likely to find results
                           a user would find if they were doing a job search. Does this matter? Do
                           we care if a job description is more relevant, or are we just more
                           interested in parsing the content of the description. It seems we can
                           assume that if we scrape 1000+ job descriptions for a given query the
                           relevancy becomes insignificant...And we can determine a larger trend
                           from the aggregated descriptions
                        3) jobs found from the search with the same date posted found in (1) need
                           to be validated to see if they are a duplicate (could have been created
                           after our search on the given day)
                        4) we can assume any jobs with a newer date posted are new jobs and persist
                           without validating uniqueness
                '''
                # j_exist_set = jobs_all.filter(date_posted=j.date_posted, company=j.company, \
                #               title=j.title)

                j_exist_set = [job for job in jobs_all if \
                               job.date_posted == j.date_posted and \
                               job.company == j.company and \
                               job.title == j.title]

                if len(j_exist_set) == 0:
                    j.save()
