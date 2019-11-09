import React, { Component } from 'react';
import './Panel.css';
import { Button, Icon } from 'antd';
import Movie from './Movie/Movie';
import Music from './Music/Music';
import { BASE_URL, tokenKeyName, showMessage, REQUEST_ERROR } from '../../../constants';

class Panel extends Component {
  state = {
    index: 0,
    savedMovies: [],
    savedMusic: []
  }

  componentDidMount = () => {
    const token = localStorage.getItem(tokenKeyName);
    if (token) {
      console.log("Hitting get saved items")
      fetch(`${BASE_URL}/api/get_saved_items`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + token
        }
      })
        .then(response => response.status !== 200 ? Promise.reject() : response.json())
        .then(data => {
          console.log("Got saved items in componentDidMount", data);
          const { movieInfo: savedMovies, savedSongs: savedMusic } = data;
          this.setState({ savedMovies, savedMusic });
        })
        .catch(error => {
          showMessage(REQUEST_ERROR);
        });
    }
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
    const token = localStorage.getItem(tokenKeyName);
    if (token) {
      fetch(`${BASE_URL}/api/save_movie`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
          "imdbID": imdbID
        })
      })
        .then(response => response.status !== 200 ? Promise.reject() : response.json())
        .then(data => {
          console.log("Successfully saved movie with response", data);
          this.setState({ savedMovies: [...this.state.savedMovies, imdbID] });
        })
        .catch(error => {
          showMessage(REQUEST_ERROR);
        });
    }
  }

  handleMusicSave = spotifyID => {
    const token = localStorage.getItem(tokenKeyName);
    if (token) {
      fetch(`${BASE_URL}/api/save_song`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
          "songID": spotifyID
        })
      })
        .then(response => response.status !== 200 ? Promise.reject() : response.json())
        .then(data => {
          console.log("Successfully saved music with response", data);
          this.setState({ savedMusic: [...this.state.savedMusic, spotifyID] });
        })
        .catch(error => {
          showMessage(REQUEST_ERROR);
        });
    }
  }

  render() {
    const { topic } = this.props.activeMessage;

    let info = null;
    let musicInputInfo = null;
    if (topic === "movie") {
      info = this.props.activeMessage.movieInfo;
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
        {topic === "movie" && <Movie movieInfo={info[this.props.activeIndex]} savedMovies={this.state.savedMovies} handleMovieSave={this.handleMovieSave} emotion={this.props.emotion} />}
        {topic === "music" && <Music musicInfo={info[this.props.activeIndex]} savedMusic={this.state.savedMusic} handleMusicSave={this.handleMusicSave} inputInfo={musicInputInfo} />}
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
