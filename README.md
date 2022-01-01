# ScrapingJob

You need to have Pipenv, Python 3.8 installed.

1. Get into the virtual environment `pipenv shell`
2. Install packages `pipenv install`
3. Test scraper with:
```
indeed = scrapy crawl indeed -a job=react -a loc=remote
indeed = scrapy crawl indeed -a job=react -a loc=New%20York%2C%20NY

getonboard = scrapy crawl getonboard -a job="Web Programer"
```

Test scraper remote with:
```
curl -u d62b44e4e9934393b54c679b5fcb001b: https://app.scrapinghub.com/api/run.json -d project=570286 -d spider=indeed -d job=javascript -d loc=remote

f'https://www.refreshmiami.com/jobs/?search_keywords={self.job}'

name = 'refreshmiami'
    allowed_domains = ['www.refreshmiami.com','refreshmiami.com']

     link            = lc_elemts.xpath('.//@href').get()
            # print(link)
            extract_date    = datetime.today().strftime('%Y-%m-%d')
            job_title = lc_elemts.xpath('.//div[@class="position"]/h3/text()').get()
            print('job title:',job_title)
            
            searched_job        = self.job
```
