import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://catalog.yale.edu/ycps/subjects-of-instruction/computer-science/"

# Send a request to fetch the webpage
response = requests.get(url)
response.raise_for_status()  # Check if request was successful

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Try to locate a section with course information
main_content = soup.find('div', class_='col-12 col-md-8')

# Retrieve and clean text if content is found
if main_content:
    text_content = main_content.get_text(separator='\n', strip=True)
    
    # Save text content to a .txt file
    with open('yale_computer_science_catalog.txt', 'w', encoding='utf-8') as file:
        file.write(text_content)
    print("Text content successfully saved to yale_computer_science_catalog.txt")
else:
    print("Failed to find the main content on the page.")
