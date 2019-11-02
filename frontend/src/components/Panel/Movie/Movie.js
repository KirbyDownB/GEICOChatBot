import React, { Component } from 'react';
import './Movie.css';

const imdbLogo = require('../../../assets/imdb.svg');

class Movie extends Component {
  render() {
    const { Poster, Title, Year, Genre, Director, Plot, Rated, imdbRating, BoxOffice, Actors } = this.props.movieInfo;

    return (
      <div className="movie__container">
        <div className="movie__container">
          <div className="movie__poster--container">
            <img className="movie__poster" src={Poster} alt=""/>
          </div>
          <div className="movie__caption movie__movieTitle">{Title} ({Year})</div>
          <div className="movie__imdb--container">
            <img className="movie__imdb" src={imdbLogo} alt="imdb"/>
            <div className="movie__imdb--rating">{imdbRating}/10</div>
          </div>
          <div className="movie__caption movie__movieRated"><span className="bold">Rated:</span> {Rated}</div>
          <div className="movie__caption movie__movieGenre"><span className="bold">Genre(s):</span> {Genre}</div>
          <div className="movie__caption movie__movieDirector"><span className="bold">Director:</span> {Director}</div>
          <div className="movie__caption movie__movieActors"><span className="bold">Actor(s):</span> {Actors}</div>
          <div className="movie__caption movie__movieDescription"><span className="bold">Description:</span> {Plot}</div>
          <div className="movie__caption movie__movieBoxOffice"><span className="bold">Box Office:</span> {BoxOffice}</div>
        </div>
      </div>
    )
  }
}

export default Movie;
