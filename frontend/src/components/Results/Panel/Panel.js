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

    let info = null;
    let musicInputInfo = null;
    if (topic === "movie") {
      info = this.props.activeMessage.movieInfo;
      // console.log("Got the movie info in activeMessage", info)
      this.props.handleMovie(info[this.props.activeIndex]);
    } else {
      info = this.props.activeMessage.music.output;
      musicInputInfo = this.props.activeMessage.music.input;
    }
    return (
      <div className="panel__container">
        <div className="panel__leftButton--container">
          {this.props.activeIndex > 0 && <Button shape="circle" type="primary" onClick={this.handlePreviousClick}>
            <Icon type="caret-left" />
          </Button>}
        </div>
        {topic === "movie" && <Movie movieInfo={info[this.props.activeIndex]} savedMovies={this.state.savedMovies} handleMovieSave={this.handleMovieSave} />}
        {topic === "music" && <Music musicInfo={info[this.props.activeIndex]} inputInfo={musicInputInfo} />}
        <div className="panel__rightButton--container">
          {this.props.activeIndex < info.length - 1 && <Button shape="circle" type="primary" onClick={this.handleNextClick}>
            <Icon type="caret-right" />
          </Button>}
        </div>
      </div>
    )
  }
}

export default Panel;
