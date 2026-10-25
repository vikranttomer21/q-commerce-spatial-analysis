import pandas as pd
import random
import os

def generate_demographics():
    # Key commercial and residential pin codes across South Delhi, Gurgaon, and Noida
    locations = [
        {"pin_code": "110016", "area_name": "Hauz Khas"},
        {"pin_code": "110024", "area_name": "Defence Colony"},
        {"pin_code": "110048", "area_name": "Greater Kailash"},
        {"pin_code": "110070", "area_name": "Vasant Kunj"},
        {"pin_code": "110017", "area_name": "Malviya Nagar"},
        {"pin_code": "110029", "area_name": "Safdarjung Enclave"},
        {"pin_code": "110020", "area_name": "Okhla Phase 3"},
        {"pin_code": "122002", "area_name": "Cyber City (Gurgaon)"},
        {"pin_code": "122009", "area_name": "Sector 53 (Gurgaon)"},
        {"pin_code": "201301", "area_name": "Sector 15 (Noida)"}
    ]

    data = []
    for loc in locations:
        data.append({
            "pin_code": loc["pin_code"],
            "area_name": loc["area_name"],
            # Generating synthetic business logic proxies
            "avg_monthly_rent": random.randint(45000, 150000), 
            "population_density_score": random.randint(6, 10), 
            "total_households": random.randint(15000, 60000)
        })

    df = pd.DataFrame(data)
    
    # Ensure the directory exists
    os.makedirs("data/processed", exist_ok=True)
    
    output_path = "data/processed/delhi_demographics.csv"
    df.to_csv(output_path, index=False)
    print(f"Demographics mock data successfully generated at: {output_path}")

if __name__ == "__main__":
    generate_demographics()