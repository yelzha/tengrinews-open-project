This project automates the extraction, transformation, and loading of data from Tengrinews.kz to facilitate detailed analytical processes. The primary goals include performing sentiment analysis and aggregating data based on geographic and temporal criteria to derive insightful information.

System Architecture
Data Extraction:

Source: Tengrinews.kz
Frequency: Daily scraping at 00:00 UTC
Tool: Custom Python script utilizing libraries like BeautifulSoup or Scrapy for web scraping.
Data Transformation and Storage:

Processing: Python scripts are employed to clean and transform the scraped data.
Storage: The data is saved as a parquet file, partitioned by date, in a Google Cloud Storage (GCS) bucket to optimize query performance and manage costs effectively.
Data Enrichment:

Comments Retrieval: Comments from the past 7 days are retrieved using an API to ensure that recent interactions are included.
Integration: News data and comments are integrated prior to loading into BigQuery.
Data Loading:

Database: Google BigQuery
Method: Batch loading of the processed and enriched data ensures efficiency and accuracy.
Data Analysis and Transformation:

Tool: dbt (data build tool)
Transformations:
Sentiment analysis on news content and comments.
Data aggregation by country and other pertinent dimensions.
Additional Feature: Advanced Geospatial Analysis
Feature Description:
Implement advanced geospatial analysis to provide deeper insights into how news sentiment and topics vary across different regions. This feature will allow the identification of geographic patterns in news engagement and sentiment, aiding targeted content delivery and marketing strategies.

Implementation:

Geospatial Data Integration: Enhance the data model to include geographic information where possible (e.g., from user comments or IP addresses).
Analysis Tools: Utilize GIS (Geographic Information System) tools within BigQuery or integrate with external libraries in Python to perform spatial analysis.
Visualization: Extend existing visualizations in tools like Google Data Studio or Tableau to include maps and geographic heatmaps of data.
Conclusion
The documentation outlines the complete workflow of the project and introduces an advanced feature to enhance geographic analytical capabilities. This additional geospatial analysis feature could significantly boost the project's ability to provide nuanced insights, supporting more strategic decision-making based on regional trends and patterns.
