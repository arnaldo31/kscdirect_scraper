# kscdirect scraper

Faron Schonfeld 
i currently have another person working on that scrape. What about this site? https://kscdirect.com/ I would need one csv that contains all product details and another csv that contains the product id along with price

## Technologies Used
- Python
- csv

## Installation
1. You will need to have [Python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) installed (on Mac they are already installed)
2. You will need to install the following packages with `pip`:
   go to `cmd` and type each of this line
   
    - Windows commands:
      ```
      python -m pip install requests
      python -m pip install beautifulsoup4
      python -m pip install lxml
      ```

## How to Use
1. Open folder where this project is saved on your local machine
2. Run the `kscdirect_scraper.py`
3. Wait the script to finish.

## Location of savefile
  - `save_product` folder with complete product details
  - `save_with_price` folder with price

## Filename
kscdirect_products_category_{`category`}_{`date`}.csv
