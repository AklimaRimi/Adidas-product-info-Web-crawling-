![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2FAklimaRimi%2FBreadcrumbsAdidas-product-info-Web-crawling-&label=Reads&countColor=%23263759)


# Adidas-product-info-Web-crawling 

This project as technical test. Thank you for this opportunity.


# Objective 
There are a lot of informations I needed to scrap from Adidas Men product. Design the Information for reliability and save the data in an Excel file.

# Solution
For this test, I used Selenium Python library for the web crawler task. Because of multiple clicks and dynamic page scrapping I chose this library.

I saved the data into separate 4 Excel sheets, for better understanding of data and better flexibility.

And I used Python multiprocessing library to get data quickly.

For this test, I had to collect only 200-300 product information. 

For the sake of accurate data, I used ``` time.sleep()``` function for better pace. Though it cost time.


# How to get the data
If you want to run the code you have to follow some instructions.

1. Download the File from this repository.
2. Install the required Python libraries by using this command in **cmd**
   ```python
   python -m pip -r install requirements.txt
   ```
3. Then in the same **cmd** write
   ```python
   python crawler.py
   ```

# Note: To finish running, you need stable network connection.

