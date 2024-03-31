{{
    config(
        materialized='view'
    )
}}

SELECT 
    cate_product_title AS product_tilte,
    CAST(REPLACE(cate_price,"$","") AS INT64 ) AS product_price,
    cate_vendor AS category_vendor,
    CASE 
        WHEN cate_voucher = "None" THEN 0
        ELSE CAST(cate_voucher AS FLOAT64)
    END AS category_voucher,
    cate_new_tag AS is_new,
    listing_link,
    Brand AS brand,
    Product_type AS product_type,
    Profile AS keyboard_profile,
    CASE
        WHEN Layout_size = "870%" THEN "87%"
        WHEN SEARCH(cate_product_title,'numpad')=true THEN "Numpad"
        ELSE Layout_size
    END AS layout_size,
    Layout_standard AS layout_standard,
    Layout_ergonomics AS layout_ergonomics,
    hot_swappable AS is_hot_swappable,
    Knob_support AS has_knob_support,
    Rgb_support AS has_rgb_support,
    Display_support AS has_display_support,
    QMK_or_VIA AS has_qmk_via,
    Connection AS connection,
    CASE
        WHEN Connection="Wired" THEN "No"
        ELSE "Yes"
    END AS is_wireless,
    CASE
        WHEN Battery_capacity = "-" THEN "Unknown"
        ELSE Battery_capacity
    END AS battery_capacity,
    Mount_style AS mount_style,
    Case_material AS case_material,
    Keycap_material AS keycap_material,
    PARSE_DATE("%Y-%m-%d",scraping_date) AS scraping_date

FROM {{ source('base', 'keyboard_details') }}

