from Scraper.scraper import Headers
from datetime import datetime
import sqlite3, sys, schedule


class DataCollector:
    def __init__(self, company):
        self.company = company

    def process(self):
        print("Getting titles at ", datetime.now())
        hd = Headers(self.company)
        hd.update_headers()
        titles = hd.get_titles()
        self.save_titles(titles)

    def save_titles(self, titles):
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        connect = sqlite3.connect("headers.db")
        c = connect.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS headers (company text, date text, header text unique)''')

        for title in titles:
            c.execute('''INSERT OR IGNORE INTO headers VALUES (?,?,?)''', (self.company, dt_string, title))

        connect.commit()
        connect.close()


if __name__ ==  "__main__":
    dc = DataCollector("CD projekt RED")
    schedule.every(10).minutes.do(dc.process)
    while True:
        try:
            schedule.run_pending()
        except Exception:
            print("Error: ", sys.exc_info()[0])
