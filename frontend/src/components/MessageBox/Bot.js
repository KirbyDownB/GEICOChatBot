import React, { Component } from 'react';
import './Bot.css';

const logo = require('../../assets/chatBotLogo.svg');

class Bot extends Component {
  render(){
    return(
      <div className="bot__container">
        <img className="bot__img" src={logo} alt="bot"></img>
        <div className="bot__text-wrapper">
          <div className="bot__name">Baughty</div>
          <div className="bot__text">Hi there! What's your name?</div>
        </div>
      </div>
    )
  }
}

export default Bot;
