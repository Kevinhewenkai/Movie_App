import React from "react";
import Navbar from "../components/NavbarNew";
import { useParams } from "react-router-dom";
import { TokenContext } from '../context/TokenContext'
import axios from "axios";
import MovieCard from "../components/MovieCardNew";

function WishList() {
  const { id } = useParams();
  const [movies, setMovies] = React.useState([])
  const [name, setName] = React.useState('')
  const { token } = React.useContext(TokenContext);

  const getMovies = async () => {
    const result = [];
    const res = await axios.get(`http://127.0.0.1:9002/wishlists/list_info/${id}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      })
    setName(res.data.list_name)
    for (let i = 0; i < res.data.movies.length; i++) {
      const response = await axios.get(`http://127.0.0.1:9002/movie/${res.data.movies[i]}`,
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
    setMovies(result)
  }

  React.useEffect(() => {
    getMovies();
  }, [])

  const handleDelete = async (index, movieId) => {
    const tmp = [...movies];
    tmp.splice(index, 1);
    setMovies(tmp)
    axios.delete(`http://127.0.0.1:9002/wishlists/delete_from_wishlist/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      data: {
        'movie_id': movieId
      }
    })
  }

  const FavouriteMovies = () => {
    const parts = movies.map((movie, index) => {
      return (
        <MovieCard
          name={movie.name}
          img={movie.img}
          id={movie.id}
          key={index}
          wishlist
          delete={() => { handleDelete(index, movie.id) }}
        />
      )
    }
    )
    return (
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gridGap: 30, padding: 20, borderRadius: 15 }} >
        {parts}
      </div>
    )
  }

  return (
    <>
      <Navbar searchBar />
      <div className={'columnCenter'}>
        <div className={"contentBody"}>
          <div className={"movieText"} style={{ display: 'flex', flexDirection: 'row', alignSelf: 'flex-start', fontSize: 55, marginBottom: 30, marginLeft: 20 }}>
            {name}
          </div>
          <FavouriteMovies />
        </div>
      </div>
    </>
  )
}

export default WishList;
