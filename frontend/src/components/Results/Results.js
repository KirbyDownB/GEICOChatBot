import React, { Component } from 'react';
import './Results.css';
import { Animated } from "react-animated-css";
import Panel from './Panel/Panel';
import Container from '../ObjectDetection/Container';

const chatGroup = require('../../assets/chatGroup.svg');

class Results extends Component {
  state = {
    activeIndex: 0
  }

  handleNextClick = () => {
    this.setState({ activeIndex: this.state.activeIndex + 1 });
  }

  handlePreviousClick = () => {
    this.setState({ activeIndex: this.state.activeIndex - 1 });
  }

  handleMovie = (data) => {
    console.log("I got a move in Result", data);
    this.props.handleMovie(data)
  }

  render() {
    return (
      <div className="results__container">
        <Animated animationIn="fadeIn" isVisible={true}>
          {!this.props.activeMessage && <div className="app__chatGroup--inactive">
            <img className="app__chatGroup" src={chatGroup} alt=""/>
            <div className="app_chatGroup--caption">Click on a message with a <span className="bold">red</span> or <span className="bold">gold</span> chatbot icon to show more details about it!</div>
          </div>}
          {this.props.activeMessage && <div className="app__chatGroup--active">
            <Panel handleMovie={this.handleMovie} handleNextClick={this.handleNextClick} handlePreviousClick={this.handlePreviousClick} activeMessage={this.props.activeMessage} activeIndex={this.state.activeIndex} />
          </div>}
        </Animated>
      </div>
    )
  }
}

export default Results;
