import React, { Component } from 'react';
import './Music.css';
import { Modal } from 'antd';
import { Radar } from 'react-chartjs-2';

const options = { year: 'numeric', month: 'long', day: 'numeric' };
const convert = require('convert-seconds');

const chartOptions = {
  legend: {
    labels: {
      // This more specific font property overrides the global property
      fontFamily: 'Asap'
    }
  }
}

class Music extends Component {
  state = {
    isMusicModalOpen: false
  }

  openMusicModal = () => {
    this.setState({ isMusicModalOpen: true });
  }

  closeMusicModal = () => {
    this.setState({ isMusicModalOpen: false });
  }

  render() {
    
    const {
      name: songName,
      features,
      url,
      album: {
        name: albumName,
        release_date: date,
        artists,
        images
      },
    } = this.props.musicInfo;

    const {
      name: inputSongName,
      features: {
        acousticness: inputAcousticness,
        danceability: inputDanceability,
        energy: inputEnergy,
        liveness: inputLiveness,
        valence: inputValence
      }
    } = this.props.inputInfo;

    const { acousticness, danceability, energy, liveness, valence } = features;

    const data = {
      labels: ["Acousticness", "Danceability", "Energy", "Liveness", "Valence"],
      datasets: [
        {
          label: inputSongName,
          backgroundColor: 'rgba(179,181,198,0.2)',
          borderColor: 'rgba(179,181,198,1)',
          pointBackgroundColor: 'rgba(179,181,198,1)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(179,181,198,1)',
          data: [inputAcousticness, inputDanceability, inputEnergy, inputLiveness, inputValence]
        },
        {
          label: songName,
          backgroundColor: 'rgba(117, 151, 252,0.2)',
          borderColor: '#7597FC',
          pointBackgroundColor: '#7597FC',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: '#7597FC',
          data: [acousticness, danceability, energy, liveness, valence]
        }
      ]
    };

    return (
      <div className="music__container">
        <div className="music__container">
          <div className="music__albumArt--container">
            <a href={url} target="_blank" rel="noopener noreferrer">
              <img className="music__albumArt" src={images[0].url} alt=""/>
            </a>
          </div>
          <div className="music__caption music__musicTitle" onClick={this.openMusicModal}>{songName}</div>
          <div className="music__caption music__musicArtist"><span className="bold">Artist:</span> {artists[0].name}</div>
          <div className="music__caption music__musicAlbum"><span className="bold">Album:</span> {albumName}</div>
          <div className="music__caption music__musicRecord"><span className="bold">Published:</span> {date}</div>
        </div>
        <Modal
          centered
          className="music__modal"
          visible={this.state.isMusicModalOpen}
          onCancel={this.closeMusicModal}
          width={600}
          footer={null}
        >
          <div className="music__modal--container">
            <div className="row justify-content-center">
              <div className="col-4">
                <div className="music__albumArt--container">
                  <a href={url} target="_blank" rel="noopener noreferrer">
                    <img className="music__albumArt" src={images[0].url} alt=""/>
                  </a>
                </div>
                <div className="music__caption music__musicTitle" onClick={this.openMusicModal}>{songName}</div>
              </div>
              <div className="col-8">
                <Radar
                  data={data}
                  width={200}
                  options={chartOptions}
                />
              </div>
            </div>
          </div>
        </Modal>
      </div>
    )
  }
}

export default Music;
