# vehicle_collisions
# Setup
### Getting Started
This project is dockerized but requires a little bit of setup to get everything working.
If you dont have docker detup on your local machine please go ahead and download it from 
https://www.docker.com/products/docker-desktop

#### Step One
We need to download the CSV from Citi Bike that contains all the data
Go ahead and run the bash script
`./download_citi_bike_data.sh'
This will download the Zip , unzip, and move to the static folder for use later

#### Step Two
We need to add the Google API key to the html file, I provided that in the email.
cycle_collisions/templates/index.html
add the api key to 'src="https://maps.googleapis.com/maps/api/js?key=API_KEY&callback=initMap&libraries=&v=weekly&libraries=geometry"
'
#### Step Three
Build The Docker Container
`docker-compose build`

#### Step Four
Run the Container when it is built
`docker-compose up -d`

#### Step Five
Last step is we need to load the data to our database. We need to access the shell and run some functions
`docker exec -it vehicle_collisions_web_1 bash` this will acces the bash termiaal
`python manage.py shell` access django shell
Run the following carefully 
`from cycle_collisions.nyc_collision_data import get_nyc_collision_data`
Load the boroughs
`get_nyc_collision_data.add_boroughs_to_db()`
Next, Load the crash infromation
`get_nyc_collision_data.add_data_to_db()`
The last script take time due to the large amount of data being iterated so please be patient
`get_nyc_collision_data.get_citi_bike_data_and_add_to_db()`
This take a few minutes but onece completed it will return quersets with sorted data