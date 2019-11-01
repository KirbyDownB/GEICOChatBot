# trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train(
#     "chatterbot.corpus.english.greetings",
#     "chatterbot.corpus.english.conversations"
# )


# while True:
#     try:
#         bot_input = chatbot.get_response(input())
#         print(bot_input)

#     except(KeyboardInterrupt, EOFError, SystemExit):
#         break
# jokes = requests.get("https://icanhazdadjoke.com/search",headers={'Accept': 'application/json'},params={"limit":30}).json().get("results")
# print(jokes)
# with open('jokes.pickle','wb') as f:

# pickle.dump(jokes, file_)
# pickle.dump(jokes,open('jokes.pickle','wb'))


            #if username already exists, a different prompt will occur
                #Back for more movie recommendations are you? Do you have any new movies you like or do you just want more like the ones I've recommended to you previously?
            #else, the rest of this code is fine

 elif count == 1:
            # Username expected

            username = request.form.get('text')

            last_question = {"text":"How has your day been? This will give us some idea about what movies/songs to recommend you.", "type":"leading","question":"day","topic":"normal"}
            count += 1
            return {"text":"How has your day been? This will give us some idea about what movies/songs to recommend you.", "type":"leading","question":"day","topic":"normal"}
        
        elif count == 2:
            # How was your day expected

            how_was_your_day = request.form.get('text')
            # calculate emotion of how was your day
            last_question = {"text":"What are some of your favorite movies? Seperate each one with a comma.", "type":"leading", "question":"favorite_movies", "topic":"normal"}
            count += 1
            return {"text":"What are some of your favorite movies? Seperate each one with a comma.", "type":"leading", "question":"favorite_movies", "topic":"normal"}

        elif count == 3:
            # Favorite movies expected

            favorite_movies = request.form.get('text').split(',')
            # create user object in mongo


            last_question = {"text":"Thanks! Here are some movie recommendations. I do more than just recommend movies you know. Try saying \"tell me a joke\", or just having a regular conversation.", "type":"leading", "question":"fav_mov_response", "topic":"movies"}
            count += 1
            return {"text":"Thanks! Here are some movie recommendations", "type":"leading", "question":"fav_mov_response", "topic":"movies"}


        else:
            text = request.form.get('text')
        
            bot_output = chatbot.get_response(text)

            return {"text":bot_output, "type":"bot"}
