{{
    config(
        materialized='view'
    )
}}

SELECT    	
    listing_title AS listing_link,
    Location AS location,
    CASE
        WHEN SEARCH(price,"Out of stock")=true THEN "Out of stock"
        ELSE "In stock" 
    END AS stock_status,
    PARSE_DATE("%Y-%m-%d",scraping_date) AS scraping_date 


FROM {{ source('base', 'purchase_options') }}

