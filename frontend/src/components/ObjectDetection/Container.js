import React, { Component } from 'react';
import P5Wrapper from 'react-p5-wrapper';
import objectDetectionSketch from './ObjectDetectionSketch';
import { Switch } from 'antd';
import './Container.css'

export default class AppContainer extends Component {

    handleExpression = (value) => {
      if (value.angry){
        this.props.setExpressions(value);
        console.log(value)
      }      // fetch("",{
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
      console.log(value)
    }

    render() {
        return (
          <div>
            <div style={{display: 'none'}}>
              <P5Wrapper sketch={objectDetectionSketch} handleExpression={this.handleExpression}/>
            </div>
          </div>
        )
    }
}
