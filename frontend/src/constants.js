export const BASE_URL = "http://4771d28d.ngrok.io";

export const fakeMessages = [
  {
    id: 1,
    type: "bot",
    topic: "normal",
    text: "Hi there what's your name?"
  },
  {
    id: 2,
    type: "user",
    topic: "normal",
    text: "I'm Eric"
  },
  {
    id: 1,
    type: "bot",
    topic: "movie",
    text: "I recommend Harry Potter and the Deathly Hallows: Part 2",
    movieInfo: {
      Title: 'Harry Potter and the Deathly Hallows: Part 2',
      Year: '2011',
      Rated: 'PG-13',
      Released: '15 Jul 2011',
      Runtime: '130 min',
      Genre: 'Adventure, Drama, Fantasy, Mystery',
      Director: 'David Yates',
      Writer: 'Steve Kloves (screenplay), J.K. Rowling (novel)',
      Actors: 'Ralph Fiennes, Michael Gambon, Alan Rickman, Daniel Radcliffe',
      Plot: 'Harry, Ron, and Hermione search for Voldemort\'s remaining Horcruxes in their effort to destroy the Dark Lord as the final battle rages on at Hogwarts.',
      Language: 'English',
      Country: 'USA, UK',
      Awards: 'Nominated for 3 Oscars. Another 45 wins & 91 nominations.',
      Poster: 'https://m.media-amazon.com/images/M/MV5BMjIyZGU4YzUtNDkzYi00ZDRhLTljYzctYTMxMDQ4M2E0Y2YxXkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_SX300.jpg',
      Ratings: [
        {
          Source: 'Internet Movie Database',
          Value: '8.1/10'
        },
        {
          Source: 'Rotten Tomatoes',
          Value: '96%'
        },
        {
          Source: 'Metacritic',
          Value: '87/100'
        }
      ],
      Metascore: '87',
      imdbRating: '8.1',
      imdbVotes: '704,107',
      imdbID: 'tt1201607',
      Type: 'movie',
      DVD: '11 Nov 2011',
      BoxOffice: '$381,000,185',
      Production: 'Warner Bros. Pictures',
      Website: 'N/A',
      Response: 'True'
    }
  }
];