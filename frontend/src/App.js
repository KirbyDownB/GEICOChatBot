import React, { Component } from 'react';
import MessageForm from './components/MessageForm/MessageForm';
import { Animated } from "react-animated-css";
import MessageList from './components/MessageList/MessageList';
import Panel from './components/Panel/Panel';
import Login from './components/Login/Login';
import Signup from './components/Signup/Signup';
import { message, Modal, Button } from 'antd';
import './App.css';
import { BASE_URL, tokenKeyName, fakeMessages } from './constants';

const logo = require('./assets/logo.svg');
const chatGroup = require('./assets/chatGroup.svg');
const ERROR_MESSAGE = "Something went wrong!";

const showError = () => message.error(ERROR_MESSAGE);

class App extends Component {
  state = {
    messages: [],
    activeMessage: null,
    lastMessage: null,
    name: "",
    isBotLoading: false,
    questionTopic: "",
    activeIndex: 0,
    isModalOpen: true,
    isLoginShowing: true,
    isSignupShowing: false,
    token: null
  }

  componentDidMount = () => {
    const token = localStorage.getItem(tokenKeyName);
    if (token) {
      console.log("I got a token", token);
      this.setState({ token });
      this.setState({ isModalOpen: false });

      fetch(`${BASE_URL}/api/chatbot`, {
        method: "POST"
      })
        .then(response => response.json())
        .then(data => {
          this.setState({ messages: [...this.state.messages, data], questionTopic: data.question });
        })
        .catch(error => {
          console.log("I got an error in componentDidMount", error);
          showError()
        });
    } else {
      console.log("I don't have a token")
    }
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
        showError();
        this.setState({ isBotLoading: false });
      });
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
          showError();
          this.setState({ isBotLoading: false, });
        });
    }
  }

  setActiveMessage = message => {
    console.log("setting active message", message)
    this.setState({ activeMessage: message, activeIndex: 0 });
  }

  submitRadioAnswer = answer => {
    this.setState({ isBotLoading: true });

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
        const botMessage = data;
        this.setState({
          isBotLoading: false,
          messages: [...this.state.messages, botMessage],
          questionTopic: data.question
        });
      })
      .catch(error => {
        console.error(error);
        showError();
        this.setState({ isBotLoading: false });
      });
  }

  handleNextClick = () => {
    this.setState({ activeIndex: this.state.activeIndex + 1 });
  }

  handlePreviousClick = () => {
    this.setState({ activeIndex: this.state.activeIndex - 1 });
  }

  setLoginToken = token => {
    localStorage.setItem(tokenKeyName, token);
    this.setState({ token, isModalOpen: false });
  }

  handleLogout = () => {
    localStorage.removeItem(tokenKeyName)
    this.setState({ token: null });
    window.location.reload();
  }

  render() {
    return (
      <div className="App">
        <div className="container-fluid">
          <div className="row">
            <div className="col-4 left">
              <Button
                onClick={this.handleLogout}
                className="app__logout"
              >
                LOGOUT
              </Button>
              <div className="app__logo--container">
                <img src={logo} alt=""/>
              </div>
              <Animated animationIn="fadeIn" isVisible={true}>
              {!this.state.activeMessage && <div className="app__chatGroup--inactive">
                <img className="app__chatGroup" src={chatGroup} alt=""/>
                <div className="app_chatGroup--caption">Click on a message with a <span className="bold">red</span> or <span className="bold">gold</span> chatbot icon to show more details about it!</div>
              </div>}
              {this.state.activeMessage && <div className="app__chatGroup--active">
                <Panel handleNextClick={this.handleNextClick} handlePreviousClick={this.handlePreviousClick} activeMessage={this.state.activeMessage} activeIndex={this.state.activeIndex} />
              </div>}
              </Animated>
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
          {!this.state.token && <Modal
            visible={this.state.isModalOpen}
            closable={false}
            centered
            footer={null}
          >
            {this.state.isLoginShowing && <Login setLoginToken={this.setLoginToken}/>}
            {this.state.isSignupShowing && <Signup />}
          </Modal>}
        </div>
      </div>
    );
  }
}

export default App;
