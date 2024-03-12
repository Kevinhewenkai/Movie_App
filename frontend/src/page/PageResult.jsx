import React from "react";
import Navbar from "../components/NavbarNew"
import Card from "../components/MovieCardNew"
import { ReactComponent as Filter } from "../assets/filter.svg"
import { useParams } from "react-router-dom";
import { TokenContext } from '../context/TokenContext'
import CircularProgress from '@mui/material/CircularProgress';
import axios from "axios";

export default function PageResult() {
  const { searchContent, by } = useParams();
  const { token } = React.useContext(TokenContext);
  const [movies, setMovies] = React.useState([])
  const [loading, setLoading] = React.useState(true);
  const [filter, setFilter] = React.useState("")

  const getResult = async () => {
    var searchMethod;
    if (by === "all") {
      searchMethod = ""
    } else if (by === "movieName") {
      searchMethod = "/films"
    } else if (by === "directorName") {
      searchMethod = "/director"
    } else if (by === "actorName") {
      searchMethod = "/actor"
    }
    const res = await axios.get(`http://127.0.0.1:9002/search${searchMethod}/${searchContent}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });
    if (res.data.length > 0) {

      setMovies(res.data)
      setLoading(false)
    }
  }

  React.useEffect(() => {
    getResult()
  }, [searchContent])

  const ResultText = (props) => {
    return (
      <div className="rowCenter" style={{ marginBottom: 20, background: 'rgba(255, 255, 255, 0.1)', padding: 20, borderRadius: 30, border: '1px solid white', width: 600 }}>
        <div className={"searchResultText"}>
          {"result Matching"}
        </div>
        <div className={"searchResultBoldText"}>
          {`\"${props.searchTarget}\"`}
        </div>
      </div>
    )
  }

  const sortByRate = async () => {
    const res = await axios.get(`http://127.0.0.1:9002/search/SortByRate/${searchContent}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });
    // console.log(res.data)
    const tmp = [...res.data]
    setMovies(tmp)
  }

  const sortByName = async () => {
    const res = await axios.get(`http://127.0.0.1:9002/search/SortByName/${searchContent}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });
    // console.log(res.data)
    const tmp = [...res.data]
    setMovies(tmp)
    // setMovies(res.data)
  }

  const sortByYear = async () => {
    const res = await axios.get(`http://127.0.0.1:9002/search/SortByYear/${searchContent}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });
    console.log(res.data)
    const tmp = [...res.data]
    setMovies(tmp)
    // setMovies(res.data)
  }

  const sortByPopularity = async () => {
    const res = await axios.get(`http://127.0.0.1:9002/search/SortByPopularity/${searchContent}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });
    // console.log(res.data)
    const tmp = [...res.data]
    setMovies(tmp)
    // setMovies(res.data)
  }

  const Filters = () => {
    return (
      <div className={'row'} style={{ columnGap: 20 }}>
        <Filter />
        <div className="filterButton" onClick={sortByRate}>Rate Mark</div>
        <div className="filterButton" onClick={sortByName}>Film name</div>
        <div className="filterButton" onClick={sortByYear}>Year</div>
        <div className="filterButton" onClick={sortByPopularity}>Popularity</div>
      </div>
    )
  }

  const ResultMovies = () => {
    // console.log(movies)
    const parts = movies.map((movie, index) => {
      if (movie.movie_id && movie.movie_name && movie.photo) {

        return (
          <Card key={index} id={movie.movie_id} img={movie.photo} name={movie.movie_name} />
        )
      }
    })

    return (
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gridGap: 30, padding: 20, borderRadius: 15 }} >
        {parts}
      </div>
    )
  }

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <CircularProgress size={1000} />
      </div>
    )
  }

  return (
    <div>
      <Navbar searchBar />
      <div className="contentBody" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', rowGap: 20 }}>
        <div style={{ display: 'flex', flexDirection: 'column', alignSelf: 'flex-start', marginLeft: "7vw" }}>
          <ResultText searchTarget={searchContent} />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', alignSelf: 'flex-start', marginLeft: "7vw" }}>
          <Filters />
        </div>
        <ResultMovies />
      </div>
    </div>
  )
}
