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
        words = ['joke']
        # return re.match(r'.*(tell|give|say).*joke.*', statement.text.lower())
        if all(x in statement.text.split() for x in words):
            return True
        else:
            return False

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


class MovieMusicAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        m = ['movie','movies','songs','song','music']
        print(m)
        print(statement.text)
        if statement.text == "movie" or statement.text == "movies":
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        
        response_statment = Statement(text="Movie? Movie? I heard Movie! Tell me your favorite movies! Separate each one with a comma.") 
        response_statment.confidence = 1
        return response_statment

        # elif all(x in statement.text.split() for x in m) or all(x in statement.text.split() for x in m) or all(x in statement.text.split() for x in m)

class MusicAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        m = ['movie','movies','songs','song','music']
        print(m)
        print(statement.text)
        if statement.text == "movie" or statement.text == "movies":
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        
        response_statment = Statement(text="Movie? Movie? I heard Movie! Tell me your favorite movies! Separate each one with a comma.") 
        response_statment.confidence = 1
        return response_statment
