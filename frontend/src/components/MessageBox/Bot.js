import React, { Component } from 'react';
import './Bot.css';

const logo = require('../../assets/chatBotLogo.svg');

class Bot extends Component {
  state = {
    timeStamp: ""
  }

  formatAMPM = (date) => {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
  }

  componentDidMount = () => {
    let date = new Date();
    this.setState({
      timeStamp: this.formatAMPM(date)
    })
  }

  render(){
    let date = new Date()
    return(
      <div className="bot__container">
        <img className="bot__img" src={logo} alt="bot"></img>
        <div className="bot__text-wrapper">
        <div className="bot__name">Baughty {this.state.timeStamp}</div>
          <div className="bot__text">{this.props.text}</div>
        </div>
      </div>
    )
  }
}

export default Bot;
