import React, { Component } from 'react';
import './Panel.css';
import { Button, Icon } from 'antd';
import Movie from './Movie/Movie';
import Music from './Music/Music';

class Panel extends Component {
  state = {
    index: 0,
    savedMovies: []
  }

  handlePreviousClick = e => {
    e.preventDefault();
    this.props.handlePreviousClick();
  }

  handleNextClick = e => {
    e.preventDefault();
    this.props.handleNextClick();
  }

  handleMovieSave = imdbID => {
    this.setState({ savedMovies: [...this.state.savedMovies, imdbID] });
  }

  render() {
    const { topic } = this.props.activeMessage;
    console.log("Topic of the active message is", topic)

    let info = null;
    if (topic === "movie") {
      info = this.props.activeMessage.movieInfo;
    } else {
      info = this.props.activeMessage.music;
      console.log("assigning info", info)
    }

    return (
      <div className="panel__container">
        <div className="panel__leftButton--container">
          {this.props.activeIndex > 0 && <Button shape="circle" type="primary" onClick={this.handlePreviousClick}>
            <Icon type="caret-left" />
          </Button>}
        </div>
        {topic === "movie" && <Movie movieInfo={info[this.props.activeIndex]} savedMovies={this.state.savedMovies} handleMovieSave={this.handleMovieSave} />}
        {topic === "music" && <Music musicInfo={info.output[this.props.activeIndex]} inputInfo={info.input} />}
        <div className="panel__rightButton--container">
          {this.props.activeIndex < info.output.length - 1 && <Button shape="circle" type="primary" onClick={this.handleNextClick}>
            <Icon type="caret-right" />
          </Button>}
        </div>
      </div>
    )
  }
}

export default Panel;