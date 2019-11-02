import React, { Component } from 'react';
import './Music.css';
import { Tag } from 'antd';

const options = { year: 'numeric', month: 'long', day: 'numeric' };
const convert = require('convert-seconds');

class Music extends Component {
  render() {
    const { Artist, Song, Album, AlbumArt, Genre, Duration, Stream, TopTags, Published, Summary } = this.props.musicInfo;
    const date = new Date(Published);
    const { minutes, seconds } = convert(Duration);

    return (
      <div className="music__container">
        <div className="music__container">
          <div className="music__albumArt--container">
            <a href={Stream} target="_blank" rel="noopener noreferrer">
              <img className="music__albumArt" src={AlbumArt} alt=""/>
            </a>
          </div>
          <div className="music__caption music__musicTitle">{Song}</div>
          {TopTags.length > 0 && <div className="music__musicTags--container">
            {TopTags.map(({ name }) => {
              return <Tag color="geekblue">{name}</Tag>
            })}
          </div>}
          <div className="music__caption music__musicDuration"><span className="bold">Duration:</span> {minutes}min {seconds}s</div>
          <div className="music__caption music__musicArtist"><span className="bold">Artist:</span> {Artist}</div>
          <div className="music__caption music__musicAlbum"><span className="bold">Album:</span> {Album}</div>
          <div className="music__caption music__musicGenre"><span className="bold">Genre(s):</span> {Genre}</div>
          <div className="music__caption music__musicRecord"><span className="bold">Published:</span> {date.toLocaleDateString("en-US", options)}</div>
          {/* <div className="music__caption music__musicSummary"><span className="bold">Summary:</span> {Summary}</div> */}
        </div>
      </div>
    )
  }
}

export default Music;
