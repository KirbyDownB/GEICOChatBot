from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import requests
import pickle
import random
import re
class JokeAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        # self.jokes = pickle.load(file_)
        self.jokes=pickle.load(open('jokes.pickle','rb'))
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        # words = ['tell','joke']
        return re.match(r'.*(tell|give|say).*joke.*', statement.text.lower())
        # if all(x in statement.text.split() for x in words):
        #     return True
        # else:
        #     return False

    def process(self, input_statement, additional_response_selection_parameters):
        

        # Randomly select a confidence between 0 and 1
        # print(self.jokes)
        joke = random.sample(self.jokes,1)[0].get("joke")

        print(joke)
        

        confidence = 1
        if joke is None:
            joke = "Im out of jokes"
        # For this example, we will just return the input as output

        response_statement = Statement(text=joke)
        response_statement.confidence = confidence

        return response_statement


class MovieAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        if statement.text.startswith('Movies:'):
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        #remove the first 7 characters on the string
        movies = input_statement[7:]
        movies = movies.split(',')

        #call will

        