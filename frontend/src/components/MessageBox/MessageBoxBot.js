import React, { Component } from 'react';
import './MessageBoxBot.css';

const logo = require('../assets/chatBotLogo.svg');

class MessageBoxBot extends Component {

  state = {
    text: ""
  }

  render(){
    return(
      <div className="messageBox__container">
        <img className="messageBox__img" src={logo}></img>
        <div className="messageBox__text-wrapper">
          <div className="messageBox__date">Baughty</div>
          <div className="messageBox__text">Hi there! What's your name?</div>
        </div>
      </div>
    )
  }
}

export default MessageBoxBot;
