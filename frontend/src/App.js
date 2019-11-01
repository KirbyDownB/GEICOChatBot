import React, { Component } from 'react';
import './App.css';
import MessageForm from './components/MessageForm/MessageForm';
import MessageList from './components/MessageList/MessageList';
import SideInfo from './components/SideInfo/SideInfo';

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
    this.setState({ messages: [...this.state.messages, message] });
  }

  render() {
    return (
      <div className="App">
        <div className="left">
          hello
        </div>
        <div style={{width: '75vw'}}>
          <div className="app__top-div">
            <MessageList messages={this.state.messages} />
          </div>
          <div className="app__bottom-div">
            <MessageForm sendMessage={this.sendMessage} />
          </div>
        </div>
      </div>
    );
  }
}

export default App;
