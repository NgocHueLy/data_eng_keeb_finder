{{
    config(
        materialized='view'
    )
}}

WITH keyboard_details AS (
    SELECT *
    FROM {{ ref("base_keyboard_details") }}
),
purchase_options AS (
    SELECT *
    FROM {{ ref("base_purchase_options") }}
)

SELECT 
    k.product_tilte,
    k.product_price,
    k.category_vendor,
    k.category_voucher,
    k.is_new,
    k.listing_link,
    k.brand,	
    k.product_type,
    k.keyboard_profile,
    k.layout_size,
    k.layout_standard,
    k.layout_ergonomics,
    k.is_hot_swappable,
    k.has_knob_support,
    k.has_rgb_support,
    k.has_display_support,
    k.has_qmk_via,
    k.connection, 
    k.is_wireless,
    k.battery_capacity,
    k.mount_style,
    k.case_material,
    k.keycap_material,
    k.scraping_date,
    p.location,
    p.stock_status

FROM keyboard_details k
JOIN purchase_options p 
ON k.listing_link = p.listing_link
    AND k.scraping_date = p.scraping_date

