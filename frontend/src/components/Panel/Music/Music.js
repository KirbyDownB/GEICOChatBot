import React, { Component } from 'react';
import './Music.css';

class Music extends Component {
  render() {
    const { Artist, Song, Year, Album, AlbumArt, Record, Genre } = this.props.musicInfo;

    return (
      <div className="music__container">
        <div className="music__container">
          <div className="music__albumArt--container">
            <img className="music__albumArt" src={AlbumArt} alt=""/>
          </div>
          <div className="music__caption music__musicTitle">{Song} ({Year})</div>
          <div className="music__caption music__musicArtist"><span className="bold">Artist:</span> {Artist}</div>
          <div className="music__caption music__musicAlbum"><span className="bold">Album:</span> {Album}</div>
          <div className="music__caption music__musicGenre"><span className="bold">Genre(s):</span> {Genre}</div>
          <div className="music__caption music__musicRecord"><span className="bold">Record:</span> {Record}</div>
        </div>
      </div>
    )
  }
}

export default Music;
