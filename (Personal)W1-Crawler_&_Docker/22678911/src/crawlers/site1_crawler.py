import os
import sys
import json
from bs4 import BeautifulSoup
from .base_crawler import BaseCrawler
from database import CSVHandler, TXTHandler, MongoHandler
from utils import setup_logger, clean_text

# Thiết lập logger
logger = setup_logger('site1_crawler', 'site1_crawler.log')

class ZingMP3Crawler(BaseCrawler):
    def __init__(self, url):
        super().__init__(url)


    def parse_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        
        # Tìm tất cả các script chứa JSON-LD
        scripts = soup.find_all('script', type='application/ld+json')
        
        for script in scripts:
            try:
                data = json.loads(script.string)
                
                # Kiểm tra nếu script chứa dữ liệu bài hát
                if data.get('@type') == 'MusicPlaylist':
                    song_list = []
                    for song in data['track']['itemListElement']:
                        song_info = {
                            'position': song['position'],
                            'name': song['item']['name'],
                            'artist': song['item']['byArtist'][0]['name'] if 'byArtist' in song['item'] else 'Unknown',
                            'url': song['url']
                        }
                        song_list.append(song_info)
                    return song_list
            except json.JSONDecodeError:
                continue
        
        return []  # Trả về danh sách rỗng nếu không tìm thấy dữ liệu

    def run(self):
        html = self.fetch_page()
        if html:
            song_list = self.parse_page(html)
            if song_list:
                self.save_to_csv(song_list, "data/csv/BXHSongs_MP3.csv")
                self.save_to_txt(song_list, "data/txt/BXHSongs_MP3.txt")
                self.save_to_mongo(song_list, db_name="Songs_ZingMP3", collection_name="dsSongs")
            else:
                logger.error("Không tìm thấy sản phẩm nào!")

# Chạy crawler cho danh mục điện thoại trên FPT Shop
if __name__ == "__main__":
    url = "https://zingmp3.vn/moi-phat-hanh"
    crawler = ZingMP3Crawler(url)
    crawler.run()
