import scrapy
import re
from datetime import datetime, timedelta




class GetonboardSpider(scrapy.Spider):
    name = 'getonboard'
    allowed_domains = ['www.getonbrd.com','getonbrd.com']
    

    def start_requests(self):
        yield scrapy.Request(f'https://www.getonbrd.com/jobs-{self.job}')
         

    def parse(self, response):
        # We extract the main container.
        # //table[contains(@class,"jobCard_mainContent")]/tbody/tr/td/div[2]/pre/div[1]
        
        link_cont_elemts  = response.xpath('//ul[@class="gb-results-list"]/div/a')
        print('link_cont_elemts',link_cont_elemts)

        for lc_elemts in link_cont_elemts:
            link            = lc_elemts.xpath('.//@href').get()
            print(link)
            extract_date    = datetime.today().strftime('%Y-%m-%d')
            
            
            searched_job        = self.job

            # if salary_tag:
            #     salary      = salary_tag
            # else:
            #     salary      = ''  

            
            # if company_name:
            #     company_name      = company_name
            # else:
            #     company_name    = lc_elemts.xpath('.//span[contains(@class, "companyName")]/a/text()').get()

            if link is not None:
                
                # Relative link
                yield response.follow(url=link, callback=self.parse_applyto, meta={'extract_date':extract_date,'link':link,'searched_job':searched_job})

        
        next_page_url = response.xpath('//*[contains(@aria-label, "Next")]/@href').get()
        

        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse)

    def parse_applyto(self, response):
        #Data extracted from the main page
        extract_date    = response.request.meta['extract_date']
        searched_job          = response.request.meta['searched_job']
        link          = response.request.meta['link']
        
        
        rows = response.xpath('//div[@class="full-width"]')
        rows_kills = response.xpath('//div[@id="job-body"]')
        tag_kills = response.xpath('//div[@id="js-apply-section"]')

        if rows:
            Apply_to      = link
            company_name = rows.xpath('//strong[@itemprop="name"]/text()').get()
            location = rows.xpath('.//h3[@class="size1"]/strong/text()').get()
            job_title = rows.xpath('.//span[@itemprop="title"]/text()').get()
            post_date = rows.xpath('.//div[@class="semi-opaque-white"]/time/text()').get()
            salary = rows.xpath('.//span[@class="tooltipster-basic"]/strong/text()').get()
            
        
            
            if salary is None:
                salary = 'Not supplied'
            
            
            if post_date is None:
                post_date = rows.xpath('//div[@class="dark-gray"]/time/text()').get()
            
            if location is None  or location == '':
                location        = rows.xpath('.//h2//span[@class="tooltipster"]//span/text()').get()
            
                if location is None:
                    location        = rows.xpath('.//h2//span[@class="tooltipster"]/text()[2]').get()
                    
            print(location)
            
        if rows_kills:
            job_description = rows_kills.xpath('.//div[@class="gb-container gb-container--medium"]/div[@class="mb4"][3]/div[@class="gb-rich-txt"]/ul/li/text()').getall()
            
            if job_description is None:
                job_description = rows_kills.xpath('.//div[@class="gb-container gb-container--medium"]/div[@class="mb4"][3]/div[@class="gb-rich-txt"]/p/text()').getall()
                
            if job_description is None:
                location        = rows.xpath('.//div[@class="gb-container gb-container--medium"]/div[@class="mb4"][3]/div[@class="gb-rich-txt"]/div/text()').get()
                
            if job_description is None:
                location        = rows.xpath('.//div[@class="gb-container gb-container--medium"]/div[@class="mb4"][3]/div[@class="gb-rich-txt"]/ul/li/strong/text()').get()
                
            job_description = " ".join(job_description)
            
            
        if tag_kills:
            tags = tag_kills.xpath('.//div[@itemprop="skills"]/a/text()').getall()
            _tag = []
            for tag in tags:
                _tag.append(tag.strip().lower())
            print('_tag ',_tag)
                
        else:
            _tag = []
            
        print('job_description ',job_description)
                
        

        # Data extracted from the link apply to company, to obtain the link apply to
         
        # job_title = response.xpath('.//h1/text()').get().replace(u"\u00a0", " ")
        
        if location is not None:

            yield {
            'Searched_job': searched_job,
            'Job_title': job_title.strip(),
            'Location': location.replace(u"\xa0", "").replace(u"\n", " ").strip('\t').strip(),
            'Company_name': company_name.strip(),
            'Post_date': post_date.strip(),
            'Extract_date': extract_date,
            'Job_description': job_description,
            'Salary': salary.replace(u"\n", " ").strip('\t').strip(),
            'Tags': _tag,
            'Apply_to': Apply_to,
            }


