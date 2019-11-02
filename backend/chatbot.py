from flask import Flask, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import random
import requests
from flask_cors import CORS
import pickle
import re
import paralleldots
import operator
import config
from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://adiach1:1234@cluster0-jgwg7.mongodb.net/geico?retryWrites=true&w=majority")
db = cluster["geico"]
collection=db["geico"]
# paralleldots.set_api_key(key.emotion_key)
paralleldots.set_api_key(config.emotion_key)

app = Flask(__name__)
CORS(app)



chatbot = ChatBot(
    "GEICOChatBot",
    storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
    logic_adapters=['chatterbot.logic.BestMatch',{'import_path': 'custom_adapters.JokeAdapter'},
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Who made you?',
            'output_text': 'My creators are John, Eric, Aditya, and Will. I was created at the University of California, Riverside in Bourns A171.'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'When is your birthday?',
            'output_text': 'I was born on November 1st, 2019'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'What is the answer to life, the universe, and everything?',
            'output_text': '42'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': '?',
            'output_text': 'I could ask the same of you as well. I don\'t think either of us could give a good answer'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Who\'s that pokemon?',
            'output_text': 'It\'s me'
        }
        ],
    database_uri='mongodb+srv://adiach1:1234@cluster0-jgwg7.mongodb.net/test?retryWrites=true&w=majority',
    read_only=True

)

'''
Leading questions
1. Hey! My name is (GEICO BOT). Please type in your username
{"text":"My name is GEICO BOT. Please type in your username", "type":"leading, "question":"username", "topic":"normal"}
2. How has your day been? This will give us some idea about what movies/songs to recommend you.
{"text":"How has your day been? This will give us some idea about what movies/songs to recommend you.", "type":"leading","question":"day"}
3. What are some of your favorite movies? Seperate each one with a comma.
{"text":"What are some of your favorite movies? Seperate each one with a comma.", "type":"leading", "question":"favorite_movies", "topic":"normal"}
'''
count = 0
last_question = None
username = ''
how_was_your_day = ''
favorite_movies = []
emotion = ''
@app.route('/api/chatbot',methods=['GET','POST'])
def main():
    global count
    # global last_question
    # global username
    # global how_was_your_day
    # global favorite_movies
    # global emotion
    username = ''
    last_question = None
    text = ''

    if request.method == 'POST':
        m = ['movie']
        s = ['song']
        if request.json is not None:
            print("line 61", request.json)
        # username = request.json.get("username")
        # text = request.json.get("text")
        print(bool(request.json))
        if bool(request.json) is False:
            print("Init empty")
            username = ''
            text = ''
            last_question = None
        if bool(request.json) is not False:
            print("Init full")
            username = request.json.get('username')
            text = request.json.get('text')
            last_question = request.json.get("question")

        if username is '' and last_question is None:
            #No response expected
            print("Entry message")
            last_question = {"text":"My name is I-TEA BOT! I recommend movies, music, and do some other stuff as well. First things first, I need a username from you.", "type":"bot", "question":"intro","topic":"normal"}
            count += 1
            return last_question

        if request.json.get('username') == "reset" or request.json.get('username') == "restart" or request.json.get('text') == "reset" or request.json.get('text') == "restart":
            print("RESTART")
            count = 1
            last_question = {"text":"My name is GEICO BOT! I recommend movies, music, and do some other stuff as well. First things first, I need a username from you.", "type":"bot", "question":"intro","topic":"normal"}
            return last_question


        if count > 0 and last_question is not None:

            print("Entereed movie flow")
            #text = request.json.get('text')
            username = request.json.get('username')
            text = request.json.get('text')
            last_question = request.json.get("question")

            print("TEXXXXT")
            print(text)
            # print(re.match(r'.*(recommend|suggest).*movies\.*', text.lower()))
            if last_question == "intro":
                username = request.json.get("username")
                text = request.json.get("text")
                #store the username in the database

                if collection.find({"username":username}).count() == 0:
                    collection.insert_one({"username":username})


                #start the movie flow
                last_question = {"text":"Hi {}! Now we can begin! Try things like \"recommend me some movies\" , \"recommend music\", or \"tell me a joke\".".format(username), "question":"general", "topic":"normal", "type":"bot"}
                return last_question

            if last_question == "restart":

                username = request.json.get("username")

                last_question = {"text":"Hey, sorry about that {}. Even though I'm not human, I still make mistakes. If you want to get movie recommendations type \'recommend movies \'. If you want song recommendations you can say '\recommend music\'. We can just talk too.","type":"bot","topic":"normal","question":"general"}
                return last_question


            if re.match(r'.*(recommend|suggest).*movie(s?)\.*', text.lower()):

                username = request.json.get("username")

                last_question = {"text":"Ok {}, how has your day been? This will give us some idea about what movies to \
                    recommend you.".format(username), "type":"bot","question":"day","topic":"normal"}
                return last_question

            if re.match(r'.*(recommend|suggest).*(song(s?)|music)\.*', text.lower()):
                username = request.json.get("username")

                last_question = {"text":"Ok {}. Tell us about yourself. Would you say that you have an Athletic, Sedentary, or Moderate lifestyle?".format(username), "question":"music_lifestyle", "topic":"questions","type":"bot","options":['Athletic','Sedentary','Moderate']}
                return last_question
            if last_question == "music_lifestyle":
                text = request.json.get("text")
                username = request.json.get("username")
                if not(text == "Athletic" or text == "Sedentary" or text == "Moderate"):
                    last_question = {"text":"Ok {}. Tell us about yourself. Would you say that you have an Athletic, Sedentary, or Moderate lifestyle?".format(username), "question":"music_lifestyle", "topic":"questions","type":"bot","options":['Athletic','Sedentary','Moderate']}
                    return last_question

                collection.find_one_and_update({"username": username}, {"$set": {"lifestyle": text}})

                last_question = {"text":"Great! One more question. Would you say that your hobbies are more Indoor or Outdoor?","question":"music_hobbies", "topic":"questions","type":"bot","options":['Indoor','Outdoor']}
                return last_question

            if last_question == "music_hobbies":
                text = request.json.get("text")

                username = request.json.get("username")

                if not(text == "Indoor" or text == "Outdoor"):
                    last_question = {"text":"Let's try that again {}. Would you say that your hobbies are more Indoor or Outdoor?","question":"music_hobbies", "topic":"questions","type":"bot","options":['Indoor','Outdoor']}
                    return last_question


                collection.find_one_and_update({"username": username}, {"$set": {"hobbies": text}})
                data = collection.find_one({"username":username})

                #data.get("lifestyle") returns the lifestyle input
                #data.get("hobbies") returns the hobbies input
                #have conditions for if the user puts in junk
                if data.get("lifestyle") == "Athletic" and data.get("hobbies") == "Outdoor":
                    list = ["EDM", "Dubstep", "Trap"]
                    randomNum = random.randint(0, len(list)-1)
                    genre = list[randomNum]
                    link = "http://ws.audioscrobbler.com/2.0/?format=json&method=tag.gettoptracks&tag=" + genre + "&api_key=" + config.last_key + "&format=json"
                    resp = requests.get(link).json()
                    store = resp["tracks"]["track"][0]
                    mbid = store["mbid"]
                    newLink = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=" + config.last_key + "&mbid=" + mbid + "&format=json"
                    newResp = requests.get(newLink).json()
                    songInfo = newResp["track"]
                    songName = songInfo["name"]
                    return {"text":"How does the song " + songName + " tickle your ears? ", "question":"general", "topic":"music","type":"bot", "musicInfo": [{"Genre": genre, "Song": songInfo["name"], "Artist": songInfo["artist"]["name"], "Album": songInfo["album"]["title"], "Duration": store["duration"], "Stream": songInfo["url"], "AlbumArt": songInfo["album"]["image"][2]["#text"], "TopTags": songInfo["toptags"]["tag"], "Published": songInfo["wiki"]["published"], "Summary": songInfo["wiki"]["summary"]}]}

                elif data.get("lifestyle") == "Athletic" and data.get("hobbies") == "Indoor":
                    list = ["Rap", "Hip-Hop", "House"]
                    randomNum = random.randint(0, len(list)-1)
                    genre = list[randomNum]
                    link = "http://ws.audioscrobbler.com/2.0/?format=json&method=tag.gettoptracks&tag=" + genre + "&api_key=" + config.last_key + "&format=json"
                    resp = requests.get(link).json()
                    store = resp["tracks"]["track"][0]
                    mbid = store["mbid"]
                    newLink = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=" + config.last_key + "&mbid=" + mbid + "&format=json"
                    newResp = requests.get(newLink).json()
                    songInfo = newResp["track"]
                    songName = songInfo["name"]
                    return {"text":"How does the song " + songName + " tickle your ears? ", "question":"general", "topic":"music","type":"bot", "musicInfo": [{"Genre": genre, "Song": songInfo["name"], "Artist": songInfo["artist"]["name"], "Album": songInfo["album"]["title"], "Duration": store["duration"], "Stream": songInfo["url"], "AlbumArt": songInfo["album"]["image"][2]["#text"], "TopTags": songInfo["toptags"]["tag"], "Published": songInfo["wiki"]["published"], "Summary": songInfo["wiki"]["summary"]}]}

                elif data.get("lifestyle") == "Moderate" and data.get("hobbies") == "Outdoor":
                    list = ["Pop", "Musicals", "Rock"]
                    randomNum = random.randint(0, len(list)-1)
                    genre = list[randomNum]
                    link = "http://ws.audioscrobbler.com/2.0/?format=json&method=tag.gettoptracks&tag=" + genre + "&api_key=" + config.last_key + "&format=json"
                    resp = requests.get(link).json()
                    store = resp["tracks"]["track"][0]
                    mbid = store["mbid"]
                    newLink = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=" + config.last_key + "&mbid=" + mbid + "&format=json"
                    newResp = requests.get(newLink).json()
                    songInfo = newResp["track"]
                    songName = songInfo["name"]
                    return {"text":"How does the song " + songName + " tickle your ears? ", "question":"general", "topic":"music","type":"bot", "musicInfo": [{"Genre": genre, "Song": songInfo["name"], "Artist": songInfo["artist"]["name"], "Album": songInfo["album"]["title"], "Duration": store["duration"], "Stream": songInfo["url"], "AlbumArt": songInfo["album"]["image"][2]["#text"], "TopTags": songInfo["toptags"]["tag"], "Published": songInfo["wiki"]["published"], "Summary": songInfo["wiki"]["summary"]}]}

                elif data.get("lifestyle") == "Moderate" and data.get("hobbies") == "Indoor":
                    list = ["Jazz", "Blues", "Swing"]
                    randomNum = random.randint(0, len(list)-1)
                    genre = list[randomNum]
                    link = "http://ws.audioscrobbler.com/2.0/?format=json&method=tag.gettoptracks&tag=" + genre + "&api_key=" + config.last_key + "&format=json"
                    resp = requests.get(link).json()
                    store = resp["tracks"]["track"][0]
                    mbid = store["mbid"]
                    newLink = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=" + config.last_key + "&mbid=" + mbid + "&format=json"
                    newResp = requests.get(newLink).json()
                    songInfo = newResp["track"]
                    songName = songInfo["name"]
                    return {"text":"How does the song " + songName + " tickle your ears? ", "question":"general", "topic":"music","type":"bot", "musicInfo": [{"Genre": genre, "Song": songInfo["name"], "Artist": songInfo["artist"]["name"], "Album": songInfo["album"]["title"], "Duration": store["duration"], "Stream": songInfo["url"], "AlbumArt": songInfo["album"]["image"][2]["#text"], "TopTags": songInfo["toptags"]["tag"], "Published": songInfo["wiki"]["published"], "Summary": songInfo["wiki"]["summary"]}]}

                elif data.get("lifestyle") == "Sedentary" and data.get("hobbies") == "Outdoor":
                    list = ["Country", "BlueGrass", "Folk"]
                    randomNum = random.randint(0, len(list)-1)
                    genre = list[randomNum]
                    link = "http://ws.audioscrobbler.com/2.0/?format=json&method=tag.gettoptracks&tag=" + genre + "&api_key=" + config.last_key + "&format=json"
                    resp = requests.get(link).json()
                    store = resp["tracks"]["track"][0]
                    mbid = store["mbid"]
                    newLink = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=" + config.last_key + "&mbid=" + mbid + "&format=json"
                    newResp = requests.get(newLink).json()
                    songInfo = newResp["track"]
                    songName = songInfo["name"]
                    return {"text":"How does the song " + songName + " tickle your ears? ", "question":"general", "topic":"music","type":"bot", "musicInfo": [{"Genre": genre, "Song": songInfo["name"], "Artist": songInfo["artist"]["name"], "Album": songInfo["album"]["title"], "Duration": store["duration"], "Stream": songInfo["url"], "AlbumArt": songInfo["album"]["image"][2]["#text"], "TopTags": songInfo["toptags"]["tag"], "Published": songInfo["wiki"]["published"], "Summary": songInfo["wiki"]["summary"]}]}

                elif data.get("lifestyle") == "Sedentary" and data.get("hobbies") == "Indoor":
                    list = ["EDM", "Dubstep", "Trap"]
                    randomNum = random.randint(0, len(list)-1)
                    genre = list[randomNum]
                    link = "http://ws.audioscrobbler.com/2.0/?format=json&method=tag.gettoptracks&tag=" + genre + "&api_key=" + config.last_key + "&format=json"
                    resp = requests.get(link).json()
                    store = resp["tracks"]["track"][0]
                    mbid = store["mbid"]
                    newLink = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=" + config.last_key + "&mbid=" + mbid + "&format=json"
                    newResp = requests.get(newLink).json()
                    songInfo = newResp["track"]
                    songName = songInfo["name"]
                    return {"text":"How does the song " + songName + " tickle your ears? ", "question":"general", "topic":"music","type":"bot", "musicInfo": [{"Genre": genre, "Song": songInfo["name"], "Artist": songInfo["artist"]["name"], "Album": songInfo["album"]["title"], "Duration": store["duration"], "Stream": songInfo["url"], "AlbumArt": songInfo["album"]["image"][2]["#text"], "TopTags": songInfo["toptags"]["tag"], "Published": songInfo["wiki"]["published"], "Summary": songInfo["wiki"]["summary"]}]}


            if last_question == "day":
                #run emotional analysis on the string.
                username = request.json.get("username")
                how_was_your_day = request.json.get('text')
                emotion = "Happy" #placeholder
                response = paralleldots.emotion(how_was_your_day)

                print(response)

                if response.get("emotion") is not None:
                    emotion = max(response.get("emotion").items(), key=operator.itemgetter(1))[0]

                print(emotion)
                collection.find_one_and_update({"username": username},
                                 {"$set": {"how_was_your_day": how_was_your_day, "emotion":emotion}})

                sentence = ''

                if emotion == "Happy":
                    sentence = random.sample(["That's good to hear", "Nice to see you in good spirits.", "I'm glad your chipper"],1)
                if emotion == "Sad" or emotion == "Angry":
                    sentence = random.sample(["I'm sorry your day is going so poorly.","I hope tomorrow is better.","Sad reacts only."],1)
                if emotion == "Excited":
                    sentence = random.sample(["Your day sounded AMAZING!!!","I wish my day was as exciting.","Sounds like today was a rollercoaster!"],1)
                if emotion == "Fear":
                    sentence = random.sample(["I hope your days are calmer in the future.","We have nothing to fear but fear itself.","Never fear, the rules are here!"],1)
                if emotion == "Bored":
                    sentence = random.sample(["Another day, another dollar I suppose.", "Back to the old grind.", "Same tbh."], 1)
                last_question = {"text":sentence[0] + "What are some of your favorite movies? Separate each one with a comma.", "type":"bot", "question":"favorite_movies", "topic":"normal"}

                return last_question


            if last_question == "favorite_movies":

                #first, create the user object
                # post = {"username":username, "how_was_your_day":how_was_your_day, "emotion":emotion, "favorite_movies":favorite_movies}
                #insert into mongo

                #then, prepend the string with a key phrase and send it to the bot. The corresponding logic adapter should pick it up and send it to Will
                username = request.json.get("username")
                text = request.json.get("text")
                user = request.json.get("username")
                text = text.split(', ')
                movieList = []

                for movie in text:
                    link = "http://www.omdbapi.com/?apikey=" + config.omdb_api+"&s=" + movie
                    resp = requests.get(link).json()

                    if resp["Response"]=="True":
                        movieList.append(resp['Search'][0]["imdbID"])
                    else:
                        print("failed")
                if len(movieList) == 0:
                    return {"type": "bot", "text": "I'm sorry I did not find any movies with those names."}

                resp = requests.post("http://167.172.203.238:5500/recommend", json={"ids": movieList})
                collection.find_one_and_update({"username": username},
                                 {"$set": {"movies_liked": movieList}})

                response_data = resp.json()["ids"]
                listings = []

                for ids in response_data:
                    postLink = "http://www.omdbapi.com/?apikey=" + config.omdb_api + "&i="
                    postLink += "tt0" + str(ids)
                    temp = requests.get(postLink).json()
                    if temp["Response"]=="True":
                        listings.append(temp)
                return {"type": "bot", "topic": "movie", "text": "Here are some movies I found: " + listings[0]["Title"] + ", " + listings[1]["Title"] + ", " + listings[2]["Title"] + ", and more if you click on me", "movieInfo": listings, "question":"chatbot"}

            else:
                bot_output = chatbot.get_response(text)
                return {"text":bot_output.text, "type":"bot", "topic":"normal","question":"chatbot"}

    bot_output = chatbot.get_response("tell me a joke")
    return {"text":"Uh Oh! Something went wrong. Let's restart.", "type":"bot","topic":"normal", "question":"restart"}


if __name__ == "__main__":
    app.run(debug=True)
