import React, { Component } from 'react';
import './Music.css';
import { Tag } from 'antd';

const options = { year: 'numeric', month: 'long', day: 'numeric' };
const convert = require('convert-seconds');

class Music extends Component {
  render() {
    console.log("Got music", this.props.musicInfo)
    const {
      name: songName,
      features,
      album: {
        external_urls: {
          spotify
        },
        name: albumName,
        release_date: date,
        artists,
        images
      },
    } = this.props.musicInfo;

    console.log("images", images[0])
    // const { name: songName, features, album: { name: albumName, external_urls: stream, release_date: date, artists, images, } } = this.props.musicInfo.info;
    // const date = new Date(Published);
    // const { minutes, seconds } = convert(Duration);

    return (
      <div className="music__container">
        <div className="music__container">

          <div className="music__albumArt--container">
            <a href={spotify} target="_blank" rel="noopener noreferrer">
              <img className="music__albumArt" src={images[0].url} alt=""/>
            </a>
          </div>
          <div className="music__caption music__musicTitle">{songName}</div>
          <div className="music__caption music__musicArtist"><span className="bold">Artist:</span> {artists[0].name}</div>
          <div className="music__caption music__musicAlbum"><span className="bold">Album:</span> {albumName}</div>
          <div className="music__caption music__musicRecord"><span className="bold">Published:</span> {date}</div>
        </div>
      </div>
    )
  }
}

export default Music;
