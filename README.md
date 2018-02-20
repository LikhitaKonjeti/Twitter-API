# Twitter-Stream-API
A twitter API to trigger streaming of the tweets and displays back the filtered tweets on the HTML page.
# Pre-requisites
Need to install MongoDb.
The  code was implemented using Django framework. Install the necessary files of Django.
Tweepy and Pymongo libraries were imported.
This minimum viable product which has the following functions-
# API 1
This triggers the twitter stream for a keyword sent in request and stores the data in a Nosql database form. The database used here is MongoDB.
At a time 50 streams are stored which are related to the keyword. The user can further stream if required.
# API 2
This takes the filters as per the user's choice.
The filters for position of text ( whether it starts with or ends with or contains in the tweeted text),retweet count, followers count, Favourites count are available.
Sorting can be done based on time.
The filtered tweets are displayed on the HTML page in a table form.If there are no tweets satisfying the filters , then an empty table is returned
The displayed tweets are paginated and 6 tweets are displayed per page
# API 3
Exports the filtered results into a .csv format file which can be used for analysis.
The location has to be specified at the backend.
Various feilds like Tweeted text,Followers count, Created_at, Retweeted count etc are exported.
