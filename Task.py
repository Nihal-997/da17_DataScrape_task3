import pandas as pd
from playwright.sync_api import sync_playwright

# Dictionary to convert rating words to numbers
rating_map = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://books.toscrape.com/')
    page.wait_for_timeout(4000)

    book_elements = page.query_selector_all('.product_pod')
    book_data = []

    for book in book_elements:
        title = book.query_selector('h3 > a').get_attribute('title')
        price = book.query_selector('.price_color').inner_text().replace('£', '')
        rating_class = book.query_selector('p.star-rating').get_attribute('class')
        rating_word = rating_class.replace('star-rating', '').strip()
        rating_number = rating_map.get(rating_word, None)

        book_data.append({
            'title': title,
            'price': price,
            'rating': rating_number
        })

    # Optional: keep only first 20 books
    book_data = book_data[:20]

    pd.DataFrame(book_data).to_csv('book_info.csv', index=False)
    print(book_data)