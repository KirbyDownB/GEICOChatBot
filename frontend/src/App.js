import React, { Component } from 'react';
import './App.css';
import MessageForm from './components/MessageForm/MessageForm';
import MessageList from './components/MessageList/MessageList';
import Panel from './components/Panel/Panel';
import { fakeMessages } from './constants';

const chatGroup = require('./assets/chatGroup.svg');

class App extends Component {
  state = {
    messages: fakeMessages,
    activeMessage: null
  }

  sendMessage = message => {
    this.setState({ messages: [...this.state.messages, message] });
  }

  setActiveMessage = message => {
    this.setState({ activeMessage: message });
  }

  render() {
    console.log("active message", this.state.activeMessage);

    return (
      <div className="App">
        <div className="container-fluid">
          <div className="row">
            <div className="col-4 left">
              {!this.state.activeMessage && <div className="app__chatGroup--inactive">
                <img className="app__chatGroup" src={chatGroup} alt=""/>
                <div className="app_chatGroup--caption">Click on a message to show more details about it!</div>
              </div>}
              {this.state.activeMessage && <div className="app__chatGroup--active">
                <Panel activeMessage={this.state.activeMessage} />
              </div>}
            </div>
            <div className="col-8 right">
              <div className="app__top-div">
                <MessageList messages={this.state.messages} setActiveMessage={this.setActiveMessage} />
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
