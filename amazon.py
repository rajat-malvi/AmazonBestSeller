from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

# Function to scrape details from a single product URL
def get_single_product_details(driver, product_url):
    """
    Scrapes product details from a given single product URL.
    """
    product_details = {}
    try:
        driver.get(product_url)  # Navigate to the product URL
        time.sleep(3)  # Allow the page to load
        
        # Extract product name
        try:
            product_details['Product Name'] = driver.find_element(By.ID, 'productTitle').text.strip()
        except:
            product_details['Product Name'] = None

        # Extract product price
        try:
            product_details['Product Price'] = driver.find_element(By.XPATH, '//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]').text.strip()
        except:
            product_details['Product Price'] = None

        # Extract best seller rating
        try:
            product_details['Best Seller Rating'] = driver.find_element(By.XPATH, '//i[@class="a-icon a-icon-addon p13n-best-seller-badge"]').text.strip()
        except:
            product_details['Best Seller Rating'] = None

        # Extract ship from
        try:
            product_details['Ship From'] = driver.find_element(By.XPATH, '//div/span[@class="a-size-small tabular-buybox-text-message"]').text.strip()
        except:
            product_details['Ship From'] = None

        # Extract sold by
        try:
            product_details['Sold By'] = driver.find_element(By.ID, 'sellerProfileTriggerId').text.strip()
        except:
            product_details['Sold By'] = None

        # Extract product rating
        try:
            product_details['Product Rating'] = driver.find_element(By.ID, 'averageCustomerReviews').text.strip()
        except:
            product_details['Product Rating'] = None

        # Extract number bought in the past month
        try:
            product_details['Number Bought in the Past Month'] = driver.find_element(By.ID, 'social-proofing-faceout-title-tk_bought').text.strip()
        except:
            product_details['Number Bought in the Past Month'] = None

        # Extract category name
        try:
            product_details['Category Name'] = driver.find_element(By.ID, 'wayfinding-breadcrumbs_feature_div').text.strip()
        except:
            product_details['Category Name'] = None

        # Extract product description
        try:
            product_details['Product Description'] = driver.find_element(By.ID, 'feature-bullets').text.strip()
        except:
            product_details['Product Description'] = None

        # Extract all available images
        try:
            image_elements = driver.find_elements(By.XPATH, "//img[@class= 'imgSwatch']")
            product_details['All Available Images'] = [img.get_attribute('src') for img in image_elements]
        except:
            product_details['All Available Images'] = None

    except Exception as e:
        print(f"Error while scraping product details for URL {product_url}: {e}")
    return product_details


# Function to scrape product URLs from a best-seller category page
def get_product_links_from_category(driver, category_url):
    """
    Extracts product links from a best-seller category page.
    """
    product_links = []
    try:
        driver.get(category_url)  # Navigate to the category URL
        time.sleep(3)  # Allow the page to load

        # Extract product links from the category page
        product_elements = driver.find_elements(By.XPATH, '//a[@class="a-link-normal aok-block"]')
        for element in product_elements:
            product_url = element.get_attribute('href')
            if product_url and '/dp/' in product_url:
                product_links.append(product_url.split('?')[0])  # Remove query parameters
    except Exception as e:
        print(f"Error while scraping product links for category {category_url}: {e}")
    return product_links


# Main function to scrape multiple categories and save results to a CSV
def scrape_multiple_categories_to_csv(bestseller_urls, output_csv_file):
    """
    Scrapes product details from multiple best-seller categories and saves them to a CSV file.
    """
    driver = webdriver.Chrome()  # Adjust based on your setup
    all_product_details = []

    try:
        for category_url in bestseller_urls:
            print(f"Scraping category: {category_url}")
            product_links = get_product_links_from_category(driver, category_url)
            print(f"Found {len(product_links)} product links")
            
            # Limiting products for demo purposes; remove slicing in production
            for product_url in product_links[:2]:  # Adjust range as needed
                print(f"Scraping product: {product_url}")
                product_details = get_single_product_details(driver, product_url)
                all_product_details.append(product_details)

    finally:
        driver.quit()

    # Write data to CSV
    fieldnames = [
        'Product Name', 'Product Price', 'Best Seller Rating',
        'Ship From', 'Sold By', 'Product Rating', 'Number Bought in the Past Month',
        'Category Name', 'Product Description', 'All Available Images'
    ]
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_product_details)
    print(f"Scraped data saved to {output_csv_file}")


if __name__ == "__main__":
    bestseller_urls = [
        "https://www.amazon.in/gp/bestsellers/kitchen/ref=zg_bs_nav_kitchen_0",
        "https://www.amazon.in/gp/bestsellers/shoes/ref=zg_bs_nav_shoes_0",
        "https://www.amazon.in/gp/bestsellers/computers/ref=zg_bs_nav_computers_0",
        "https://www.amazon.in/gp/bestsellers/electronics/ref=zg_bs_nav_electronics_0"
    ]
    
    output_csv_file = "amazon_products.csv"
    scrape_multiple_categories_to_csv(bestseller_urls, output_csv_file)
