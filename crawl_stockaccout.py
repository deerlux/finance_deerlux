#!/usr/bin/env python2
import datetime, os

if __name__ == '__main__':
    repo_dir = os.environ['OPENSHIFT_REPO_DIR']
    
    start_date = datetime.date.today()
    end_date = datetime.date(2015, 4, 20)

    os.chdir(os.path.join(repo_dir, 'financecrawl'))
    
    curr_date = start_date

    while curr_date > end_date:
        dateStr = curr_date.strftime('%Y.%m.%d')
        os.system('scrapy crawl stockaccount -a date_in=' + dateStr)
        curr_date -= datetime.timedelta(7) 
        print 'scrapyed: %s' % dateStr


