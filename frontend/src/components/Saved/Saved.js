import React, { Component } from 'react';
import './Saved.css';
import { BASE_URL, tokenKeyName } from '../../constants';
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
        .then(response => response.json())
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

  render() {
    return (
      <div className="saved__container">
        {this.state.isSavedLoading ? (
          <div className="saved__loading--container">
              <Spin indicator={antIcon} />
          </div>
        ) : (
          <div className="saved__info">
            {this.state.movies.length > 0 && <div className="saved__movies--container">
              <div className="saved__movies--header">Saved Movies</div>
              <div className="row">
                {this.state.movies.map(movie => {
                  return (
                    <div className="col-4">
                      <Tooltip title={movie.Title}>
                      	<img src={movie.Poster} alt="" className="saved__moviePoster"/>
                      </Tooltip>
                    </div>
                  )
                })}
              </div>
            </div>}
            {this.state.music.length > 0 && <div className="music--container">
              <div className="saved__music--header">Saved Music</div>
              <div className="row">
                {this.state.music.map(({ album, name }) => {
                  return (
                    <div className="col-4">
                      <Tooltip title={name}>
                        <img src={album.images[0].url} alt="" className="saved__musicAlbum"/>
                      </Tooltip>
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