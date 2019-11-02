import React, { Component } from 'react';
import './App.css';
import MessageForm from './components/MessageForm/MessageForm';
import MessageList from './components/MessageList/MessageList';
import Panel from './components/Panel/Panel';
import { BASE_URL } from './constants';

const chatGroup = require('./assets/chatGroup.svg');

const initialMessages = [
  {
    type: "bot",
    topic: "normal",
    text: "Hey there! My name is Bot! I recommend movies, music, and some other stuff as well! Try things like \"recommend me some movies\", or \"tell me a joke\"."
  },
  {
    type: "bot",
    topic: "normal",
    text: "To start things off, what's your name?"
  }
];

class App extends Component {
  state = {
    messages: [],
    activeMessage: null,
    name: "",
    errorMessage: "",
    isBotLoading: false
  }

  componentDidMount = () => {
    fetch(`${BASE_URL}/api/chatbot`, {
      method: "POST"
    })
      .then(response => response.json())
      .then(data => {
        this.setState({ messages: [...this.state.messages, data] });
      })
      .catch(error => {
        console.error(error);
      })
  }

  sendName = message => {
    const name = message.text;
    this.setState({
      messages: [...this.state.messages, message],
      name,
      isBotLoading: true
    });

    fetch(`${BASE_URL}/api/chatbot`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        "text": name
      })
    })
      .then(response => response.json())
      .then(({type, topic, text}) => {
        const botMessage = { type, topic, text };
        this.setState({
          isBotLoading: false,
          errorMessage: "",
          messages: [...this.state.messages, botMessage]
        });
      })
      .catch(error => {
        console.error(error);
        this.setState({
          isBotLoading: false,
          errorMessage: "Something went wrong!"
        });
      })
  }

  sendMessage = message => {
    this.setState({
      messages: [...this.state.messages, message],
      isBotLoading: true
    });

    if (this.state.name) {
      fetch(`${BASE_URL}/api/chatbot`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          "text": message.text,
          "name": this.state.name
        })
      })
        .then(response => response.json())
        .then(({ type, topic, text }) => {
          const botMessage = { type, topic, text };
          this.setState({
            isBotLoading: false,
            errorMessage: "",
            messages: [...this.state.messages, botMessage]
          });
        })
        .catch(error => {
          console.error(error);
          this.setState({
            isBotLoading: false,
            errorMessage: "Something went wrong!"
          });
        })
    }
  }

  setActiveMessage = message => {
    this.setState({ activeMessage: message });
  }

  render() {
    return (
      <div className="App">
        <div className="container-fluid">
          <div className="row">
            <div className="col-4 left">
              {!this.state.activeMessage && <div className="app__chatGroup--inactive">
                <img className="app__chatGroup" src={chatGroup} alt=""/>
                <div className="app_chatGroup--caption">Click on a message with a <span className="bold">red</span> or <span className="bold">gold</span> chatbot icon to show more details about it!</div>
              </div>}
              {this.state.activeMessage && <div className="app__chatGroup--active">
                <Panel activeMessage={this.state.activeMessage} />
              </div>}
            </div>
            <div className="col-8 right">
              <div className="app__top-div">
                <MessageList isBotLoading={this.state.isBotLoading} messages={this.state.messages} setActiveMessage={this.setActiveMessage} name={this.state.name} />
              </div>
              <div className="app__bottom-div">
                <MessageForm sendMessage={this.sendMessage} sendName={this.sendName} name={this.state.name} />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
