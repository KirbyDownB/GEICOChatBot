import React, { Component } from 'react';
import MessageForm from './components/MessageForm/MessageForm';
import MessageList from './components/MessageList/MessageList';
import Results from './components/Results/Results';
import Login from './components/Login/Login';
import Signup from './components/Signup/Signup';
import Saved from './components/Saved/Saved';
import Container from './components/ObjectDetection/Container'
import objectDetectionSketch from './components/ObjectDetection/ObjectDetectionSketch';
import P5Wrapper from 'react-p5-wrapper';

import { Tooltip, Icon, message, Modal, Button, Switch, Radio } from 'antd';
import './App.css';
import { BASE_URL, tokenKeyName, showMessage, REQUEST_ERROR } from './constants';

const logo = require('./assets/logo.svg');

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
    token: null,
    toggle: true,
    activeMenuItem: "results",
    movie: "",
    expressions: null,
    currentIndex: 0,
    emotion: null
  }

  componentDidMount = () => {
    const token = localStorage.getItem(tokenKeyName);
    if (token) {
      this.setState({ token, isModalOpen: false });

      fetch(`${BASE_URL}/api/chatbot`, {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + token
        }
      })
        .then(response => response.status !== 200 ? Promise.reject() : response.json())
        .then(data => {
          this.setState({
            messages: [...this.state.messages, data],
            questionTopic: data.question,
            name: data.username
          });
        })
        .catch(error => {
          console.log("I got an error in componentDidMount", error);
          showMessage(REQUEST_ERROR);
        });
    } else {
      console.log("I don't have a token");
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
      .then(response => response.status !== 200 ? Promise.reject() : response.json())
      .then(data => {
        const botMessage = data;
        this.setState({
          isBotLoading: false,
          name,
          messages: [...this.state.messages, botMessage],
          questionTopic: data.question,
        });
      })
      .catch(error => {
        showMessage(REQUEST_ERROR);
        this.setState({ isBotLoading: false });
      });
  }

  sendMessage = message => {
    this.setState({
      messages: [...this.state.messages, message],
      isBotLoading: true
    });

    if (this.state.token) {
      console.log("Sending message with last question", this.state.questionTopic)

      fetch(`${BASE_URL}/api/chatbot`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + this.state.token
        },
        body: JSON.stringify({
          "text": message.text,
          "username": this.state.name,
          "question": this.state.questionTopic
        })
      })
        .then(response => response.status !== 200 ? Promise.reject() : response.json())
        .then(data => {
          console.log("Got data after sending message", data)
          const botMessage = data;
          this.setState({
            isBotLoading: false,
            messages: [...this.state.messages, botMessage],
            questionTopic: data.question,
          });

          if (botMessage.topic === "music" || botMessage.topic === "movie") {
            this.setState({ activeMessage: botMessage });
          }
        })
        .catch(error => {
          showMessage(REQUEST_ERROR);
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
        showMessage(REQUEST_ERROR);
        this.setState({ isBotLoading: false });
      });
  }

  handleNextClick = () => {
    this.setState({ activeIndex: this.state.activeIndex + 1 });
  }

  handlePreviousClick = () => {
    this.setState({ activeIndex: this.state.activeIndex - 1 });
  }

  setToken = token => {
    console.log("Got token", token);
    localStorage.setItem(tokenKeyName, token);
    this.setState({ token, isModalOpen: false });
    window.location.reload();
  }

  handleLogout = () => {
    localStorage.removeItem(tokenKeyName)
    this.setState({ token: null });
    window.location.reload();
  }

  onChange = () => {
    this.setState(prevState =>({
      toggle: !prevState.toggle
    }))
  }

  handleMenuChange = e => {
    const activeMenuItem = e.target.value;
    this.setState({ activeMenuItem });
  }

  showSignup = () => {
    this.setState({
      isSignupShowing: true,
      isLoginShowing: false
    });
  }

  showLogin = () => {
    this.setState({
      isSignupShowing: false,
      isLoginShowing: true
    });
  }

  setExpressions = expressions => {
    if (this.state.activeMessage && this.state.activeMessage.topic === "movie" && this.state.token) {
      const { imdbID } = this.state.activeMessage.movieInfo[this.state.currentIndex];
      console.log("I'm looking at this movie now from App", imdbID);
      console.log("This is my expression in App", expressions);

      const emotion = Object.entries(expressions).reduce((item1, item2) => item1[1] > item2[1] ? item1 : item2)[0];
      this.setState({ emotion });

      fetch(`${BASE_URL}/api/web_cam`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + this.state.token
        },
        body: JSON.stringify({
          "imdbID": imdbID,
          "expressions": expressions
        })
      })
    }
  }

  setCurrentIndex = index => {
    this.setState({ currentIndex: index });
  }

  render() {
    console.log(this.state.movie)
    return (
      <div className="App">
        <div className="container-fluid">
          <div className="row">
            <div className="col-4 left">
              <Tooltip title="Logout">
                <Button
                  onClick={this.handleLogout}
                  className="app__logout"
                >
                  <Icon type="logout" style={{ transform: "rotate(180deg)" }} />
                </Button>
              </Tooltip>
              <div className="app__logo--container">
                <img src={logo} alt=""/>
              </div>
              <Container movie={this.state.movie} setExpressions={this.setExpressions} />
              <div className="app__menu--container">
                {this.state.activeMenuItem === "results" && <Results setCurrentIndex={this.setCurrentIndex} activeMessage={this.state.activeMessage} emotion={this.state.emotion} />}
                {this.state.activeMenuItem === "saved" && <Saved />}
              </div>
              <div className="app__toggle--container">
                <Radio.Group
                  className="app__menu--group"
                  defaultValue="results"
                  buttonStyle="solid"
                  onChange={this.handleMenuChange}
                >
                  <Radio.Button value="results">Results</Radio.Button>
                  <Radio.Button value="saved">Saved</Radio.Button>
                </Radio.Group>
              </div>
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
            {this.state.isLoginShowing && <Login showSignup={this.showSignup} setToken={this.setToken}/>}
            {this.state.isSignupShowing && <Signup showLogin={this.showLogin} setToken={this.setToken} />}
          </Modal>}
        </div>
      </div>
    );
  }
}

export default App;
