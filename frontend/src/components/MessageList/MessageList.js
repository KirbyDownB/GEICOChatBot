import React, { Component } from 'react';
import {Animated} from "react-animated-css";
import "./MessageList.css";
import Bot from '../MessageBox/Bot';
import User from '../MessageBox/User';

class MessageList extends Component {
  handleMessageClick = (e, message) => {
    e.preventDefault();

    if (message.topic !== "normal") {
      this.props.setActiveMessage(message);
    } else {
      this.props.setActiveMessage(null);
    }
  }

  componentDidUpdate = () => {
    this.node.scrollTop = this.node.scrollHeight
  }

  render() {
    return (
      <div className="messageList_wrapper">
        <div className="messageList__container" ref={(node) => (this.node = node)}>
          {this.props.messages.map(message => {
            return (
            <Animated animationIn="bounceInLeft" animationInDuration={ 500 } isVisible={true}>
              <div className="messageList__box" onClick={e => this.handleMessageClick(e, message)}>
                {message.type === "bot" ? (
                  <Bot {...message} />
                ) : (
                  <User {...message} />
                )}
              </div>
            </Animated>
            )
          })}
        </div>
      </div>
    )
  }
}

export default MessageList;
