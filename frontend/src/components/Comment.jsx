import React from "react";
import { Rating, Stack } from "@mui/material";
import { ReactComponent as User } from "../assets/User_fill.svg"
import { ReactComponent as UserAdd } from "../assets/User_add_alt.svg"
import { ReactComponent as Ban } from "../assets/Cancel.svg"
import { TokenContext } from '../context/TokenContext'
import { useNavigate } from "react-router-dom";
import axios from "axios";

const CommentsAndRating = (props) => {
  const [comment, setComment] = React.useState('');
  const [rating, setRating] = React.useState(0);

  const handleCommentChange = event => {
    setComment(event.target.value);
  }

  return (
    <div className={'columnCenter'}>
      <div className={'row'} style={{ columnGap: 20 }}>
        <div className={'smallpinkButton'}>
          Write your comments
        </div>
        <div className={'smallpinkButton'}>
          Rate
          <Rating
            value={rating}
            onChange={(event, newValue) => {
              setRating(newValue)
            }}
          />
        </div>
        <div
          className={'smallpinkButton'}
          style={{ backgroundColor: '#F58502', width: 200, cursor: 'pointer' }}
          onClick={async () => {
            const res = await axios.post(`http://127.0.0.1:9002/review/add_comment_rating/${props.id}`,
              {
                "movie_id": props.id,
                "review": comment,
                "rating": rating,
                "added_on": 123124
              }, {
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${props.token}`
              }
            });
            props.addReview(rating, comment)
            setComment("")
          }}
        >
          Submit
        </div>
      </div>
      <textarea className={'commentInput'} rows="3" cols="33"
        value={comment}
        onChange={handleCommentChange}
        style={{ color: '#FFF', fontFamily: 'Inter', fontStyle: 'normal', fontSize: 24, padding: 10, marginBottom: 10 }} />
    </div>
  )
}

function Comment(prop) {
  const [image, setImage] = React.useState('');
  const [name, setName] = React.useState('');
  const [userName, setUserName] = React.useState('');
  const [reviews, setReviews] = React.useState([]);
  const { token } = React.useContext(TokenContext);

  const getUserName = async () => {
    const res = await axios.get(`http://127.0.0.1:9002/user/profile/me`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });
    setUserName(res.data.user_name)
  }

  React.useEffect(() => {
    getUserName();
  })

  const handleAddReviews = (rating, review) => {
    const data = ({
      name: userName,
      rating: rating,
      review: review,
    })
    setReviews([...reviews, data])
  }

  const getReviews = async () => {
    const results = [];
    const res = await axios.get(`http://127.0.0.1:9002/review/get_comments/${prop.id}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });
    if (res.data && res.data.review_id) {
      for (let i = 0; i < res.data.review_id.length; i++) {
        const review = await axios.get(`http://127.0.0.1:9002/review/get_comments/${prop.id}/${res.data.review_id[i]}`,
          {
            headers: {
              'Authorization': `Bearer ${token}`,
            }
          })
        results.push({
          name: review.data.user_name,
          rating: review.data.rating,
          review: review.data.review,
          user_id: review.data.user_id
        })
      }
      setReviews(results);
    }
  }


  const CommentReady = (props) => {
    const navigate = useNavigate();
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

    const banUser = async (id) => {
      await axios.post(`http://127.0.0.1:9002/banned/add/${id}`,
        {
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        })
    }

    const visitOtherUserProfile = (id) => {
      navigate(`/profile/${id}`)
    }

    const parts = reviews.map((review, index) => {
      return (
        <div style={{ width: 1003, backgroundColor: 'rgba(255, 255, 255, 0.1)', padding: 20, paddingBottom: 80, border: '1 solid #8B8787', borderRadius: 30, marginLeft: 10 }}>
          <div className={'rowBetween'}>
            <div className="row" style={{ alignItems: 'center', columnGap: 10 }}>
              <User />
              <div className={"movieInfo"} style={{ fontSize: 20 }} onClick={() => visitOtherUserProfile(review.user_id)}>{review.name}</div>
              <Rating value={review.rating} readOnly />
            </div>
            <Stack direction='row' spacing={2}>
              <div style={{ cursor: 'pointer' }}>
                <UserAdd onClick={() => followUser(review.user_id)} />
              </div>
              <div style={{ cursor: 'pointer' }}>
                <Ban onClick={() => { banUser(review.user_id) }} />
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

  const getMovie = async () => {
    const response = await axios.get(`http://127.0.0.1:9002/movie/${prop.id}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });
    setImage(response.data.movie_photo);
    setName(response.data.name);
  }

  React.useEffect(() => {
    getMovie()
  }, [])

  React.useEffect(() => {
    getReviews()
  }, [])

  return (
    <div className={'columnCenter'}>
      <div className={'movieTitle'} style={{ textAlign: 'center', marginBottom: 20 }}>
        {name}   I
      </div>
      <div className={'row'} style={{ alignItems: 'flex-start', marginBottom: 10 }} >
        <img src={`data:image/jpeg;base64,${image}`} className={'cardImage'} />
        <div className={'columnCenter'}>
          <CommentsAndRating id={prop.id} token={token} addReview={handleAddReviews} />
          <CommentReady />
        </div>
      </div>
    </div>
  )
}

export default Comment;
