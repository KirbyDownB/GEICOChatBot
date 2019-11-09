import React, { Component } from 'react';
import './Movie.css';
import { Modal, Icon, Tooltip } from 'antd';
import { chooseEmoji } from '../../../../constants';


const imdbLogo = require('../../../../assets/imdb.svg');

class Movie extends Component {
  state = {
    isMovieModalOpen: false
  }

  openMovieModal = () => {
    this.setState({ isMovieModalOpen: true });
  }

  closeMovieModal = () => {
    this.setState({ isMovieModalOpen: false });
  }

  handleMovieLike = () => {
    alert("You just liked", this.props.movieInfo.Title)
  }

  handleMovieDislike = () => {
    alert("You just disliked", this.props.movieInfo.Title)
  }

  handleMovieSave = (e, imdbID) => {
    e.preventDefault();
    this.props.handleMovieSave(imdbID);
  }

  render() {
    console.log("Got movie info props", this.props.movieInfo);
    console.log("Movie state", this.state)
    const { Poster, Title, Year, Genre, Director, Plot, Rated, imdbRating, BoxOffice, Actors, imdbID } = this.props.movieInfo;

    return (
      <div className="movie__container">
        <div className="movie__container">
          <div className="movie__poster--container">
            <img className="movie__poster" src={Poster} alt=""/>
          </div>
          <div className="movie__caption movie__movieTitle" onClick={this.openMovieModal}>{Title} ({Year})</div>
          <div className="movie__imdb--container">
            <img className="movie__imdb" src={imdbLogo} alt="imdb"/>
            <div className="movie__imdb--rating">{imdbRating}/10</div>
          </div>
          <div className="movie__save--container">
            <Tooltip title="Save">
              <Icon
                className="movie__save"
                type="star"
                theme={this.props.savedMovies.includes(imdbID) ? "filled" : "outlined"}
                onClick={e => this.handleMovieSave(e, imdbID)}
                style={{ fontSize: "20px" }}
              />
            </Tooltip>
          </div>
          <div className="movie__emoji--container">
            {this.props.emotion && <div className="movie__emoji">
              {chooseEmoji(this.props.emotion)}
            </div> }
          </div>
        </div>
        <Modal
          centered
          className="movie__modal"
          visible={this.state.isMovieModalOpen}
          onCancel={this.closeMovieModal}
          width={600}
          footer={null}
        >
          <div className="movie__modal--container">
            <div className="row justify-content-center">
              <div className="col-6">
                <div className="movie__modalPoster--container">
                  <img className="movie__modal--poster" src={Poster} alt=""/>
                </div>
                <div className="movie__caption movie__modal--movieTitle">{Title} ({Year})</div>
                <div className="movie__modalImdb--container">
                  <img className="movie__modal--imdb" src={imdbLogo} alt="imdb"/>
                  <div className="movie__modalImdb--rating">{imdbRating}/10</div>
                </div>
              </div>
              <div className="col-6">
                <div className="movie__caption movie__modal--movieRated"><span className="bold">Rated:</span> {Rated}</div>
                <div className="movie__caption movie__modal--movieGenre"><span className="bold">Genre(s):</span> {Genre}</div>
                <div className="movie__caption movie__modal--movieDirector"><span className="bold">Director:</span> {Director}</div>
                <div className="movie__caption movie__modal--movieActors"><span className="bold">Actor(s):</span> {Actors}</div>
                <div className="movie__caption movie__modal--movieDescription"><span className="bold">Description:</span> {Plot}</div>
                <div className="movie__caption movie__modal--movieBoxOffice"><span className="bold">Box Office:</span> {BoxOffice}</div>
              </div>
            </div>
          </div>
        </Modal>
      </div>
    )
  }
}

export default Movie;
