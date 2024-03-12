import React from "react";
import { ReactComponent as Heart } from "../assets/heart.svg"
import { ReactComponent as Add } from "../assets/Add.svg"
import { ReactComponent as Video } from "../assets/Video_fill.svg"
import { TokenContext } from '../context/TokenContext'
import { MovieIdContext } from '../context/MovieIdContext'
import axios from "axios";

const Popup = props => {
  const [name, setName] = React.useState('');
  const [wishlist, setWishList] = React.useState([]);
  const { token } = React.useContext(TokenContext);
  const { movieId } = React.useContext(MovieIdContext)

  const handleNameChange = (event) => {
    setName(event.target.value)
  }

  React.useEffect(() => {
    console.log(wishlist);
  }, [wishlist])

  const getWishList = async () => {
    const res = await axios.get(`http://127.0.0.1:9002/wishlists`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });
    console.log(res.data)
    const result = [];
    for (let i = 0; i < res.data.list_id.length; i++) {
      const response = await axios.get(`http://127.0.0.1:9002/wishlists/list_info/${res.data.list_id[i]}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        })
      result.push({
        "name": response.data.list_name,
        "id": res.data.list_id[i]
      })
    }
    setWishList(result)
  }

  const handleAddWishList = async () => {
    const res = await axios.post('http://127.0.0.1:9002/wishlists/add_list',
      {
        "list_name": name,
        "status": 0
      }, {
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
    const tmp = [...wishlist, { name: name, id: res.data.list_id }];
    setWishList(tmp)
    setName("")
  }

  const addMovieToTheList = async (id) => {
    const res = await axios.post(`http://127.0.0.1:9002/wishlists/add_to_wishlist/${id}`,
      {
        "movie_id": movieId,
        "added_on": 0
      }, {
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
    console.log(res)
  }

  const addToFavourite = async () => {
    const res = await axios.post(`http://127.0.0.1:9002/favourite/add/${movieId}`,
      {
      }, {
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    });
    console.log(res)
  }

  const Feeds = (props) => {
    const parts = wishlist.map((list, index) => {
      return (
        <div>
          {
            list.name != "fav movies" &&
            <div
              key={index}
              className={"rowCenter"}
              style={{ columnGap: 20, cursor: 'pointer' }}
              onClick={() => {
                props.popup()
                addMovieToTheList(list.id)
              }}
            >
              <Video />
              <div className={"movieSubtitle"} style={{ color: 'black' }}>
                {list.name}
              </div>
            </div>
          }
        </div>
      )
    })
    return (
      <div style={{ display: 'grid', gridTemplateColumns: '1fr' }} >
        {parts}
      </div>
    )
  }

  React.useEffect(() => {
    getWishList()
  }, [])

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleAddWishList()
    }
  }

  return (
    <div className="popup-box">
      <div className="box">
        <span className="close-icon" onClick={props.popup}>x</span>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'self-start' }}>
          <div className={"rowCenter"} style={{ columnGap: 20, cursor: 'pointer', rowGap: 20 }}
            onClick={() => {
              props.popup();
              addToFavourite();
            }}
          >
            <Heart />
            <div className={"movieSubtitle"} style={{ color: 'black' }}>
              Favourite
            </div>
          </div>
          <Feeds popup={props.popup} />
          <div className={"rowCenter"} style={{ columnGap: 20, cursor: 'pointer', rowGap: 20 }}>
            <Add onClick={handleAddWishList} />
            <input
              onKeyDown={handleKeyDown}
              onChange={handleNameChange}
              value={name}
              className={"wishlistInput"}
              style={{ color: 'black', background: '#F2EAEA', border: 0 }}
              placeholder={'New'}>
            </input>
          </div>
        </div>
        {/* <div className={"rowCenter"} style={{ columnGap: 20, cursor: 'pointer', rowGap: 20, position: 'absolute', bottom: 0, left: '20%' }}> */}
        {/*   <Add onClick={addWishlist} /> */}
        {/*   <input placeholder={"Add new wishlist"} className={"wishlistInput"} onChange={(e) => { setName(e.target.value) }} /> */}
        {/* </div> */}
      </div>
    </div>
  );
};

export default Popup;
