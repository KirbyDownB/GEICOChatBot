import React, { Component } from 'react';
import "./MessageList.css";
import Bot from '../MessageBox/Bot';
import User from '../MessageBox/User';

class MessageList extends Component {
  render() {
    return (
      <div className="messageList__container">
        {this.props.messages.map(message => {
          return (
            <div>
              {message.type === "bot" ? (
                <Bot {...message} />
              ) : (
                <User {...message} />
              )}
            </div>
          )
        })}
      </div>
    )
  }
}

export default MessageList;