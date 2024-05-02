import requests
from bs4 import BeautifulSoup
import re

def scrape_webpage(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text(separator=' ', strip=True)
        return page_text
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_information(text):
    hotel_name = re.search(r"^(.*?Hotel), Yerevan", text)
    if not hotel_name:
        hotel_name = re.search(r"^(.*?) – Updated", text)
    hotel_name = hotel_name.group(1) if hotel_name else "Hotel name not found"

    address_match = re.search(r"(\d+/\d+ [^–]+ street, \d+ Yerevan, Armenia)", text)
    hotel_address = address_match.group(1) if address_match else "Address not found"

    description_match = re.search(r"Description:?\s*(.*?)\s*(?:Room|Facilities|House rules)", text, re.S)
    description = description_match.group(1).strip() if description_match else "Description not found"

    reviews = re.findall(r'“([^”]+)”', text)

    categories_scores = re.findall(r"(\w+) (\d+\.\d)", text)

    facilities_match = re.search(r"Facilities\s*([^House rules]+)", text, re.S)
    facilities = facilities_match.group(1).strip() if facilities_match else "Facilities not listed"

    house_rules_match = re.search(r"House Rules\s*(.*?)\s*(?:Check-in|Cancellations)", text, re.S)
    house_rules = house_rules_match.group(1).strip() if house_rules_match else "House rules not listed"

    return {
        "Hotel Name": hotel_name,
        "Hotel Address": hotel_address,
        "Description": description,
        "Guest Reviews": " ".join(reviews),
        "Categories Scores": dict(categories_scores),
        "Facilities": facilities,
        "House Rules": house_rules
    }


def save_to_markdown(info, filename):
    markdown_content = f"""
## Hotel Name: {info['Hotel Name']}
### Address: {info['Hotel Address']}
### Description
{info['Description']}

### Guest Reviews
{info['Guest Reviews']}

### Categories Scores
{', '.join([f'{k}: {v}' for k, v in info['Categories Scores'].items()])}

### Facilities
{info['Facilities']}

### House Rules
{info['House Rules']}
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(markdown_content)
    print(f"Data has been saved to {filename}")



url = 'https://www.booking.com/hotel/am/el-house-yerevan.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaAeIAQGYATG4ARfIAQzYAQHoAQH4AQKIAgGoAgO4Ar-qxLEGwAIB0gIkNjlkZjgwNzctMGFhMi00NTFhLThiNmEtOTgyMTMyZTJkNmI52AIF4AIB&sid=a0024d7247d1bd4da91c7daa61d0ae46&dest_id=-2325645;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;hpos=1;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1714492793;srpvid=d2d370794d4601d3;type=total;ucfs=1&#hotelTmpl'

scraped_text = scrape_webpage(url)

hotel_info = extract_information(scraped_text)

save_to_markdown(hotel_info, "hotel_info.md")