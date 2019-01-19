import os
import requests
from datetime import datetime
import re

from sqlalchemy import *
from sqlalchemy.exc import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


class CvilleDataScraper:

    wait_s = 30

    def __init__(self, dbfile='cvilledata.db', dumpdir='./data'):
        self.driver = webdriver.Firefox()
        self.db = create_engine('sqlite:///{}'.format(dbfile))
        self.dumpdir = dumpdir
        if not os.path.exists(self.dumpdir):
            os.makedirs(self.dumpdir)
        self.page_table = None
        self.file_table = None
        self.metadata = MetaData(self.db)

    def __del__(self):
        self.driver.quit()

    def setup_db(self):
        c1 = Column('page_id', Integer, primary_key=True)
        c2 = Column('title', String(80))
        c3 = Column('url', String(256))
        c4 = Column('parent_page_id', Integer)
        c5 = Column('license', String(256))
        c6 = Column('updated', Date)
        c7 = Column('type', String(80))
        c8 = Column('rows', Integer)
        c9 = Column('description', Text)
        tables = {
            'page': Table('page', self.metadata, c1, c2, c3, c5, c6, c7, c8, c9),
            'file': Table('file', self.metadata, c4, c2.copy(), c3.copy())
        }
        for tbl in tables:
            try:
                tables[tbl].create()
                print("Created table `{}`.".format(tbl))
            except OperationalError:
                print("Table `{}` already created.".format(tbl))

    def get_data_pages(self):
        page_table = Table('page', self.metadata, autoload=True)
        ins = page_table.insert()
        page_id = 0
        n = 1
        while n:
            print("Loading data page", n)
            url = 'http://opendata.charlottesville.org/datasets?page=' + str(n)
            self.driver.get(url)
            _ = wait(self.driver, self.wait_s).until(EC.presence_of_element_located((By.XPATH, "//a")))
            links = self.driver.find_elements_by_css_selector('.result-name.ember-view')
            for link in links:
                page_id += 1
                try:
                    ins.execute(page_id=page_id, title=link.text, url=link.get_attribute('href'))
                except IntegrityError:
                    print("Data for page_id", page_id, "already in database.")
            try:
                _ = self.driver.find_element_by_xpath("//a[@aria-label='Next']")
                n += 1
            except NoSuchElementException:
                print("Done")
                n = None

    def get_data_links(self, start_page_id=0):

        page_table = Table('page', self.metadata, autoload=True)
        s = page_table.select().where(page_table.c.page_id > start_page_id)
        rs = s.execute()
        rows = [row for row in rs]
        rs.close()

        file_table = Table('file', self.metadata, autoload=True)
        ins = file_table.insert()

        for row in rows:
            page_id = row['page_id']
            title = row['title']
            href = row['url']
            print(page_id, 'Getting', title)
            self.driver.get(href)
            try:
                _ = wait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#download-button")))
            except TimeoutException as e:
                print('Page {} as {} taking too long.'.format(title, href))
                continue
            try:
                data_license = self.driver.find_element_by_xpath("//div[@class='metatags']/span[@class='license']/span/a").get_attribute('href')
            except NoSuchElementException:
                data_license = 'None'
            data_updated = self.driver.find_element_by_xpath("//div[@class='metatags']/span[@class='updated']").text
            m, d, y = map(int, data_updated.split('/'))
            data_updated = datetime(y, m, d)
            data_type = self.driver.find_element_by_xpath("//div[@class='metatags']/span[@class='type']").text
            data_rows = self.driver.find_element_by_xpath("//div[@class='metatags']/span[@class='rows']").text
            data_rows = int(re.sub(r'\D+','', data_rows))
            data_desc = self.driver.find_element_by_xpath("//div[@id='dataset-description']").text

            upd = page_table.update().where(page_table.c.page_id==page_id).values(license=data_license,
                updated=data_updated, type=data_type, rows=data_rows, description=data_desc)
            upd.execute()

            for data_link in self.driver.find_elements_by_xpath('//a[@download]'):
                link_text = data_link.get_attribute('download')
                link_url = data_link.get_attribute('href')
                print(link_text, link_url)
                try:
                    ins.execute(parent_page_id=page_id, title=link_text, url=link_url)
                except IntegrityError:
                    print("Data for link", link_text, "already in database.")

    def get_data(self):
        file_table = Table('file', self.metadata, autoload=True)
        for row in file_table.select().execute():
            file_name = row[1]
            file_name = re.sub(r'[^A-Za-z0-9.]+', '_', file_name)
            file_url = row[2]
            print("Getting", file_name)
            cmd = "curl {} -o {}/{}".format(file_url, self.dumpdir, file_name)
            os.system(cmd)


if __name__ == '__main__':

    from . import CvilleDataScraper as CDS

    scraper = CDS()
    #scraper.setup_db()
    #scraper.get_data_pages()
    #scraper.get_data_links(start_page_id=37)
    #scraper.get_data()