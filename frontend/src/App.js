import React, { Component } from 'react';
import './App.css';

import MessageForm from './components/MessageForm/MessageForm';
import MessageBoxBot from './components/MessageBox/MessageBoxBot';
import MessageBoxUser from './components/MessageBox/MessageBoxUser';

class App extends Component {
  state = {
    messages: [],
    temp: ""
  }

  sendMessage = message => {
    this.setState({
      temp: message
    })
  }

  render() {
    return (
      <div className="App">
        <div className="container-fluid">
          <div className="row">
            <div className="col-4 left">
              hi
            </div>
            <div className="col-8 right">
              <div className="app__top-div">
                <MessageBoxBot />
                <MessageBoxUser temp={this.state.temp}/>
              </div>
              <div className="app__bottom-div">
                <MessageForm sendMessage={this.sendMessage} />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
