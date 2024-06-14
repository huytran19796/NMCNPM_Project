import os

import twisted
import asyncio
import boto3

print(twisted.__version__)
print(twisted.__version__)
print(twisted.__version__)
print(twisted.__version__)

os.chdir('/opt/airflow/crawling/Crawl_Project')
os.system("scrapy crawl conferences -o /opt/airflow/data_stage_1/stage_1.json")