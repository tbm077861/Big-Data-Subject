import os
import sys
from bs4 import BeautifulSoup
from .base_crawler import BaseCrawler
from database import CSVHandler, TXTHandler, MongoHandler
from utils import setup_logger, clean_text

# Thiết lập logger
logger = setup_logger('site2_crawler', 'site2_crawler.log')

class ZingNewsCrawler(BaseCrawler):
    def __init__(self, base_url):
        super().__init__(base_url)

    def parse_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all('article', class_='article-item')
        news_list = []

        for article in articles:
            title_tag = article.find('p', class_='article-title')
            meta_tag = article.find('p', class_='article-meta')
            summary_tag = article.find('p', class_='article-summary')
            thumbnail_tag = article.find('p', class_='article-thumbnail')

            title = title_tag.a.text.strip() if title_tag and title_tag.a else None
            url = title_tag.a['href'] if title_tag and title_tag.a else None
            summary = summary_tag.text.strip() if summary_tag else None
            image_url = (
                thumbnail_tag.img.get('data-src') or thumbnail_tag.img.get('src')
                if thumbnail_tag and thumbnail_tag.img else None
            )

            publish_time_tag = meta_tag.find('span', class_='friendly-time') if meta_tag else None
            publish_time = publish_time_tag.text.strip() if publish_time_tag else None

            category_tag = meta_tag.find('span', class_='category') if meta_tag else None
            category = category_tag.text.strip() if category_tag else None

            news_list.append({
                'title': title,
                'url': url,
                'summary': summary,
                'image_url': image_url,
                'publish_time': publish_time,
                'category': category
            })

        return news_list

    def run(self):
        html = self.fetch_page()
        if html:
            results = self.parse_page(html)
            if results:
                self.save_to_csv(results, "data/csv/Tin_tuc_ZingNews.csv")
                self.save_to_txt(results, "data/txt/Tin_tuc_ZingNews.txt")
                self.save_to_mongo(results, db_name="Tin_tuc_ZingNews", collection_name="tinTuc")
            else:
                logger.error("Không tìm thấy bài hát nào!")
        
# Chạy crawler cho danh sách bài hát trên ZingMP3
if __name__ == "__main__":
    base_url = "https://znews.vn/cong-nghe.html"
    crawler = ZingNewsCrawler(base_url)
    crawler.run()