import React, { Component } from 'react';
import './Movie.css';
import { Tooltip, Rate } from 'antd';

class Movie extends Component {
  render() {
    const { Poster, Title, Year, Genre, Director, Plot, Rated, imdbRating, BoxOffice } = this.props.activeMessage.movieInfo;

    return (
      <div className="movie__container">
        <div className="movie__container">
          <div className="movie__poster--container">
            <img className="movie__poster" src={Poster} alt=""/>
          </div>
          <div className="movie__movieTitle">{Title} ({Year})</div>
          <Tooltip title={<span>IMDB Rating: {imdbRating}/10</span>}>
            <div className="movie__movieRating">
              <Rate disabled defaultValue={imdbRating / 2} />
            </div>
          </Tooltip>
          <div className="movie__movieRated"><span className="bold">Rated:</span> {Rated}</div>
          <div className="movie__movieGenre"><span className="bold">Genre(s):</span> {Genre}</div>
          <div className="movie__movieDirector"><span className="bold">Director:</span> {Director}</div>
          <div className="movie__movieDescription"><span className="bold">Description:</span> {Plot}</div>
          <div className="movie__movieBoxOffice"><span className="bold">Box Office:</span> {BoxOffice}</div>
        </div>
      </div>
    )
  }
}

export default Movie;
