import React, { Component } from 'react';
import './App.css';
import MessageForm from './components/MessageForm/MessageForm';
import MessageList from './components/MessageList/MessageList';
import Panel from './components/Panel/Panel';
import { message } from 'antd';
import { BASE_URL, fakeMessages } from './constants';

const chatGroup = require('./assets/chatGroup.svg');

class App extends Component {
  state = {
    messages: fakeMessages,
    activeMessage: null,
    lastMessage: null,
    name: "",
    isBotLoading: false,
    questionTopic: ""
  }

  componentDidMount = () => {
    fetch(`${BASE_URL}/api/chatbot`, {
      method: "POST"
    })
      .then(response => response.json())
      .then(data => {
        this.setState({ messages: [...this.state.messages, data], questionTopic: data.question });
      })
      .catch(error => {
        message.error("Something went wrong on our end!");
        console.error(error);
      })
  }

  sendName = message => {
    const name = message.text;
    this.setState({
      messages: [...this.state.messages, message],
      isBotLoading: true
    });

    fetch(`${BASE_URL}/api/chatbot`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        "username": name,
        "question": this.state.questionTopic
      })
    })
      .then(response => response.json())
      .then(data => {
        const botMessage = data;
        this.setState({
          isBotLoading: false,
          name,
          messages: [...this.state.messages, botMessage],
          questionTopic: data.question
        });
      })
      .catch(error => {
        console.error(error);
        message.error("Something went wrong on our end!");
        this.setState({
          isBotLoading: false,
        });
      })
  }

  sendMessage = message => {
    this.setState({
      messages: [...this.state.messages, message],
      isBotLoading: true
    });

    if (this.state.name) {
      console.log("Sending with last question", this.state.questionTopic);
      fetch(`${BASE_URL}/api/chatbot`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          "text": message.text,
          "username": this.state.name,
          "question": this.state.questionTopic
        })
      })
        .then(response => response.json())
        .then(data => {
          console.log("Got data", data)
          const botMessage = data;
          this.setState({
            isBotLoading: false,
            messages: [...this.state.messages, botMessage],
            questionTopic: data.question
          });
        })
        .catch(error => {
          console.error(error);
          message.error("Something went wrong on our end!");
          this.setState({
            isBotLoading: false,
          });
        })
    }
  }

  setActiveMessage = message => {
    console.log("setting active message", message)
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
