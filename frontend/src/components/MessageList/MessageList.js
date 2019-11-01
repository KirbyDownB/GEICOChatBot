import React, { Component } from 'react';
import {Animated} from "react-animated-css";
import "./MessageList.css";
import Bot from '../MessageBox/Bot';
import User from '../MessageBox/User';

class MessageList extends Component {

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
              <div>
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
