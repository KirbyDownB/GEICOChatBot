import React, { Component } from 'react';
import './User.css';

const logo = require('../../assets/userLogo.svg');

class User extends Component {
  state = {
    timeStamp: ""
  }

  formatAMPM = (date) => {
    let hours = date.getHours();
    let minutes = date.getMinutes();
    let ampm = hours >= 12 ? 'PM' : 'AM';

    hours = hours % 12;
    hours = hours ? hours : 12;
    minutes = minutes < 10 ? '0'+minutes : minutes;

    const strTime = hours + ':' + minutes + ' ' + ampm;

    return strTime;
  }

  componentDidMount = () => {
    let date = new Date();
    this.setState({
      timeStamp: this.formatAMPM(date)
    })
  }

  render(){
    return(
      <div className="user__container">
        <img className="user__img" src={logo} alt="user"></img>
        <div className="user__text-wrapper">
          <div className="user__name">{this.props.name} {this.state.timeStamp}</div>
          <div className="user__text">{this.props.text}</div>
        </div>
      </div>
    )
  }
}

export default User;
