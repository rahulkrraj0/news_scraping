
import requests
from bs4 import BeautifulSoup
import re
import os


def File_Save(title, content):
    # Clean title for filename (remove newlines and special characters)
    safe_title = re.sub(r'[<>:"/\\|?*\n’‘“”]', '_', title).strip()
    filename = f"data/{safe_title}.txt"

    # Ensure the "data" directory exists
    os.makedirs("data", exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"File saved as: {filename}")

def Ndtv_Article(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    title = soup.h1.string.strip() if soup.h1 else "No_Title_Found"
    subtitle = soup.h2.string.strip() if soup.h2 else "No Subtitle Found"
        
    content_div = soup.find(class_="Art-exp_wr")
    if content_div:
            paragraphs = [p.get_text() + "\n" for p in content_div.find_all("p")]
            content = "\n".join([title, subtitle] + paragraphs)
    File_Save(title, content)

def TheHindu(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    title = soup.h1.get_text() if soup.h1 else "No_Title_Found"
    title2 = soup.h2.get_text() if soup.h2 else "No_Subtitle_Found"

    caption_tag = soup.find("p", class_="caption")
    caption = caption_tag.get_text() if caption_tag else "No_Caption_Found"

    # Extract text from all divs with data-component="text-block"
    content_div = soup.find("div", id="content-body-69297366")

    if content_div:
        paragraphs = [p.get_text() + "\n" for p in content_div.find_all("p")[:-2]]  # Remove last 2 <p> tags
        content = "\n".join([title, title2] + paragraphs)
    else:
        content = "\n".join([title, title2, caption])  # If no content found

    File_Save(title, content)

def Bbc_Aticle(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    #print(soup.prettify())

    title = soup.h1.get_text() if soup.h1 else "No_Title_Found"
    # Extract text from all divs with data-component="text-block"
    content_divs = soup.find_all("div", attrs={"data-component": "text-block"})
    content = "\n\n".join([title] + [div.get_text() + "\n" for div in content_divs])  # Get text from each div and join
    #print(title, content, sep="\n\n")

    File_Save(title, content)

def IndianExpress(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    title = soup.h1.string.strip() if soup.h1 else "No_Title_Found"
    subtitle = soup.h2.string.strip() if soup.h2 else "No Subtitle Found"
    
    content = soup.find(class_="story_details")
    text = content.get_text().replace("Story continues below this ad", " ") if content else ""

    content = f"{title}\n\n\n{subtitle}\n\n\n{text}"
    File_Save(title, content)

def My_Url(url):
    if "thehindu" in url:
        print("This is The Hindu.")
        TheHindu(url)
    elif "ndtv.com" in url:
        print("This is Ndtv.")
        Ndtv_Article(url)
    elif "bbc" in url:
        print("This is BBC.")
        Bbc_Aticle(url)
    elif "indianexpress" in url:
        print("This is Indian Express.")
        IndianExpress(url)
    else:
        print("Unknown news source.")

def url_list(url):
    """Fetches the webpage and extracts 'article' links from class 'nation'."""
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Find all elements with class "nation"
    nation_elements = soup.find(class_="nation")

    url_lst = []

    # Extract and filter links
    if nation_elements:
        for link in nation_elements.find_all('a', href=True):  # Ensures href exists
            href = link.get('href')

            if "article" in href:  # Only keep links containing "article"
                url_lst.append(href)

    return url_lst  # Return the list of extracted article links



url = input('Enter url: ')
My_Url(url)
