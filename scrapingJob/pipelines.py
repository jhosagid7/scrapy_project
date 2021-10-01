# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class ScrapingjobPipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('jobScrapy.db')
        self.c = self.connection.cursor()
        #query
        try:
            self.c.execute("""
                CREATE TABLE indeeds (
                    Searched_job TEXT,
                    Job_title TEXT,
                    Location TEXT,
                    Company_name TEXT,
                    Post_date TEXT,
                    Extract_date TEXT,
                    Job_description TEXT,
                    Salary TEXT,
                    Apply_to TEXT
                )
            """)
            self.connection.commit()
        except sqlite3.OperationalError:
            pass 
    

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute("""
            INSERT INTO indeeds (Searched_job,Job_title,Location,Company_name,Post_date,Extract_date,Job_description,Salary,job_title,Apply_to) VALUES(?,?,?,?,?,?,?,?,?,?)
        """, (
            item.get('Searched_job'),
            item.get('Job_title'),
            item.get('Location'),
            item.get('Company_name'),
            item.get('Post_date'),
            item.get('Extract_date'),
            item.get('Job_description'),
            item.get('Salary'),
            item.get('job_title'),
            item.get('Apply_to'),
        ))
        self.connection.commit()
        return item
