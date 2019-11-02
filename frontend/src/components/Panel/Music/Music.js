import React, { Component } from 'react';
import './Music.css';
import { Tooltip, Rate } from 'antd';

class Music extends Component {
  render() {
    const { Poster, Title, Year, Genre, Director, Plot, Rated, imdbRating, BoxOffice } = this.props.activeMessage.musicInfo;

    return (
      <div className="music__container">
        <div className="music__container">
          <div className="music__poster--container">
            <img className="music__poster" src={Poster} alt=""/>
          </div>
          <div className="music__musicTitle">{Title} ({Year})</div>
          <Tooltip title={<span>IMDB Rating: {imdbRating}/10</span>}>
            <div className="music__musicRating">
              <Rate disabled defaultValue={imdbRating / 2} />
            </div>
          </Tooltip>
          <div className="music__musicRated"><span className="bold">Rated:</span> {Rated}</div>
          <div className="music__musicGenre"><span className="bold">Genre(s):</span> {Genre}</div>
          <div className="music__musicDirector"><span className="bold">Director:</span> {Director}</div>
          <div className="music__musicDescription"><span className="bold">Description:</span> {Plot}</div>
          <div className="music__musicBoxOffice"><span className="bold">Box Office:</span> {BoxOffice}</div>
        </div>
      </div>
    )
  }
}

export default Music;
