import React, { Component } from 'react';
import "./MessageForm.css";
import { Form, Input, Button } from 'antd';

const { Item } = Form;

class MessageForm extends Component {
  state = {
    text: ""
  }

  handleChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  }

  handleSubmit = e => {
    e.preventDefault();

    const text = e.target.text.value.trim();

    if (!text) {
      this.setState({ text: "" });
      return;
    }

    const message = {
      type: "user",
      text,
      topic: "normal",
      id: 2
    };

    this.props.sendMessage(message);
    
    this.setState({ text: "" });
  }

  render() {
    return (
      <div className="messageForm__container">
        <Form layout="inline" onSubmit={this.handleSubmit}>
          <Item>
            <Input
              autoComplete="off"
              value={this.state.text}
              name="text"
              className="messageForm__message"
              onChange={this.handleChange}
              placeholder="Enter your message..."
            />
          </Item>
          <Item>
            <Button
              className="messageForm__submit"
              type="primary"
              htmlType="submit"
            >
              SUBMIT
            </Button>
          </Item>
        </Form>
      </div>
    )
  }
}

export default MessageForm;
