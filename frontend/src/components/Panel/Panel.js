import React, { Component } from 'react';
import './Panel.css';
import Movie from './Movie/Movie';
import Music from './Music/Music';

class Panel extends Component {
  render() {
    const { topic } = this.props.activeMessage;

    return (
      <div className="panel__container">
        {topic === "movie" ? (
          <Movie movieInfo={this.props.activeMessage.movieInfo} />
        ) : (
          <Music musicInfo={this.props.activeMessage.musicInfo} />
        )}
      </div>
    )
  }
}

export default Panel;