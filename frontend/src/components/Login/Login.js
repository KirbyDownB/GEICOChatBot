import React, { Component } from 'react';
import './Login.css';
import { Input, Form, Icon, Button } from 'antd';
import { BASE_URL, showMessage, CREDENTIALS_ERROR, FORGOT_ERROR } from '../../constants';

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
      showMessage(FORGOT_ERROR);
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
      .then(response => response.status !== 200 ? Promise.reject() : response.json())
      .then(data => {
        console.log("Successfully logged in with data", data)
        const { token } = data;
        this.props.setToken(token);
        this.setState({ isLoginLoading: false });
      })
      .catch(error => {
        console.log("I got an error in Login", error);
        console.error(error);
        this.setState({ isLoginLoading: false });
        showMessage(CREDENTIALS_ERROR);
      })
  }

  handleShowSignup = () => {
    this.props.showSignup();
  }

  render() {
    return (
      <div className="login__container">
        <div className="login__title">LOGIN</div>
        <Form onSubmit={this.handleLoginSubmit}>
          <Item>
            <div className="login__caption">Username</div>
            <Input
              className="login__input"
              placeholder="Username"
              name="username"
              prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
            />
          </Item>
          <Item>
            <div className="login__caption">Password</div>
            <Input
              className="login__input"
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
                loading={this.state.isLoginLoading}
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
                onClick={this.handleShowSignup}
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