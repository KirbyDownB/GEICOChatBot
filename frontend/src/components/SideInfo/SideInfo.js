import React, { Component } from 'react';
import { Icon } from 'antd';
import './SideInfo.css';

class SideInfo extends Component {
  state = {
    genre: "",
    director: "",
  }
  render(){
    return(
      <div>
        <div className="SideInfo__movie-container">
        </div>
        <div>
          <h1 className="SideInfo__movie-title">Aditya Acharya</h1>
          <Icon style={{fontSize: '20px'}} type="star" theme="twoTone" twoToneColor="#eb2f96"/>
          <div style={{display: 'flex'}}>
            <h4 className="SideInfo__sub-text">Genre:</h4>
            <h4 className="SideInfo__sub-text2">Spooky</h4>
          </div>
          <div style={{display: 'flex'}}>
            <h4 className="SideInfo__sub-text">Director:</h4>
            <h4 className="SideInfo__sub-text2">Eric Ong</h4>
          </div>
        </div>
      </div>
    )
  }
}

export default SideInfo;
