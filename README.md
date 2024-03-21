This is an application for generating random numbers from geolocation coordinates.

Application consists from 2 main parts:
- worker: reads values from firehose API, filters duplications out and pushes that data to the database. Currently a single instance of SQLLite is used, but one can scale it into multiple db instances
 and push the data depending on the actual location of the final user
- application instance: it includes a pool (cache) which fetches geo coordinates from the database, computes cache from them and saves in memory. By default puul size is 1000, but it's configurable;
  Application instance fetches the data from the pull on demand; it's connected to UI and API endpoints to request random numbers based on the following parameters: min,nax - interval in that random
  numbers will be computed, and N - amount of generated random numbers

Users can request random numbers with UI in the browser or using API endpoints.

<img width="1205" alt="Снимок экрана 2024-03-22 в 00 02 51" src="https://github.com/lvanan/StartHack/assets/18289344/4de63109-ae3a-4b9c-b011-82a36537424e">
