import scrapy
from datetime import datetime



class IndeedSpider(scrapy.Spider):
    name = 'indeed'
    allowed_domains = ['www.indeed.com','indeed.com', 'us.conv.indeed.com']
    

    def start_requests(self):
        yield scrapy.Request(f'https://www.indeed.com/jobs?q={self.job}&l={self.loc}')
         

    def parse(self, response):
        # We extract the main container.
        link_cont_elemts  = response.xpath('//td/div[4]/div[1]/a')

        for lc_elemts in link_cont_elemts:
            link            = lc_elemts.xpath('.//@href').get()
            extract_date    = datetime.today().strftime('%Y-%m-%d')
            location        = lc_elemts.xpath('.//div[contains(@class, "companyLocation")]/span/text()').get()
            company_name    = lc_elemts.xpath('.//span[contains(@class, "companyName")]/text()').get()
            salary_tag      = lc_elemts.xpath('.//table[1]/tbody/tr/td/div[3]/div/span/text()').get()
            post_date       = lc_elemts.xpath('.//table[2]/tbody/tr[2]/td/div[1]/span[1]/text()').get()
            job_description = lc_elemts.xpath('.//table[2]/tbody/tr[2]/td/div[1]/div/ul/li/text()').get()
            searched_job        = self.job

            if salary_tag:
                salary      = salary_tag
            else:
                salary      = ''  

            
            if company_name:
                company_name      = company_name
            else:
                company_name    = lc_elemts.xpath('.//span[contains(@class, "companyName")]/a/text()').get()

            if link is not None:
                
                # Relative link
                yield response.follow(url=link, callback=self.parse_applyto, meta={'extract_date':extract_date,'location':location,'company_name':company_name,'post_date':post_date,'job_description':job_description,'salary':salary,'searched_job':searched_job})

        
        next_page_url = response.xpath('//*[contains(@aria-label, "Next")]/@href').get()

        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse)

    def parse_applyto(self, response):
        #Data extracted from the main page
        extract_date    = response.request.meta['extract_date']
        location        = response.request.meta['location']
        company_name    = response.request.meta['company_name']
        post_date       = response.request.meta['post_date']
        job_description = response.request.meta['job_description']
        salary          = response.request.meta['salary']
        searched_job          = response.request.meta['searched_job']

        rows = response.xpath('//div[@id="applyButtonLinkContainer"]/div/div[2]/a')

        # Data extracted from the link apply to company, to obtain the link apply to
        Apply_to = rows.xpath('.//@href').get()
        job_title = response.xpath('.//h1/text()').get().replace(u"\u00a0", " ")

        yield {
        'Searched_job': searched_job,
        'Job_title': job_title,
        'Location': location,
        'Company_name': company_name,
        'Post_date': post_date,
        'Extract_date': extract_date,
        'Job_description': job_description,
        'Salary': salary,
        'Apply_to': Apply_to,
        }


