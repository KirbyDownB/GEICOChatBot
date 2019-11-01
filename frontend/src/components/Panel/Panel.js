import React, { Component } from 'react';
import './Panel.css';
import { Tooltip, Rate } from 'antd';

class Panel extends Component {
  render() {
    const { Poster, Title, Year, Genre, Director, Plot, Rated, imdbRating, BoxOffice } = this.props.activeMessage.movieInfo;

    return (
      <div className="panel__container">
        <div className="panel__poster--container">
          <img className="panel__poster" src={Poster} alt=""/>
        </div>
        <div className="panel__movieTitle">{Title} ({Year})</div>
        <Tooltip title={<span>IMDB Rating: {imdbRating}/10</span>}>
          <div className="panel__movieRating">
            <Rate disabled defaultValue={imdbRating / 2} />
          </div>
        </Tooltip>
        <div className="panel__movieRated"><span className="bold">Rated:</span> {Rated}</div>
        <div className="panel__movieGenre"><span className="bold">Genre(s):</span> {Genre}</div>
        <div className="panel__movieDirector"><span className="bold">Director:</span> {Director}</div>
        <div className="panel__movieDescription"><span className="bold">Description:</span> {Plot}</div>
        <div className="panel__movieBoxOffice"><span className="bold">Box Office:</span> {BoxOffice}</div>
      </div>
    )
  }
}

export default Panel;