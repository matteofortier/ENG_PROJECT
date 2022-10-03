# Game Genres Labeller - Using Deep Learning Techniques

*Matteo Fortier*

![app1.png](app1.png)
![app2.png](app2.png)
![pie_chart.png](pie_chart.png)
![stacked_area.png](stacked_area.png)


## Design

Today, many people dream of becoming a sucessful game streamer, whether it be on twitch or some other game streaming platform. Some want it as their dream job, while some simply enjoy streaming gaming content and entertainment to many people around the world. However, it is harder than ever to become successful as the market becomes more and more saturated. 9 MILLION unique creators streaming each month, 109,400 average concurrent streamers. What if there was a analytics dashboard that could help starting streamers know their platform and their market better, allowing them to get on trends early, and grow faster as a streamer?

## Data

The Twitch API was used for this project. The API allowed us to collect all current streams at any given moment, sorted in views. Each stream would have all the information on it such as the number of  viewers, the game being played, the language, the streamer, the title, the  tags. There was potential to collect a massive amount of data. But for this proof of concept the amount of data collected was limited to the top 1000 streams, every 30 minutes. Additionally the API does not allow for collection of historical data, so the data available at this time is only around 7 days worth. 

## Algorithms

 ***Data Engineering Pipeline***

- Data Collection From Twitch API to MongoDB Atlas:
  - Twitch API Requests
  - Automated using APScheduler -> Set to run every half hour interval
  - Automated scheduler is run on a light google compute unit
  - Each 30 minute batch is pushed onto MongoDB Atlas
- Data Collection  From MongoDB Atlas:
  - Using pymongo requests and read-only user
- Data Visualisation Using Plotly
- Web-app using Dash
  - Deployment using heroku

## Tools

- MongoDB, MongoDB Atlas
- APScheduler
- Google Cloud Platform
- Plotly
- Dash
- Heroku

## Communication

The project used powerpoint for the presentation and dash, plotly and heroku for the web-app
