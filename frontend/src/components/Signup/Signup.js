import React, { Component } from 'react';
import './Signup.css';
import { Form, Input, Icon, Button } from 'antd';
import { showMessage, PASSWORD_MATCH_ERROR } from '../../constants';

const { Item } = Form;

class Signup extends Component {
  state = {
    isSignupLoading: false
  }

  handleSignup = e => {
    e.preventDefault();

    const username = e.target.username.value;
    const password = e.target.password.value;
    const passwordConfirm = e.target.passwordConfirm.value;

    if (password !== passwordConfirm ) {
      showMessage(PASSWORD_MATCH_ERROR);
    }


    // Fetch request here
  }

  handleShowLogin = () => {
    this.props.showLogin();
  }

  render() {
    return (
      <div className="signup__container">
        <div className="signup__title">SIGNUP</div>
        <Form onSubmit={this.handlesignupSubmit}>
          <Item>
            <div className="signup__caption">Username</div>
            <Input
              className="signup__input"
              placeholder="Username"
              name="username"
              prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
            />
          </Item>
          <Item>
            <div className="signup__caption">Password</div>
            <Input
              className="signup__input"
              placeholder="Password"
              name="password"
              type="password"
              prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
            />
          </Item>
          <Item>
            <div className="signup__caption">Confirm Password</div>
            <Input
              className="signup__input"
              placeholder="Confirm Password"
              name="passwordConfirm"
              type="password"
              prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
            />
          </Item>
          <Item>
            <div className="signup__button--wrapper">
              <Button
                className="signup__submit"
                type="primary"
                htmlType="submit"
                loading={this.state.isSignupLoading}
              >
                SIGNUP
              </Button>
            </div>
          </Item>
        </Form>
        <div className="signup__login" onClick={this.handleShowLogin}>Already a user?</div>
      </div>
    );
  }
}

export default Signup;