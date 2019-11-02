import React, { Component } from 'react';
import './App.css';
import MessageForm from './components/MessageForm/MessageForm';
import MessageList from './components/MessageList/MessageList';
import Panel from './components/Panel/Panel';
import { message } from 'antd';
import { BASE_URL, fakeMessages } from './constants';

const logo = require('./assets/logo.svg');
const chatGroup = require('./assets/chatGroup.svg');
const ERROR_MESSAGE = "Something went wrong on our end!";

class App extends Component {
  state = {
    messages: [],
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
        console.log("I got an error in componentDidMount");
        console.error(error);
        message.error(ERROR_MESSAGE);
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
        console.log("I got an error after sending name");
        console.error(error);
        message.error(ERROR_MESSAGE);
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
          const botMessage = data;
          this.setState({
            isBotLoading: false,
            messages: [...this.state.messages, botMessage],
            questionTopic: data.question
          });
        })
        .catch(error => {
          console.log("I got an error after sending message");
          console.error(error);
          message.error(ERROR_MESSAGE);
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

  submitRadioAnswer = answer => {
    this.setState({ isBotLoading: true });

    console.log("Submitting radio answer", answer)

    fetch(`${BASE_URL}/api/chatbot`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        "text": answer,
        "username": this.state.name,
        "question": this.state.questionTopic
      })
    })
      .then(response => response.json())
      .then(data => {
        console.log("Got data after submitting radio answer", data)
        const botMessage = data;
        this.setState({
          isBotLoading: false,
          messages: [...this.state.messages, botMessage],
          questionTopic: data.question
        });
      })
      .catch(error => {
        console.error(error);
        message.error(ERROR_MESSAGE);
        this.setState({
          isBotLoading: false,
        });
      })
  }

  render() {
    return (
      <div className="App">
        <div className="container-fluid">
          <div className="row">
            <div className="col-4 left">
              <div className="app__logo--container">
                <img src={logo} alt=""/>
              </div>
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
                <MessageList submitRadioAnswer={this.submitRadioAnswer} isBotLoading={this.state.isBotLoading} messages={this.state.messages} setActiveMessage={this.setActiveMessage} name={this.state.name} />
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
