import requests
from bs4 import BeautifulSoup

def scrape_amazon(product_name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    search_url = f"https://www.amazon.com/s?k={product_name.replace(' ', '+')}"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for item in soup.select('.s-result-item'):
        title_elem = item.select_one('h2 a.a-link-normal')
        price_whole_elem = item.select_one('.a-price-whole')
        price_fraction_elem = item.select_one('.a-price-fraction')
        price = None

        if price_whole_elem and price_fraction_elem:
            price = f"{price_whole_elem.get_text(strip=True)}.{price_fraction_elem.get_text(strip=True)}"
        
        if title_elem and price:
            results.append({
                'title': title_elem.get_text(strip=True),
                'price': price,
                'link': "https://www.amazon.com" + title_elem['href']
            })
    return results

def scrape_ebay(product_name):
    search_url = f"https://www.ebay.com/sch/i.html?_nkw={product_name.replace(' ', '+')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for item in soup.select('.s-item'):
        title = item.select_one('.s-item__title')
        price = item.select_one('.s-item__price')
        link = item.select_one('.s-item__link')
        if title and price and link:
            results.append({
                'title': title.get_text(strip=True),
                'price': price.get_text(strip=True),
                'link': link['href']
            })
    return results

def scrape_all_sites(product_name):
    amazon_results = scrape_amazon(product_name)
    ebay_results = scrape_ebay(product_name)
    return {'amazon': amazon_results, 'ebay': ebay_results}
