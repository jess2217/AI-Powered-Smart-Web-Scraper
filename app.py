import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Initialize list to store quotes
quote_file = []

# Streamlit UI
st.title("Goodreads Quote Scraper")
tag = st.selectbox('Choose a topic', ['love', 'humor', 'friendship', 'life', 'technology'])
generate = st.button('Generate Quotes')

# Construct the URL
url = f"https://www.goodreads.com/quotes/tag/{tag}"
st.write(f"Scraping from: {url}")

if generate:
    try:
        # Send request and parse content
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        content = BeautifulSoup(res.content, 'html.parser')

        # Find quotes
        quotes = content.find_all('div', class_='quote')

        for quote in quotes:
            text_tag = quote.find('div', class_='quoteText')
            if text_tag:
                text = text_tag.text.strip().split("\n")[0]  # Extracting main quote text
            
            author_tag = quote.find('span', class_='authorOrTitle')
            author = author_tag.text.strip() if author_tag else "Unknown"

            # Goodreads does not provide a direct quote link, so linking to author page
            link_tag = quote.find('a', class_='authorOrTitle')
            link = f"https://www.goodreads.com{link_tag['href']}" if link_tag else url

            # Display in Streamlit
            st.success(text)
            st.markdown(f"**Author:** {author}")
            st.markdown(f"[View More Quotes]({link})")
            
            # Append to list
            quote_file.append([text, author, link])

        # Save quotes to CSV
        if quote_file:
            df = pd.DataFrame(quote_file, columns=['Quote', 'Author', 'Link'])
            df.to_csv('quotes.csv', index=False, encoding='utf-8')
            st.success("Quotes saved to quotes.csv")

    except Exception as e:
        st.error(f"Error: {e}")
