import React, { Component } from 'react';
import './App.css';

import MessageForm from './components/MessageForm/MessageForm';

class App extends Component {
  state = {
    messages: []
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
              <MessageForm />
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
