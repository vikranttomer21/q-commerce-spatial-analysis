CREATE DATABASE IF NOT EXISTS qcommerce_spatial_db;
USE qcommerce_spatial_db;

CREATE TABLE demographic_demand (
    pin_code VARCHAR(10) PRIMARY KEY,
    area_name VARCHAR(100),
    avg_monthly_rent DECIMAL(10, 2),
    population_density_score INT,
    total_households INT
);

CREATE TABLE competitor_locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand_name VARCHAR(150),
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    search_zone VARCHAR(100),
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
USE qcommerce_spatial_db;

CREATE OR REPLACE VIEW vw_competitor_density AS
SELECT 
    search_zone,
    COUNT(id) AS total_stores,
    SUM(CASE WHEN brand_name LIKE '%Blinkit%' THEN 1 ELSE 0 END) AS blinkit_stores,
    SUM(CASE WHEN brand_name LIKE '%Zepto%' THEN 1 ELSE 0 END) AS zepto_stores,
    SUM(CASE WHEN brand_name LIKE '%Swiggy%' THEN 1 ELSE 0 END) AS swiggy_stores
FROM competitor_locations
GROUP BY search_zone;