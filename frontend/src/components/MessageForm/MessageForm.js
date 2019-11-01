import React, { Component } from 'react';
import "./MessageForm.css";
import { Form, Input, Button } from 'antd';

const { Item } = Form;

class MessageForm extends Component {
  state = {
    message: ""
  }

  handleChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  }

  handleSubmit = e => {
    e.preventDefault();

    const message = e.target.message.value;
    this.props.sendMessage(message);
  }

  render() {
    return (
      <div className="messageForm__container">
        <Form layout="inline" onSubmit={this.handleSubmit}>
          <Item>
            <Input
              value={this.state.message}
              name="message"
              className="messageForm__message"
              onChange={this.handleChange}
              placeholder="Enter your message..."
            />
          </Item>
          <Item>
            <Button
              type="primary"
              htmlType="submit"
            >
              Submit
            </Button>
          </Item>
        </Form>
      </div>
    )
  }
}

export default MessageForm;
