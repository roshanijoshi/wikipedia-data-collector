import requests
from bs4 import BeautifulSoup
from database import insert_data
url = 'https://en.wikipedia.org/wiki/English_language'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1', id='firstHeading').text.strip()
    print("Page Title:", title)

    data = {"title": title}
    
    paragraphs = soup.find_all('p')  
    introduction = None
    for para in paragraphs:
        if para.text.strip():  
            introduction = para.text.strip()
            break
    if introduction:
        print(f"\nIntroduction Paragraph:\n{introduction}")
        data["introduction"] = introduction
    else:
        print("\nIntroduction paragraph not found.")
        data["introduction"] = None 
    
    try:
        first_image = soup.find('table', class_='infobox').find('img')['src']
        print("\nFirst Image URL:", f"https:{first_image}")
        data["first_image"] = f"https:{first_image}"
    except AttributeError:
        print("\nNo image found.")
        data["first_image"] = None
    
    history_section = soup.find('span', id='History')
    history_content= None
    if history_section:
        paragraphs = history_section.find_parent('h2').find_next_siblings()
        data["history_content"] = [p.text.strip() for p in paragraphs if p.name == 'p']
        print("\n".join("history_content"))
        
    else:
        print("History section not found.")
        data["history_content"]=""
        
    insert_data(data["title"], data["introduction"], data["first_image"], data["history_content"])

else:
    print("Failed to fetch the page. Please check the URL or your internet connection.")
