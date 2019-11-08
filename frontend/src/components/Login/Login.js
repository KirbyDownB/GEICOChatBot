import React, { Component } from 'react';
import './Login.css';
import { Input, Form, Icon, Button } from 'antd';
import { BASE_URL } from '../../constants';

const { Item } = Form;

class Login extends Component {
  state = {
    isLoginLoading: false
  }

  handleLoginSubmit = e => {
    e.preventDefault();

    const username = e.target.username.value;
    const password = e.target.password.value;

    if (!username || !password) {
      alert("You forgot to enter something!");
      return;
    }

    this.setState({ isLoginLoading: true });

    fetch(`${BASE_URL}/api/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        "username": username,
        "password": password
      })
    })
      .then(response => response.json())
      .then(data => {
        const { token, Message } = data;
        this.props.setLoginToken(token);
        this.setState({ isLoginLoading: false });
      })
      .catch(error => {
        console.error(error);
        this.setState({ isLoginLoading: false });
      })
  }

  render() {
    return (
      <div className="login__container">
        <div className="login__title">Login</div>
        <Form onSubmit={this.handleLoginSubmit}>
          <Item>
            <Input
              placeholder="Username"
              name="username"
              prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
            />
          </Item>
          <Item>
            <Input
              placeholder="Password"
              name="password"
              type="password"
              prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
            />
          </Item>
          <Item>
            <div className="login__button--wrapper">
              <Button
                className="login__submit"
                type="primary"
                htmlType="submit"
              >
                LOGIN
              </Button>
            </div>
          </Item>
          <Item>
            <div className="login__signupButton--wrapper">
              <Button
                className="login__signup"
                type="primary"
                htmlType="submit"
                loading={this.state.isLoginLoading}
                ghost
              >
                SIGNUP
              </Button>
            </div>
          </Item>
        </Form>
      </div>
    );
  }
}

export default Login;