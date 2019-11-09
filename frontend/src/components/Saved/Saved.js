import React, { Component } from 'react';
import './Saved.css';
import { BASE_URL, tokenKeyName } from '../../constants';

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

      fetch(`${BASE_URL}/api/get_saved_movies`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + token
        },
      })
        .then(response => response.json())
        .then(data => {
          const { movieInfo } = data;
          this.setState({
            movies: [...this.state.movies, ...movieInfo],
            isSavedLoading: false
          });
        })
        .catch(error => {
          console.error(error);
          this.setState({ isSavedLoading: false });
        })
    }
  }

  render() {
    return (
      <div className="saved__container">
        {this.state.isSavedLoading ? (
          <div className="saved__loading--container">
            Loading...
          </div>
        ) : (
          <div className="saved__info">
            {this.state.movies.length > 0 && <div className="saved__movies--container">
              <div className="saved__movies--header">Saved Movies</div>
              <div className="row">
                {this.state.movies.map(movie => {
                  return (
                    <div className="col-4">
                      <img src={movie.Poster} alt="" className="saved__moviePoster"/>
                    </div>
                  )
                })}
              </div>
            </div>}
            {this.state.music.length > 0 && <div className="music--container">
              <div className="saved__music--header">Saved Movies</div>
              <div className="row">
                {this.state.music.map(music => {
                  return (
                    <div className="col-4">
                      <img src={music.Poster} alt="" className="saved__musicAlbum"/>
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