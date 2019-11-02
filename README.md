# Baut
Baut is a chatbot that helps recommend you songs and movies based on your relative feelings and personal lifestyle.

## Frontend
The frontend is written in React, and is split up into several components. The main components that make up the user interface are `Panel`, `MessageForm`, and `MessageList`.

The `Panel` component is used to render any additional information that the chatbot will return back. For instance, when the chatbot returns movie or song recommendations (when the user clicks on the appropriate message), the `Panel` will display more information for the user, such as the movie poster, director, actors etc.

The `MessageForm` component simply takes in the user's input and sends it to the backend. The component also helps construct a `message` with the text.

The `MessageList` component holds all the `message` objects in an Array. It also chooses which type of message to render to the user, such as a normal chatbot message, movie chatbot message, music chatbot message, and user message. Clicking on either a movie or music chatbot message will make the `Panel` component render additional information pertaining to the clicked message, as mentioned before.

 In order to start the frontend, simply navigate to the `frontend` directory and execute the following.

```
npm install
```

Once the node packages have finished installing, you may now run the app by doing
```
npm start
```

The React app will compile and a browser should automatically open to `localhost:3000`, where you can proceed with the chatbot interface.

## Backend
The backend is written in Flask, a Python microframework that makes creating endpoints quick and easy. Within this Flask app we have an endpoint call `api/chatbot`. This endpoint handles all of the dialog flow from the user to the bot. 

The user is first greeted with a prompt to put in their user name. This is to keep track of the recommendations. 

The chatterbot library is used to handle input. If the bot realizes the user is asking for a movie recommendation, it sends calls to the recommendation algorithm. If it realizes the user is asking for a song recommendation, we conditionally recommend a song to the user. If the bot realizes that the user is asking for a joke, it uses a joke api and returns a random joke. If the user is asking for none of these three things, the user submission is handled by the chatterbot greeting and conversation corpus. 
