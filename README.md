# Project Immo Eliza

## Description

Web Scraping Immo Website
This project focuses on web scraping the Immo website, the largest real estate website in Belgium. The goal was to collect data on houses and apartments, resulting in approximately 20,000 records.
The collected data underwent several analyses, including pass analysis, cluster analysis, and principal component analysis. The scraping process utilized Beautiful Soup, a Python library for web scraping, while data cleaning was performed using Pandas, a popular data manipulation library in Python.
To conduct the statistical analysis, the R programming language was employed. The R program provided the necessary tools and packages to perform various statistical analyses on the scraped and cleaned data.
Installation
To run this project, you need to have Python and R installed on your system. Additionally, ensure that the following libraries are installed for Python:
•	Beautiful Soup: pip install beautifulsoup4
•	Pandas: pip install pandas
For R, make sure you have the required packages installed, which will be mentioned in the analysis section.
Usage
1.	Clone this repository to your local machine.
2.	Open the Python script web_scraping.py and update the necessary parameters, such as the target URL and the data collection settings.
3.	Run the web_scraping.py script to initiate the web scraping process. The scraped data will be saved in a CSV file.
4.	Open the R script data_analysis.R and modify any required input paths or settings.
5.	Run the data_analysis.R script to perform statistical analysis on the scraped data.
Analysis
The statistical analysis of the scraped data was performed using R. The script data_analysis.R contains the code for pass analysis, cluster analysis, and principal component analysis. Make sure to update the input file path to the location where the scraped data is stored.
The R script relies on various packages, such as dplyr, ggplot2, and factoextra. 
Results
The results of the analysis can be found in the results directory. This directory contains visualizations and summaries obtained from the statistical analyses performed on the scraped data.
Contributing
Contributions to this project are welcome. If you encounter any issues or have suggestions for improvement, please open an issue or submit a pull request.
License
This project is licensed under the MIT License. Feel free to use and modify the code as per your needs.
Contact
If you have any questions or inquiries, please feel free to contact the project maintainer at k.mehdikhanlou@gmail.com.


