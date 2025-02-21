from crawlers.site1_crawler import ZingMP3Crawler
import json
from crawlers.site2_crawler import ZingNewsCrawler

if __name__ == '__main__':
    print("Crawling from Zing MP3")
    url = "https://zingmp3.vn/moi-phat-hanh"
    crawler = ZingMP3Crawler(url)
    crawler.run()
    
    print("Crawling from ZNEWS")
    url = "https://znews.vn/cong-nghe.html"
    crawler = ZingNewsCrawler(url)
    crawler.run()