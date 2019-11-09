import React, { Component } from 'react';
import './Saved.css';
import { BASE_URL, tokenKeyName, showMessage, REQUEST_ERROR } from '../../constants';
import { Icon, Spin, Tooltip } from 'antd';

const antIcon = <Icon type="loading" style={{ fontSize: 24 }} spin />;

class Saved extends Component {
  state = {
    isSavedLoading: false,
    music: [],
    movies: []
  }

  componentDidMount = () => {
    const token = localStorage.getItem(tokenKeyName);

    if (token) {
      this.setState({ isSavedLoading: true });

      fetch(`${BASE_URL}/api/get_saved_items`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + token
        },
      })
        .then(response => response.status !== 200 ? Promise.reject() : response.json())
        .then(data => {
          const { movieInfo, savedSongs } = data;
          console.log("Got saved songs", savedSongs)
          this.setState({
            movies: [...this.state.movies, ...movieInfo],
            music: [...this.state.music, ...savedSongs],
            isSavedLoading: false
          });
        })
        .catch(error => {
          console.error(error);
          this.setState({ isSavedLoading: false });
        })
    }
  }

  handleDeleteSavedMovie = (e, imdbID) => {
    e.preventDefault();
    const token = localStorage.getItem(tokenKeyName);

    if (token) {
      fetch(`${BASE_URL}/api/delete_movie`, {
        method: "DELETE",
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
          const updatedMovies = this.state.movies.filter(movie => movie.imdbID !== imdbID);
          this.setState({ movies: updatedMovies });
        })
        .catch(error => {
          console.error(error);
          showMessage(REQUEST_ERROR);
        })
    }
  }

  handleDeleteSavedMusic = (e, spotifyID) => {
    e.preventDefault();
    const token = localStorage.getItem(tokenKeyName);

    if (token) {
      console.log("Deleting spotify id", spotifyID)
      fetch(`${BASE_URL}/api/delete_song`, {
        method: "DELETE",
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
          const updatedMusic = this.state.music.filter(song => song.id !== spotifyID);
          this.setState({ music: updatedMusic });
        })
        .catch(error => {
          console.error(error);
          showMessage(REQUEST_ERROR);
        })
    }
  }

  render() {
    console.log("Currently saved movies", this.state.movies);
    console.log("Currently saved music", this.state.music);

    return (
      <div className="saved__container">
        {this.state.isSavedLoading ? (
          <div className="saved__loading--container">
              <Spin indicator={antIcon} />
          </div>
        ) : (
          <div className="saved__info">
            {this.state.movies.length === 0 && this.state.music.length === 0 && <div className="saved__empty">
              You don't have any saved movies and/or songs yet!
            </div> }
            {this.state.movies.length > 0 && <div className="saved__movies--container">
              <div className="saved__movies--header">Saved Movies</div>
              <div className="row">
                {this.state.movies.map(({ imdbID, Title, Poster }) => {
                  const imdbURL = `https://www.imdb.com/title/${imdbID}/`;

                  return (
                    <div className="col-4 saved__movie">
                      <a href={imdbURL} target="_blank" rel="noopener noreferrer">
                        <Tooltip title={Title}>
                          <img src={Poster} alt="" className="saved__moviePoster"/>
                        </Tooltip>
                      </a>
                      <div className="remove" onClick={e => this.handleDeleteSavedMovie(e, imdbID)}>
                        <Icon type="close-circle" theme="filled" style={{ fontSize: "20px", color: "#000" }} />
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>}
            {this.state.music.length > 0 && <div className="music--container">
              <div className="saved__music--header">Saved Music</div>
              <div className="row">
                {this.state.music.map(({ album, name, external_urls: { spotify: spotifyURL }, id: spotifyID }) => {
                  return (
                    <div className="col-4 saved__music">
                      <a href={spotifyURL} target="_blank" rel="noopener noreferrer">
                        <Tooltip title={name}>
                          <img src={album.images[0].url} alt="" className="saved__musicAlbum"/>
                        </Tooltip>
                      </a>
                      <div className="remove" onClick={e => this.handleDeleteSavedMusic(e, spotifyID)}>
                        <Icon type="close-circle" theme="filled" style={{ fontSize: "20px", color: "#000" }} />
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>}
          </div>
        )}
        </div>
    )
  }
}

export default Saved;