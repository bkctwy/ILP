import re
import time
from db import DB
from bs4 import BeautifulSoup
from utils.utils import string_to_md5
from scraper.base_scraper import BaseScraper


class FalooScraper(BaseScraper):
    def __init__(
        self, book_id: int = None, alias: str = None, cookies: str = None
    ) -> None:
        super().__init__(book_id, alias, cookies)
        self.base_url = "https://b.faloo.com"
        self.index_url = f"https://b.faloo.com/{self.id}.html"
        self.index_page_text = self.get_index_page()

    def get_title(self):
        super().get_title()
        if self.title is None:
            title_soup = BeautifulSoup(self.index_page_text, "html.parser")
            self.title = title_soup.find("h1").text
            return self.title
        else:
            return self.title

    def get_index(self, export_path: str = None, export_type: str = None) -> list:
        super().get_index()
        if self.db.is_table_empty(self.title):
            index_soup = BeautifulSoup(self.index_page_text, "html.parser")
            chapter_list = index_soup.find_all("div", class_="DivTd3")
            for chapter in chapter_list:
                chapter_title = chapter.text.strip()
                chapter_url = "https:" + chapter.find("a")["href"]
                chapter_id = chapter_url.split("/")[-1].split(".")[0]
                chapter_md5_id = string_to_md5(chapter_id)
                self.db.insert_data(
                    self.title,
                    chapter_md5_id,
                    chapter_id,
                    chapter_title,
                    chapter_url,
                    None,
                )
                self.index_chapter_list.append(
                    {
                        "md5_id": chapter_md5_id,
                        "id": chapter_id,
                        "title": chapter_title,
                        "url": chapter_url,
                        "sum": None,
                    }
                )
        elif self.db.is_table_empty(self.title) is None:
            return []
        elif not self.db.is_table_empty(self.title):
            all_data = self.db.get_all_data(self.title)
            for data in all_data:
                chapter_md5_id = data[self.chapter_md5_id_slice][0]
                chapter_title = data[self.chapter_title_slice][0]
                chapter_url = data[self.chapter_url_slice][0]
                chapter_sum = data[self.chapter_sum_slice][0]
                chapter_id = data[self.chapter_id_slice][0]
                self.index_chapter_list.append(
                    {
                        "md5_id": chapter_md5_id,
                        "id": chapter_id,
                        "title": chapter_title,
                        "url": chapter_url,
                        "sum": chapter_sum,
                    }
                )
        if export_path is not None and export_type is not None:
            self.db.export_data(self.title, export_path, export_type)
        return self.index_chapter_list

    def get_author(self) -> str:
        super().get_author()
        soup = BeautifulSoup(self.index_page_text, "html.parser")
        self.author = soup.find("div", class_="zi1").find("a")["title"]
        print(self.author)
        return self.author

    def parse_chapter(
        self, chapter_response: str, chapter_title: str, index: int
    ) -> None:
        db = DB(self.DB_PATH)

        chapter_soup = BeautifulSoup(chapter_response, "html.parser")
        chapter_original = chapter_soup.find("div", class_="noveContent")
        for b_tag in chapter_original.find_all("b"):
            b_tag.decompose()
        chapter_main = chapter_original.text
        chapter_main = re.sub(
            r"\(活动时间：10月1日到10月7日\)", "", chapter_main
        ).strip()
        chapter_head = chapter_title + "\n---\n\n"
        chapter_sum = len(chapter_main)
        chapter_md5 = string_to_md5(self.index_chapter_list[index]["id"])
        self.save_novel(self.title, chapter_head + chapter_main, chapter_title)
        self.logger.info(f"下载完成：{self.title}:{chapter_title}")

        db.update_data(self.title, "chapter_sum", chapter_sum, "md5_id", chapter_md5)

        del db

    async def fetch_chapter(self, index: int) -> dict:
        if await super().fetch_chapter(index):
            return {"status": "downloaded"}

        response = await self.async_get(
            url=f"{self.index_chapter_list[index]["url"]}",
            headers=self.HEADERS,
            cookies=self.cookies,
            encoding="gb18030",
        )

        chapter_response = response
        time.sleep(self.SLEEP_TIME)
        return {
            "status": "success",
            "chapter_response": chapter_response,
            "index": index,
            "chapter_title": self.index_chapter_list[index]["title"],
        }
