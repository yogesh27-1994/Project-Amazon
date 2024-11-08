import requests
from bs4 import BeautifulSoup as bs
import csv

# Define headers for the HTTP request to mimic a browser visit
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0',
}

# Define parameters for the search query on Amazon
params = {
    'rh': 'n:6612025031',
    'fs': 'true',
    'ref': 'lp_6612025031_sar',
}

# Send a GET request to Amazon with specified headers and parameters
try:
    response = requests.get('https://www.amazon.in/s', params=params, headers=headers, timeout=10)
    # Check if the request was successful
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    exit(1)  # Exit if there's an error with the request

# Parse the HTML content of the page using BeautifulSoup
page_ = bs(response.text, "html.parser")

# List to store extracted product data
products_data = []

# Locate the main container with all product items
main_container = page_.find("div", class_="s-main-slot s-result-list s-search-results sg-row")

# Check if the main container was found
if not main_container:
    print("Error: Could not find the product list container on the page.")
    exit(1)

# Loop through each product block in the main container
for product in main_container.find_all("div", {"data-component-type": "s-search-result"}):
    # Extract the product title
    title_tag = product.find("span", class_="a-size-base-plus a-color-base a-text-normal")
    product_name = title_tag.get_text().strip() if title_tag else "No title available"

    # Extract the product rating
    rating_tag = product.find("span", class_="a-icon-alt")
    product_rating = rating_tag.get_text().strip() if rating_tag else "No rating available"

    # Extract the product price (only whole part)
    price_tag = product.find("span", class_="a-price-whole")
    product_price = price_tag.get_text().strip() if price_tag else "No price available"

    # Append the extracted data to the products_data list
    products_data.append([product_name, product_rating, product_price])

# Check if any products were found
if not products_data:
    print("No products found. Please check the page structure or search parameters.")
else:
    # Write the extracted data to a CSV file
    csv_filename = "products.csv"
    try:
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)  # Wrap all fields in quotes
            # Write the header row
            writer.writerow(["Product_Name", "Rating", "Price"])
            # Write each product's data row
            writer.writerows(products_data)
        print(f"Data has been successfully saved to {csv_filename}")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")
