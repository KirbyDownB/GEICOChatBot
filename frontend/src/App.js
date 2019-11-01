import React, { Component } from 'react';
import './App.css';
import MessageForm from './components/MessageForm/MessageForm';
import MessageList from './components/MessageList/MessageList';

const fakeMessages = [
  {
    id: 1,
    type: "bot",
    text: "Hi there what's your name?"
  },
  {
    id: 2,
    type: "user",
    text: "I'm Eric"
  }
]

class App extends Component {
  state = {
    messages: fakeMessages,
  }

  sendMessage = message => {
    console.log(message)
    this.setState({ messages: [...this.state.messages, message] })
  }

  render() {
    return (
      <div className="App">
        <div className="container-fluid">
          <div className="row">
            <div className="col-4 left">
              hi
            </div>
            <div className="col-8 right">
              <div className="app__top-div">
                <MessageList messages={this.state.messages} />
              </div>
              <div className="app__bottom-div">
                <MessageForm sendMessage={this.sendMessage} />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
