### Project Proposal: TWITCH Dashboard

**Framing Question:** What games are currently popular on twitch? What twitch statistics should a streamer be aware of if they want to gain popularity? Can a dashboard for twitch stats be created?

**Purpose and Need:** 

1033 BILLION minutes watched in 2021. 2,834,000 average concurrent viewers daily. Twitch.tv is the biggest video game streaming platform. Some seek to gain popularity and success on the platform, however, there is a lot of competition. 9 MILLION unique creators streaming each month, 109,400 average concurrent streamers. What are the trends and statistics that can help streamers maximise the growth of their channels? What games are currently trending? What games are currently growing? What time of day is best for streaming?

**Data Description:**

Twitch API 

https://dev.twitch.tv/docs/api/reference

The top streams can be retrieved, each with the following data:

| Field           | Type    | Description                                                  |
| :-------------- | :------ | :----------------------------------------------------------- |
| `id`            | string  | Stream ID.                                                   |
| `user_id`       | string  | ID of the user who is streaming.                             |
| `user_login`    | string  | Login of the user who is streaming.                          |
| `user_name`     | string  | Display name corresponding to `user_id`.                     |
| `game_id`       | string  | ID of the game being played on the stream.                   |
| `game_name`     | string  | Name of the game being played.                               |
| `type`          | string  | Stream type: `"live"` or `""` (in case of error).            |
| `title`         | string  | Stream title.                                                |
| `viewer_count`  | int     | Number of viewers watching the stream at the time of the query. |
| `started_at`    | string  | UTC timestamp.                                               |
| `language`      | string  | Stream language. A language value is either the [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) two-letter code for a [supported stream language](https://help.twitch.tv/s/article/languages-on-twitch#streamlang) or “other”. |
| `thumbnail_url` | string  | Thumbnail URL of the stream. All image URLs have variable width and height. You can replace `{width}` and `{height}` with any values to get that size image |
| `tag_ids`       | string  | Shows tag IDs that apply to the stream.                      |
| `is_mature`     | boolean | Indicates if the broadcaster has specified their channel contains mature content that may be inappropriate for younger audiences |



I plan to collect the data hourly to observe trends.



**Tools:**

- Python, pandas, NumPy
- GCP/AWS to store database
- MongoDB database
- Streamlit for deployed product
- Plotly for graphs

**MVP Goal:**

Some example graphs to be implemented on the final product.
