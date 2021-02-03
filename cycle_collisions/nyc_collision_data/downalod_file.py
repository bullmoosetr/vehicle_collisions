
import requests
 
print('Download Starting...')
 
url = 'https://s3.amazonaws.com/tripdata/201901-citibike-tripdata.csv.zip'
 
req = requests.get(url)
 
 
with open("201901-citibike-tripdata.csv.zip",'wb') as zip:
    zip.write(req.content)
 
print('Download Completed!!!')