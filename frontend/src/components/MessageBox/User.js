import React, { Component } from 'react';
import './User.css';

const logo = require('../../assets/userLogo.svg');

class User extends Component {
  render(){
    return(
      <div className="user__container">
        <img className="user__img" src={logo} alt="user"></img>
        <div className="user__text-wrapper">
          <div className="user__name">User</div>
          <div className="user__text">{this.props.text}</div>
        </div>
      </div>
    )
  }
}

export default User;
