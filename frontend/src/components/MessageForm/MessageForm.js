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

    const message = {
      type: "user",
      text: e.target.text.value,
      topic: "normal",
      id: 2
    };

    this.props.sendMessage(message);
    this.setState({
      text: ""
    });

  }

  render() {
    return (
      <div className="messageForm__container">
        <Form layout="inline" onSubmit={this.handleSubmit}>
          <Item>
            <Input
              value={this.state.text}
              name="text"
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
