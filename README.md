
![](keeb_finder_overview.png)

# Purpose
I took interested in mechanical keyboards and saw a lot of discussion on social media about them. So many types of keybaords available now with different materials, layouts, size... I wonder how popular one type is over others, options and technical specification of the keyboard in selling now.

Keeb-finder is a good website for that. They have many keyboards listed and easy to scrape. For the seek of practicing, keyboard data was only scraped from Mar 28, 2024 to Mar 30, 2024 using a Python script [here](https://github.com/NgocHueLy/data_eng_keeb_finder/blob/main/keeb-finder-scraper-products.py). Hopefully this scraping will not be a burden for the site.

Disclaimer: Some keyboards will be missing because of bad url format, or missing info.

# Questions This Project Seeks to Answer
- How many keyboards listed over time 
- Wired/Wireless connection percentage
- Most common material of keyboard case
- Most popular keyboard brands

# Tech Stack
- [Python Script](https://github.com/NgocHueLy/data_eng_keeb_finder/blob/main/keeb-finder-scraper-products.py) to scrape keyboards tile and detail listing from [keeb-finder/com/keyboards](https://keeb-finder.com/keyboards)
- [GitHub](https://github.com/) repo for storing scraped data and the project
- [Google Cloud](https://console.cloud.google.com/?hl=en&project=dtc-de-course-412502) to use BigQuery as data warehouse. I haven't set up VM machine since my GCP free trial already ended.
- [Mage](https://www.mage.ai/) used to orchestrate and monitor pipeline
- [DBT Core](https://www.getdbt.com/) to transform data in BigQuery and prepare for visualization using SQL
- [Looker Studio](https://lookerstudio.google.com/) to visualize the transformed dataset
- [Pandas](https://pandas.pydata.org/) to import and transform dataset
- [Terraform](https://www.terraform.io/) for version control of our infrastructure
- [Docker](https://docker.io/) for Mage image. I also update dbt to latest version iva Mage terminal as the original dbt version in Mage not working


# Pipeline Architecture
![](keeb-finder-pipeline.png)
- Python script scrape data from keeb-finder.com and save them as csv files. These files were uploaded to GitHub for easier to work with Mage
- Terraform is used to setup BigQuerry database
- Project keeb-finder create in Mage and use to load and clean data from GitHub to BigQuery. 
- dbtCore also run inside Mage as dbt blocks to build and load models to BigQuery
- Looker Studio is used to visualized the transformed dataset by dbt
# Structure of Data Models
![](dbt-graph.png)



# Dashboard Preview
View dashboard [here](https://lookerstudio.google.com/reporting/093cd60c-59a7-44e8-b1c1-97235457e8c9)

![](dashboard_preview.png)

# Replication Steps

# Next Steps
- More automation with Mage, scape data with Mage and load to GCS instead of GitHub
- CI/CD run pipeline daily