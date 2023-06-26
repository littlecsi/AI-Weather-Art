import requests
from bs4 import BeautifulSoup as bs

def get_top3_news() -> list:
    """
    Gets top 3 most read news from BBC website.

    :return: a `list` of top 3 most read news from BBC website.
    :rtype: list
    """
    URL = 'https://www.bbc.co.uk/news'
    response = requests.get(URL)

    # Pass response into beautifulsoup
    soup = bs(response.content, 'html.parser')

    # Extract the most read news from bbc homepage
    text = [span.text for span in soup.findAll('span', {'class': 'gs-c-promo-heading__title gel-pica-bold'})]

    # Slice from the 5th element (first 5 is the most 'watched' news)
    text = text[5:8]

    return text

def main():
    news = get_top3_news()
    # print(news)
    for header in news:
        print(header)

    return None

if __name__ == '__main__':
    main()