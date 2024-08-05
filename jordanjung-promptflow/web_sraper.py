from promptflow import tool
import requests
from bs4 import BeautifulSoup

@tool
def scrape_mouse_review():
    url = "https://www.rtings.com/mouse/reviews/logitech/g-pro-x-superlight-2"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.find('h1', class_='title-section').text.strip()
        
        # Extract overall score
        overall_score = soup.find('div', class_='overall-score-box').find('div', class_='score').text.strip()
        
        # Extract pros and cons
        pros = [li.text.strip() for li in soup.find('div', class_='pros-info').find_all('li')]
        cons = [li.text.strip() for li in soup.find('div', class_='cons-info').find_all('li')]
        
        # Extract summary
        summary = soup.find('div', class_='summary').find('p').text.strip()
        
        result = f"Review: {title}\n"
        result += f"Overall Score: {overall_score}\n"
        result += "Pros:\n" + "\n".join(f"- {pro}" for pro in pros) + "\n"
        result += "Cons:\n" + "\n".join(f"- {con}" for con in cons) + "\n"
        result += f"Summary: {summary}\n"
        
        return result
    except Exception as e:
        return f"Error scraping website: {str(e)}"