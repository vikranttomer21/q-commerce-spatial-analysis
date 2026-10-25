from playwright.sync_api import sync_playwright
import pandas as pd
import re
import os

def scrape_dark_stores_full(search_query):
    stores_data = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) 
        page = browser.new_page()
        page.goto("https://www.google.com/maps", wait_until="domcontentloaded")
        
        search_box = page.locator('input[name="q"]')
        search_box.wait_for(state="visible", timeout=15000)
        search_box.fill(search_query)
        search_box.press('Enter')
        page.wait_for_timeout(5000) 
        
        scrollable_pane_selector = 'div[role="feed"]'
        
        # Error handling: If the scroll feed doesn't load, skip scrolling
        try:
            page.wait_for_selector(scrollable_pane_selector, timeout=10000)
            previous_count = 0
            while True:
                page.evaluate(f'''
                    const pane = document.querySelector('{scrollable_pane_selector}');
                    pane.scrollTo(0, pane.scrollHeight);
                ''')
                page.wait_for_timeout(3000)
                
                elements = page.query_selector_all('a.hfpxzc')
                current_count = len(elements)
                
                if current_count == previous_count:
                    print(f"Extraction complete for {search_query}. Found: {current_count}")
                    break
                previous_count = current_count
                print(f"Scrolling... currently loaded: {current_count}")
        except Exception:
            print(f"No scrollable feed found for {search_query}. Extracting visible results.")

        # Extract whatever elements are on the screen
        elements = page.query_selector_all('a.hfpxzc')
        for el in elements:
            url = el.get_attribute('href')
            name = el.get_attribute('aria-label')
            
            coords = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', url)
            if coords:
                stores_data.append({
                    "brand_name": name,
                    "latitude": float(coords.group(1)),
                    "longitude": float(coords.group(2)),
                    "search_zone": search_query
                })
                
        browser.close()
    return pd.DataFrame(stores_data)

if __name__ == "__main__":
    queries = [
        "Blinkit South Delhi", "Blinkit Gurugram", "Blinkit Noida", 
        "Blinkit East Delhi", "Blinkit West Delhi", "Blinkit Dwarka",
        "Zepto South Delhi", "Zepto Gurugram", "Zepto Noida", 
        "Zepto East Delhi", "Zepto West Delhi", "Zepto Dwarka",
        "Swiggy Instamart South Delhi", "Swiggy Instamart Gurugram", "Swiggy Instamart Noida"
    ]
    all_data = pd.DataFrame()
    
    for query in queries:
        print(f"Starting pipeline for: {query}")
        try:
            df = scrape_dark_stores_full(query)
            all_data = pd.concat([all_data, df], ignore_index=True)
        except Exception as e:
            print(f"Pipeline failed for {query}: {e}. Skipping to next.")
            continue
        
    # Updated Pandas deduplication syntax
    all_data = all_data.drop_duplicates(subset=['latitude', 'longitude'])
    
    os.makedirs("data/raw", exist_ok=True)
    output_path = "data/raw/delhi_ncr_competitors.csv"
    all_data.to_csv(output_path, index=False)
    print(f"Raw competitor data exported to: {output_path}. Total unique records: {len(all_data)}")