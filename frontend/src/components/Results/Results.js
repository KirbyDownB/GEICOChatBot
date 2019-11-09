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
    const updatedIndex = this.state.activeIndex + 1;
    this.setState({ activeIndex: updatedIndex });
    this.props.setCurrentIndex(updatedIndex);
  }

  handlePreviousClick = () => {
    const updatedIndex = this.state.activeIndex - 1;
    this.setState({ activeIndex: updatedIndex });
    this.props.setCurrentIndex(updatedIndex);
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
            <Panel
              handleNextClick={this.handleNextClick}
              handlePreviousClick={this.handlePreviousClick}
              activeMessage={this.props.activeMessage}
              activeIndex={this.state.activeIndex}
              emotion={this.props.emotion}
            />
          </div>}
        </Animated>
      </div>
    )
  }
}

export default Results;
