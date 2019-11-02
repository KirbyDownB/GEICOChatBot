import React, { Component } from 'react';
import './Bot.css';
import { Radio } from 'antd';

const { Group } = Radio;
const botLogo = require('../../assets/chatBotLogo.svg');
const movieBotLogo = require('../../assets/movieBotLogo.svg');
const musicBotLogo = require('../../assets/musicBotLogo.svg');

const radioStyle = {
  display: 'block',
  height: '25px',
  lineHeight: '30px',
};

class Bot extends Component {
  state = {
    timeStamp: "",
    answer: null,
    isAnswerSelected: false
  }

  formatAMPM = (date) => {
    let hours = date.getHours();
    let minutes = date.getMinutes();
    let ampm = hours >= 12 ? 'PM' : 'AM';

    hours = hours % 12;
    hours = hours ? hours : 12;
    minutes = minutes < 10 ? '0'+minutes : minutes;

    const strTime = hours + ':' + minutes + ' ' + ampm;

    return strTime;
  }

  componentDidMount = () => {
    let date = new Date();
    this.setState({ timeStamp: this.formatAMPM(date) });
  }

  handleChooseAnswer = e => {
    const answer = e.target.value;
    this.setState({ isAnswerSelected: true });
    this.props.sendRadioAnswer(answer);
  }

  render(){
    let logo = botLogo;
    let cursorType = "default";
    let messageMarginTop = "auto";
    let messageMarginBottom = "auto";

    if (this.props.topic === "movie") {
      logo = movieBotLogo;
      cursorType = "pointer";
    } else if (this.props.topic === "music") {
      logo = musicBotLogo;
      cursorType = "pointer";
    } else if (this.props.topic === "questions") {
      if (this.props.options.length === 3) {
        messageMarginTop = "-40px";
      } else {
        messageMarginTop = "-10px"
      }
      messageMarginBottom = "35px";
    }

    return(
      <div className="bot__container" style={{ cursor: cursorType, marginBottom: messageMarginBottom }}>
        <img className="bot__img" src={logo} alt="bot" style={{ marginTop: messageMarginTop }}></img>
        <div className="bot__text-wrapper">
        <div className="bot__name">Baut {this.state.timeStamp}</div>
          <div className="bot__text">{this.props.text}</div>
          {this.props.options && <Group onChange={this.handleChooseAnswer} disabled={this.state.isAnswerSelected}>
            {this.props.options.map(option => {
              return <Radio className="bot__option" style={radioStyle} value={option}>{option}</Radio>
            })}
          </Group>}
        </div>
      </div>
    )
  }
}

export default Bot;
