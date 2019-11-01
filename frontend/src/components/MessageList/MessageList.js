import React, { Component } from 'react';
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

  render() {
    return (
      <div className="messageList__container">
        {this.props.messages.map(message => {
          return (
            <div className="messageList__box" onClick={e => this.handleMessageClick(e, message)}>
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