from promptflow import tool
import requests
from bs4 import BeautifulSoup
import json

@tool
def get_amazon_reviews(product_name: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    search_url = f"https://www.amazon.com/s?k={product_name.replace(' ', '+')}"
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        product_link = soup.select_one('a.a-link-normal.s-no-outline')
        if not product_link:
            return json.dumps({"error": "No product found"})
        
        product_url = 'https://www.amazon.com' + product_link['href']
        response = requests.get(product_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        reviews = []
        review_elements = soup.select('div[data-hook="review"]')
        
        if not review_elements:
            all_reviews_link = soup.select_one('a[data-hook="see-all-reviews-link-foot"]')
            if all_reviews_link:
                all_reviews_url = 'https://www.amazon.com' + all_reviews_link['href']
                response = requests.get(all_reviews_url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                review_elements = soup.select('div[data-hook="review"]')
        
        for review in review_elements[:5]:
            title_elem = review.select_one('[data-hook="review-title"]')
            rating_elem = review.select_one('[data-hook="review-star-rating"]')
            body_elem = review.select_one('[data-hook="review-body"]')
            
            if title_elem and rating_elem and body_elem:
                reviews.append({
                    'title': title_elem.get_text(strip=True),
                    'rating': rating_elem.get_text(strip=True),
                    'body': body_elem.get_text(strip=True)[:200] + '...'
                })
        
        return json.dumps({"product": product_name, "reviews": reviews})
    
    except Exception as e:
        return json.dumps({"error": str(e)})

# Example usage (not part of the tool, just for testing):
# product_name = "Logitech G Pro Wireless Gaming Mouse"
# result = get_amazon_reviews(product_name)
# print(result)
