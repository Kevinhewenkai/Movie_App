import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ReactComponent as User } from "../assets/user.svg"
import { ReactComponent as UserLarge } from "../assets/userLarge.svg"
import { ReactComponent as User2 } from "../assets/userInProfile.svg"
import { ReactComponent as Video } from "../assets/Video_fill (1).svg"
import { ReactComponent as Edit } from "../assets/edit.svg"
import { ReactComponent as Lock } from "../assets/lock.svg"
import { ReactComponent as Unlock } from "../assets/unlock.svg"
import { ReactComponent as Trash } from "../assets/trash.svg"
import { ReactComponent as Add } from "../assets/add_ring.svg"
import { ReactComponent as Minus } from "../assets/minus.svg"
import { ReactComponent as UserAdd } from "../assets/User_add_alt.svg"
import { Stack } from "@mui/material";
import { ReactComponent as Ban } from "../assets/Cancel.svg"
import NavbarNew from "../components/NavbarNew";
import { TokenContext } from '../context/TokenContext'
import { Rating } from "@mui/material";
import axios from "axios";
import MovieCard from "../components/MovieCardNew";

const UserInfo = (props) => {
  return (
    <div style={{ display: 'flex', width: '80vw', justifyContent: 'space-between', marginBottom: 20, marginTop: 20 }}>
      <div className="rowCenter">
        <div className={"logoPadding"} style={{ width: 70, height: 60 }}>
          <UserLarge />
        </div>
        <div className="movieSubtitle" style={{ fontSize: 48 }}>{props.userName}</div>
      </div>
    </div>
  )
}

const Views = (props) => {
  return (
    <div style={{
      width: '80vw',
      display: 'flex',
      flexDirection: 'row',
      justifyContent: 'space-evenly',
      alignItems: 'center',
      backgroundColor: 'rgba(255, 255, 255, 0.1)',
      borderRadius: 30,
      height: 40,
      fontFamily: 'Inter',
      fontSize: 32,
      color: 'white',
      fontStyle: 'normal',
    }}>
      <div onClick={() => props.setView('fav')} style={{ cursor: 'pointer' }}>fav movie</div>
      <div onClick={() => props.setView('followers')} style={{ cursor: 'pointer' }}>followers</div>
      <div onClick={() => props.setView('followings')} style={{ cursor: 'pointer' }}>followings</div>
      <div onClick={() => props.setView('wishlists')} style={{ cursor: 'pointer' }}>wishlist</div>
      <div onClick={() => props.setView('reviews')} style={{ cursor: 'pointer' }}>reviews</div>
      <div onClick={() => props.setView('feedback')} style={{ cursor: 'pointer' }}>feedback</div>
      <div onClick={() => props.setView('banList')} style={{ cursor: 'pointer' }}>ban list</div>
    </div>
  )
}


export default function OtherProfile(prop) {
  const [view, setView] = React.useState('fav');
  const [userName, setUserName] = React.useState('');
  const [userId, setUserid] = React.useState(0);
  const { token } = React.useContext(TokenContext);
  const { id } = useParams()
  const navigate = useNavigate()

  const getUserName = async () => {
    const res = await axios.get(`http://127.0.0.1:9002/user/profile/other/${id}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });
    setUserName(res.data.user_name)
    setUserid(res.data.user_id)
  }

  React.useEffect(() => {
    getUserName();
  }, [])

  const Wishlist = () => {
    const [name, setName] = React.useState("")
    const [inputShow, setInputShow] = React.useState(false)
    const [itemIndex, setItemIndex] = React.useState(0)
    const [wishlists, setWishLists] = React.useState([]);

    const getWishList = async () => {
      const res = await axios.get(`http://127.0.0.1:9002/wishlists/user/${id}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        })
      const result = [];
      for (let i = 0; i < res.data.list_id.length; i++) {
        const response = await axios.get(`http://127.0.0.1:9002/wishlists/list_info/${res.data.list_id[i]}`,
          {
            headers: {
              'Authorization': `Bearer ${token}`,
            }
          })
        const statusRes = await axios.get(`http://127.0.0.1:9002/wishlists/get_wishlist_status/${res.data.list_id[i]}`,
          {
            headers: {
              'Authorization': `Bearer ${token}`,
            }
          })
        result.push({
          "name": response.data.list_name,
          "id": res.data.list_id[i],
          "status": statusRes.data.status
        })
      }
      setWishLists(result)
    }

    React.useEffect(() => {
      getWishList()
    }, [])

    const handleDeleteWishList = async (index, id) => {
      const tmp = [...wishlists]
      tmp.splice(index, 1);
      setWishLists(tmp)
      axios.delete(`http://127.0.0.1:9002/wishlists/delete_list/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
    }

    const handleNameChange = (event) => {
      setName(event.target.value)
    }

    const handleEditClick = (index) => {
      setInputShow(!inputShow)
      setItemIndex(index)
    }

    const handleLockClick = async (index) => {
      const tmp = [...wishlists];
      const change = tmp[index].status === 0 ? 1 : 0;
      tmp[index].status = change;
      setWishLists(tmp);
      await axios.post(`http://127.0.0.1:9002/wishlists/change_wishlist_status/${tmp[index].id}`,
        {
          "status": change
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        })
    }

    const onSubmit = async () => {
      const tmp = [...wishlists];
      tmp[itemIndex].name = name;
      setWishLists(tmp);
      setInputShow(false)
      await axios.post(`http://127.0.0.1:9002/wishlists/change_name/${tmp[itemIndex].id}`,
        {
          "list_name": name
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        })
    }

    const parts = wishlists.map((list, index) => {
      return (
        <div>
          {
            list.name != "fav movies" &&
            <div key={index} style={{ display: 'flex', width: '80vw', justifyContent: 'space-between', cursor: 'pointer' }}>
              <div className="rowCenter" onClick={() => { navigate(`/wishlist/${list.id}`) }}>
                <Video />
                <div className="movieSubtitle">{list.name}</div>
              </div>
              <div className="rowCenter" style={{ columnGap: 10 }}>
              </div>
            </div >
          }
        </div>
      )
    })
    return (
      <div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr' }} >
          {parts}
        </div>
        {
          inputShow &&
          <div className="columnCenter" style={{ rowGap: 15 }}>
            <input onChange={handleNameChange} style={{ width: 300, height: 35, borderRadius: 15, fontFamily: 'Inter', fontStyle: 'normal', fontSize: 20 }} />
            <button className="smallpinkButton" style={{ width: 200, height: 30 }} onClick={onSubmit}>
              edit
            </button>
          </div>
        }
      </div>
    )
  }

  const Following = () => {
    const [followings, setFollowings] = React.useState([])

    const unfollowUser = async (id, index) => {
      const tmp = [...followings];
      tmp.splice(index, 1);
      setFollowings(tmp)
      await axios.post(`http://127.0.0.1:9002/follow/delete/${id}`,
        {
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        })
    }

    const getData = async () => {
      const res = await axios.get(`http://127.0.0.1:9002/follow/me`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        })
      const result = []
      for (let i = 0; i < res.data.follow.length; i++) {
        const response = await axios.get(`http://127.0.0.1:9002/user/profile/other/${res.data.follow[i]}`,
          {
            headers: {
              'Authorization': `Bearer ${token}`,
            }
          })
        result.push({
          name: response.data.user_name,
          id: res.data.follow[i]
        })
      }
      setFollowings(result)
    }

    React.useEffect(() => {
      getData()
    }, [])

    const parts = followings.map((following, index) => {
      return (
        <div key={index} style={{ display: 'flex', width: '80vw', justifyContent: 'space-between', marginBottom: 20, marginTop: 20 }}>
          <div className="rowCenter">
            <User2 />
            <div className="movieSubtitle">{following.name}</div>
          </div>
          <div className="rowCenter" style={{ columnGap: 10 }}>
            <Trash onClick={() => { unfollowUser(following.id, index) }} />
          </div>
        </div >
      )
    })

    return (
      <div>
        {parts}
      </div>
    )
  }

  const Followers = () => {
    const [followers, setFollower] = React.useState([])
    const getData = async () => {
      const res = await axios.get(`http://127.0.0.1:9002/follow/who_follow/me`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        }
      )
      const result = []
      for (let i = 0; i < res.data.followed_by.length; i++) {
        const response = await axios.get(`http://127.0.0.1:9002/user/profile/other/${res.data.followed_by[i]}`,
          {
            headers: {
              'Authorization': `Bearer ${token}`,
            }
          })
        result.push({
          name: response.data.user_name,
          id: res.data.followed_by[i]
        })
      }
      setFollower(result)
    }

    React.useEffect(() => {
      getData()
    }, [])

    const followUser = async (id) => {
      await axios.post(`http://127.0.0.1:9002/follow/add/${id}`,
        {
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        })
    }

    const parts = followers.map((follower, index) => {
      return (
        <div key={index} style={{ display: 'flex', width: '80vw', justifyContent: 'space-between', marginBottom: 20, marginTop: 20 }}>
          <div className="rowCenter">
            <User2 />
            <div className="movieSubtitle">{follower.name}</div>
          </div>
          <div className="rowCenter" style={{ columnGap: 10 }}>
            <Add onClick={() => { followUser(follower.id) }} />
          </div>
        </div >
      )
    })
    return (
      <div>
        {parts}
      </div>
    )
  }

  const Reviews = () => {
    // const parts = wishlist.map((list, index) => {
    const [reviews, setReviews] = React.useState([]);
    const getReviews = async () => {
      const res = await axios.get(`http://127.0.0.1:9002/user/review/me`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        })
      console.log(res)
      const result = []
      for (let i = 0; i < res.data.length; i++) {
        result.push({
          rate: res.data[i].rate,
          comment: res.data[i].comment,
          image: res.data[i].movie_pic
        })
      }
      setReviews(result)
    }

    React.useEffect(() => {
      getReviews()
    })

    const parts = reviews.map((review, index) => {
      return (

        <div style={{ display: 'flex', width: '80vw', justifyContent: 'space-between', marginBottom: 20, marginTop: 20 }}>
          <div className="rowCenter">
            {/* <div className="movieSubtitle">{list.name}</div> */}
            <img src={`data:image/jpeg;base64,${review.image}`} className={'cardImage'} />
          </div>
          <div className="columnCenter" style={{ columnGap: 10, alignItems: 'flex-start' }}>
            <div className={'smallpinkButton'} style={{ marginLeft: 15 }}>
              Rate
              <Rating value={review.rate} readOnly />
            </div>
            <textarea className={'commentInput'} rows="3" cols="33"
              style={{ color: '#FFF', fontFamily: 'Inter', fontStyle: 'normal', fontSize: 24, padding: 10, width: '60vw' }} >
              {review.comment}
            </textarea>
          </div>
        </div >
      )
    })

    return (
      <div>
        {parts}
      </div>
    )
    // })

    // return (
    //   <div style={{ display: 'grid', gridTemplateColumns: '1fr', gridGap: 30 }} >
    //     {parts}
    //   </div>
    // )
  }

  const FavouriteMovies = () => {
    const [movies, setMovies] = React.useState([])
    const getFavourite = async () => {
      const res = await axios.get(`http://127.0.0.1:9002/favourite/me`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        })
      const result = []
      for (let i = 0; i < res.data.favourite.length; i++) {
        const response = await axios.get(`http://127.0.0.1:9002/movie/${res.data.favourite[i]}`,
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
      getFavourite();
    }, [])

    const parts = movies.map((movie, index) => {
      return (
        <MovieCard
          name={movie.name}
          img={movie.img}
          id={movie.id}
          key={index}
        />
      )
    }
    )
    return (
      <div>
        {
          movies.length > 0 &&
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gridGap: 30, backgroundColor: '#1D1D1D', padding: 20, borderRadius: 15 }} >
            {parts}
          </div>
        }
      </div>
    )
  }

  const FeedBack = () => {
    const [feedback, setFeedBack] = React.useState('');
    const [feedbackList, setFeedBackList] = React.useState([]);

    const handleFeedBackChange = (event) => {
      setFeedBack(event.target.value)
    }

    const onSubmit = async () => {
      const date = new Date();
      const year = parseInt(date.getFullYear())
      const month = parseInt(date.getMonth() + 1)
      const day = parseInt(date.getDate())
      const time = year * 10000 + month * 100 + day
      console.log(feedback)
      const tmp = [...feedbackList]
      tmp.push(
        {
          description: feedback,
          time: time,
          user_id: userId
        }
      )
      setFeedBackList(tmp)
      const res = await axios.post('http://127.0.0.1:9002/insert_feedback',
        {
          description: feedback,
          time: time,
          user_id: userId
        }, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        }
      });
      console.log(res)
    }

    const getFeedBack = async () => {
      const res = await axios.get(`http://127.0.0.1:9002/feedback`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        })
      console.log(res)
      const result = []
      for (let i = 0; i < res.data.length; i++) {
        const response = await axios.get(`http://127.0.0.1:9002/user/profile/other/${res.data[i].user_id}`,
          {
            headers: {
              'Authorization': `Bearer ${token}`,
            }
          })
        result.push({
          name: response.data.user_name,
          id: res.data[i].user_id,
          description: res.data[i].description
        })
      }
      setFeedBackList(result)
    }

    React.useEffect(() => {
      getFeedBack()
    }, [])

    const parts = feedbackList.map((feedbackItem, index) => {
      return (
        <div key={index} style={{ width: 1003, backgroundColor: 'rgba(255, 255, 255, 0.1)', padding: 20, paddingBottom: 80, border: '1 solid #8B8787', borderRadius: 30, marginLeft: 10 }}>
          <div className={'rowBetween'}>
            <div className="row" style={{ alignItems: 'center', columnGap: 10 }}>
              <User2 />
              <div className={"movieInfo"} style={{ fontSize: 20 }}>{feedbackItem.name}</div>
            </div>
            <div className={"movieInfo"} style={{ fontSize: 20 }}>{feedbackItem.time}</div>
          </div>
          <div className={'movieInfo'} style={{ fontSize: 20, marginTop: 20, lineHeight: 1 }}>{feedbackItem.description}</div>
        </div>
      )
    })

    return (
      <div className={"columnCenter"} style={{ backgroundColor: '#1D1D1D', width: '80vw', borderRadius: 30, rowGap: 30, paddingBottom: 30 }}>
        <textarea className={'commentInput'} rows="3" cols="33"
          onChange={handleFeedBackChange}
          style={{ color: '#FFF', fontFamily: 'Inter', fontStyle: 'normal', fontSize: 24, padding: 10, marginBottom: 10, width: '40vw' }} />
        <button className="pinkButton" style={{ width: '40vw', paddingLeft: 10, paddingRight: 10 }} onClick={onSubmit}>SUBMIT</button>
        {parts}
      </div>
    )
  }

  const EditProfile = () => {
    const [name, setName] = React.useState('');

    const handleNameChange = (event) => {
      setName(event.target.value)
    }

    const onSubmit = async () => {
      setUserName(name)
      await axios.post('http://127.0.0.1:9002/user/profile/update',
        {
          user_name: name
        }, {
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });
    }
    return (
      <div className={"columnCenter"} style={{ backgroundColor: '#1D1D1D', width: '80vw', borderRadius: 30, rowGap: 30, paddingBottom: 30 }}>
        <div style={{ width: '40vw', display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
          <div className="movieText">
            user name
          </div>
          <input className='blackButton' placeholder='name' type='text' onChange={handleNameChange} />
        </div>
        <button className="pinkButton" style={{ width: '40vw', paddingLeft: 10, paddingRight: 10 }} onClick={onSubmit}>SUBMIT</button>
      </div>
    )
  }

  const BanList = () => {
    const [banList, setBanList] = React.useState([])

    const getBanList = async () => {
      const res = await axios.get(`http://127.0.0.1:9002/banned`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        })
      console.log(res)
      const result = []
      for (let i = 0; i < res.data['banned id'].length; i++) {
        const userId = res.data['banned id'][i]
        const response = await axios.get(`http://127.0.0.1:9002/user/profile/other/${userId}`,
          {
            headers: {
              'Authorization': `Bearer ${token}`,
            }
          })
        result.push({
          name: response.data.user_name,
          id: userId
        })
      }
      console.log(result)
      setBanList(result)
    }

    React.useEffect(() => {
      getBanList()
    }, [])

    const unBanUser = async (id, index) => {
      const tmp = [...banList];
      tmp.splice(index, 1);
      setBanList(tmp)
      await axios.delete(`http://127.0.0.1:9002/banned/delete/${id}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        })
    }

    const parts = banList.map((bannedUser, index) => {
      return (
        <div key={index} style={{ display: 'flex', width: '80vw', justifyContent: 'space-between', marginBottom: 20, marginTop: 20 }}>
          <div className="rowCenter">
            <User2 />
            <div className="movieSubtitle">{bannedUser.name}</div>
          </div>
          <div className="rowCenter" style={{ columnGap: 10 }}>
            <Minus onClick={() => { unBanUser(bannedUser.id, index) }} />
          </div>
        </div >
      )
    })
    return (
      <div>
        {parts}
      </div>
    )
  }

  return (
    <div>
      <NavbarNew searchBar />
      <div className={"contentBody"} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <UserInfo
          setView={setView}
          userName={userName}
        />
        <Views
          view={view}
          setView={setView}
        />
        <div>
          {
            <div style={{ display: 'flex', width: '80vw', justifyContent: 'flex-start', marginBottom: 20, marginTop: 20, paddingBottom: 10, borderBottom: '10px solid white' }}>
              {view === "fav" && <div className={"profileSubTitle"}>FAVOURITE MOVIE</div>}
              {view === "followers" && <div className={"profileSubTitle"}>FOLLOWERS</div>}
              {view === "followings" && <div className={"profileSubTitle"}>FOLLOWINGS</div>}
              {view === "wishlists" && <div className={"profileSubTitle"}>WISHLIST</div>}
              {view === "reviews" && <div className={"profileSubTitle"}>REVIEWS</div>}
              {view === "feedback" && <div className={"profileSubTitle"}>FEEDBACK</div>}
              {view === "editProfile" && <div className={"profileSubTitle"}>EDIT PROFILE</div>}
              {view === "banList" && <div className={"profileSubTitle"}>BAN LIST</div>}
            </div>
          }
        </div>
        {view === "fav" && <FavouriteMovies />}
        {view === "followers" && <Followers />}
        {view === "followings" && <Following />}
        {view === "wishlists" && <Wishlist />}
        {view === "reviews" && <Reviews />}
        {view === "feedback" && <FeedBack />}
        {view === "editProfile" && <EditProfile />}
        {view === "banList" && <BanList />}
      </div>
    </div >
  )
}
