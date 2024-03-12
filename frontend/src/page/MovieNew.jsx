import React from "react";
import NavbarNew from "../components/NavbarNew";
import { ReactComponent as Star } from "../assets/Star_fill.svg"
import { Rating, Stack } from "@mui/material";
import { ReactComponent as User } from "../assets/User_fill.svg"
import { ReactComponent as UserAdd } from "../assets/User_add_alt.svg"
import { ReactComponent as Ban } from "../assets/Cancel.svg"
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { TokenContext } from '../context/TokenContext'
import { ReactComponent as Filter } from "../assets/filter.svg"
import MovieCard from "../components/MovieCardNew";

const RatingAndHeart = (props) => {
  return (
    <div>
      <div className="rowCenter">
        <Star />
        <span className="movieText">{props.star}/5</span>
      </div>
    </div>
  )
}

const MovieHeader = (props) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', rowGap: 30 }}>
      <div className="movieTitle" style={{ margin: 0, fontSize: 60 }}>
        {props.name}
      </div>
      <div className="rowCenter" style={{ margin: 0 }}>
        <div className="movieSubtitle">year:</div>
        <div className="movieInfo">{props.year}</div>
        <div className="movieSubtitle">country:</div>
        <div className="movieInfo">{props.country}</div>
        <div className="movieSubtitle">language:</div>
        <div className="movieInfo">{props.language}</div>
      </div>
    </div>
  )
}

const Divider = () => {
  return (
    <div style={{ width: '60vw', borderBottom: '5px solid white', marginTop: 20, marginBottom: 20 }} />
  )
}

const MovieIntroduction = (props) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', rowGap: 20 }}>
      <div>
        <div className="movieText" style={{ width: '60vw', fontSize: 24 }}>
          {props.description}
        </div>
        <Divider />
        <div className="row" >
          <div className="movieText" style={{ fontWeight: 700, fontSize: 24 }}>
            Director:
          </div>
          {
            props.director.map((dir, index) => {
              return (
                <div className="movieText" index={index} style={{ fontSize: 24 }}>
                  {dir}
                </div>
              )
            })
          }
        </div>
        <Divider />
        <div className="row" style={{ width: '60vw' }}>
          <div className="movieText" style={{ fontWeight: 700, fontSize: 24 }}>
            Stars:
          </div>
          {
            props.actor.map((dir, index) => {
              return (
                <div className="movieText" index={index} style={{ fontSize: 24 }}>
                  {dir}
                </div>
              )
            })
          }
        </div>
      </div>
      <CommentReady reviews={props.reviews} />
    </div>
  )
}

const MovieGenre = (props) => {
  return (
    <div>
      {
        props.genres.map((genre, index) => {
          return (
            <div className="movieGenreButton" style={{ fontSize: 30, width: 250 }} index={index}>
              {genre}
            </div>
          )
        })
      }
    </div>
  )
}

const CommentReady = (props) => {
  const parts = props.reviews.map((review, index) => {
    return (
      <div key={index} style={{ width: 1003, backgroundColor: 'rgba(255, 255, 255, 0.1)', padding: 20, paddingBottom: 80, border: '1 solid #8B8787', borderRadius: 30 }}>
        <div className={'rowBetween'}>
          <div className="row" style={{ alignItems: 'center', columnGap: 10 }}>
            <User />
            <div className={"movieInfo"} style={{ fontSize: 20 }}>{review.name}</div>
            <Rating value={review.rating} readOnly />
          </div>
          <Stack direction='row' spacing={2}>
            <div style={{ cursor: 'pointer' }}>
              <UserAdd />
            </div>
            <div style={{ cursor: 'pointer' }}>
              <Ban />
            </div>
          </Stack>
        </div>
        <div className={'movieInfo'} style={{ fontSize: 20, marginTop: 20, lineHeight: 1 }}>{review.review}</div>
      </div>
    )
  })
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr', gridGap: 10 }} >
      {parts}
    </div>
  )
}

function MovieNew() {
  const [name, setName] = React.useState('');
  const [description, setDescription] = React.useState('');
  const [genre, setGenre] = React.useState([]);
  const [director, setDirector] = React.useState([]);
  const [actor, setActor] = React.useState([]);
  const [year, setYear] = React.useState(0);
  const [star, setStar] = React.useState(0);
  const [image, setImage] = React.useState('');
  const [country, setCountry] = React.useState('');
  const [language, setLanguage] = React.useState('');
  const [reviews, setReviews] = React.useState([]);
  const { id } = useParams();
  const { token } = React.useContext(TokenContext);

  const getMovie = async () => {
    const response = await axios.get(`http://127.0.0.1:9002/movie/${id}`,
      {
        headers: {
          'Authorization': `Bearer ${token || 'None'}`,
        }
      }
    )
    const res = await axios.get(`http://127.0.0.1:9002/review/get_rating/${id}`,
      {
        headers: {
          'Authorization': `Bearer ${token || 'None'}`,
        }
      }
    )
    console.log(response)
    setName(response.data.name);
    setDescription(response.data.description);
    setGenre(response.data.genre);
    setDirector(response.data.Director);
    setActor(response.data.Actor);
    setStar(parseFloat(res.data.rating).toFixed(1));
    setImage(response.data.movie_photo);
    setYear(response.data.year);
    setCountry(response.data.country);
    setLanguage(response.data.language);
  }

  const getReviews = async () => {
    const results = [];
    const res = await axios.get(`http://127.0.0.1:9002/review/get_comments/${id}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });
    if (res.data && res.data.review_id) {
      for (let i = 0; i < res.data.review_id.length; i++) {
        const review = await axios.get(`http://127.0.0.1:9002/review/get_comments/${id}/${res.data.review_id[i]}`,
          {
            headers: {
              'Authorization': `Bearer ${token}`,
            }
          })
        results.push({
          name: review.data.user_name,
          rating: review.data.rating,
          review: review.data.review,
        })
      }
      setReviews(results);
    }
  }

  React.useEffect(() => {
    getMovie();
  }, [])


  React.useEffect(() => {
    getReviews();
  }, [])

  const Recommendation = () => {
    const [movies, setMovies] = React.useState([])
    const [sortedBy, setSortedby] = React.useState("genre")
    const getMovies = async () => {
      const res = await axios.get(`http://127.0.0.1:9002/recommend/${sortedBy}/${id}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        });
      // console.log(res.data["similar movies"])
      const tmp = []
      for (let i = 0; i < res.data["similar movies"].length; i++) {
        const response = await axios.get(`http://127.0.0.1:9002/movie/${res.data["similar movies"][i]}`,
          {
            headers: {
              'Authorization': `Bearer ${token || 'None'}`,
            }
          }
        )
        const data = {
          name: response.data.name,
          image: response.data.movie_photo,
          id: response.data.id
        }
        tmp.push(data)
      }
      setMovies(tmp)
    }

    React.useEffect(() => {
      getMovies()
    }, [sortedBy])

    const RecommendMovies = () => {
      const parts = movies.map((movie, index) => {
        return (
          <MovieCard
            name={movie.name}
            img={movie.image}
            id={movie.id}
            key={index}
          // popup={handlePopupOpen}
          />
        )
      })
      return (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gridGap: 30, borderRadius: 15 }} >
          {parts}
        </div>
      )
    }

    return (
      <div style={{ display: 'flex', justifyContent: 'flex-start', flexDirection: 'column', rowGap: 30 }}>
        <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', width: '40vw', alignItems: 'center', columnGap: 20 }}>
          <div className="movieText" style={{ fontSize: 30, width: 300, paddingRight: 20, borderRight: '1px solid white' }}>Similar films</div>
          <Filter />
          <div className="blackButton" style={{ width: 150, height: 50 }} onClick={() => { setSortedby("history") }}>History</div>
          <div className="blackButton" style={{ width: 150, height: 50 }} onClick={() => { setSortedby("genre") }}>Genre</div>
          <div className="blackButton" style={{ width: 150, height: 50 }} onClick={() => { setSortedby("director") }}>Director</div>
        </div>
        <RecommendMovies />
      </div>
    )
  }

  return (
    <div>
      <NavbarNew searchBar />
      <div className="contentBody" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', rowGap: 30 }}>
        <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', width: '90vw' }}>
          <MovieHeader name={name} year={year} language={language} country={country} />
          <RatingAndHeart star={star} />
        </div>
        <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-evenly', backgroundColor: 'rgba(255, 255, 255, 0.1)', padding: 20, borderRadius: 35, width: '90vw', columnGap: 20 }}>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <img src={`data:image/jpeg;base64,${image}`} className={'cardImage'} />
            <MovieGenre genres={genre} />
          </div>
          <MovieIntroduction description={description} director={director} actor={actor} reviews={reviews} />
        </div>
        <div style={{ display: 'flex', justifyContent: 'flex-start', width: '100%', marginLeft: 70 }}>
          <Recommendation />
        </div>
      </div>
    </div>
  )
}

export default MovieNew;
