import axios from "axios";
import React from "react";
import MovieCard from "../components/MovieCardNew";
import Popup from "../components/Popup";
import NavbarNew from "../components/NavbarNew";
import { TokenContext } from '../context/TokenContext'
import { PopupContext } from '../context/PopupContext'
import SearchBar from "../components/SearchBar";
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';

function Dashboard() {
  const [movies, setMovies] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const { token } = React.useContext(TokenContext);
  const { popupOpen, setPopupOpen } = React.useContext(PopupContext)

  console.log(token)

  const handlePopupOpen = () => {
    setPopupOpen(!popupOpen);
  }

  const getMovies = async () => {
    const result = [];
    const res = await axios.get('http://127.0.0.1:9002/movie');
    for (let i = 0; i < res.data.movie_ids.length; i++) {
      const response = await axios.get(`http://127.0.0.1:9002/movie/${res.data.movie_ids[i]}`,
        {
          headers: {
            'Authorization': `Bearer ${token || 'None'}`,
          }
        });
      result.push({
        name: response.data.name,
        img: response.data.movie_photo,
        id: response.data.id
      })
    }
    setMovies(result);
    setLoading(false)
  }

  React.useEffect(() => {
    getMovies();
  }, [])

  const Feeds = () => {
    const parts = movies.map((movie, index) => {
      return (
        <MovieCard
          name={movie.name}
          img={movie.img}
          id={movie.id}
          key={index}
          popup={handlePopupOpen}
        />
      )
    });
    return (
      <Box sx={{ flexGrow: 1 }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gridGap: 30 }} >
          {
            parts.map((card, index) => {
              return (
                <div key={index}>
                  {card}
                </div>
              )
            })
          }

        </div>
      </Box>
    )
  }

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <CircularProgress size={500} />
      </div>
    )
  }

  return (
    <>
      <NavbarNew />
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', rowGap: 20, marginTop: 50 }}>
        <div className='title'>
          Delphinus
        </div>
        <SearchBar />
        <Feeds />
        {popupOpen &&
          <Popup
            popup={handlePopupOpen}
          />
        }
      </div>
    </>
  )
}

export default Dashboard;
