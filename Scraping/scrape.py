import requests
from bs4 import BeautifulSoup

url = 'https://www.booking.com/hotel/am/el-house-yerevan.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaAeIAQGYATG4ARfIAQzYAQHoAQH4AQKIAgGoAgO4Ar-qxLEGwAIB0gIkNjlkZjgwNzctMGFhMi00NTFhLThiNmEtOTgyMTMyZTJkNmI52AIF4AIB&sid=a0024d7247d1bd4da91c7daa61d0ae46&dest_id=-2325645;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;hpos=1;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1714492793;srpvid=d2d370794d4601d3;type=total;ucfs=1&#hotelTmpl'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text(separator=' ', strip=True)

    with open('page_content.txt', 'w', encoding='utf-8') as file:
        file.write(page_text)

    print("Content saved to page_content.txt")

except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")