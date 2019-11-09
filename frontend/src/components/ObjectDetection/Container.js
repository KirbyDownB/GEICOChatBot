import React, { Component } from 'react';
import P5Wrapper from 'react-p5-wrapper';
import objectDetectionSketch from './ObjectDetectionSketch';
import { Switch } from 'antd';
import './Container.css'

export default class AppContainer extends Component {

    state = {
      toggle: true,
      movie: ""
    }

    handleExpression = (value) => {
      if (value.angry){
        this.props.setExpressions(value);
        console.log(value)
      }
      // fetch("",{
      //   method: "POST",
      //   headers: {
      //     "Content-Type": "application/json"
      //   },
      //   body: JSON.stringify({
      //     expressions: value
      //   })
      // })
      // .then(response => response.json())
      // .catch(error => {
      //   console.log(error)
      // });
      // // this.setState({
      // //   emotion: value
      // // })
    }

    handleToggle = () => {
      this.setState(prevState => ({
        toggle: !prevState.toggle
      }))
    }


    render() {
      console.log(this.state.toggle)
        return (
          <div>
          {this.state.toggle?
            <div style={{display: 'none'}}>
              <P5Wrapper sketch={objectDetectionSketch} handleExpression={this.handleExpression}/>
            </div>:
            <div>
              <P5Wrapper sketch={objectDetectionSketch} handleExpression={this.handleExpression}/>
            </div>
          }
            <div><Switch onChange={this.handleToggle}/></div>
          </div>
        )
    }
}
