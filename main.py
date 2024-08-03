from bs4 import BeautifulSoup
import requests
import logging

def extract_manga_details(query):
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()

    url = f"https://manganato.com/search/story/{query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    manga_list = []
    
    search_items = soup.find_all("div", class_="search-story-item")
    
    for item in search_items:
        # Extract thumbnail
        thumbnail = item.find("img", class_="img-loading")["src"]
        
        # Extract name
        name = item.find("a", class_="a-h text-nowrap item-title").get("title")
        
        # Extract rating
        rating = item.find("em", class_="item-rate").text.strip()
        
        # Extract total chapters
        chapter_links = item.find_all("a", class_="item-chapter")
        if chapter_links:
            last_chapter = chapter_links[0].get("title")
            total_chapters = last_chapter.split(" ")[-1]
        else:
            total_chapters = "N/A"
        
        # Extract last update
        last_update = item.find("span", class_="text-nowrap item-time").text.strip()
        
        manga_details = {
            "thumbnail": thumbnail,
            "name": name,
            "rating": rating,
            "total_chapters": total_chapters,
            "last_update": last_update
        }
        
        manga_list.append(manga_details)
        
        # Log the details
        logger.info(manga_details)
    
    return manga_list

# Example usage
query = "bleach"
manga_details = extract_manga_details(query)
