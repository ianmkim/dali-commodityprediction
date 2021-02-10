# Commodity Price Prediction Engine
A lot of developers have tried to apply LSTM models on stocks which are very relient on news and current events for their valuation. My partner Nam and I had the idea to try similar methods on very short term commodities futures which are much less relient on news.

We formulated and trained multiple LSTM, GRU, and transformer models on primarily soybean oil. Only the smallest models are uploaded in this repository as I am unable to release the larger models into the public.

This platform was the first iteration of an easily extenable prediction visualization platform. The reason I uploaded this for the DALI lab is because the other repository is much too large and I haven't really been maintaining it well...


# Installation & Usage
install dependencies "pip install -r requirements.txt --user" and run with "flask run" or "python3 app.py"

You can also find a live version hosted on heroku https://commodityprediction.herokuapp.com/

However, the heroku version will cold boot and therefore will load very very slowly the first time.

