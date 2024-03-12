import React from "react";
import { ReactComponent as Comment } from "../assets/comment.svg"
import { ReactComponent as Save } from "../assets/save.svg"
import { ReactComponent as Trash } from "../assets/redTrash.svg"
import { useNavigate } from "react-router-dom";
import { PopupContext } from '../context/PopupContext'
import { MovieIdContext } from '../context/MovieIdContext'

export default function MovieCardNew(prop) {
  const navigate = useNavigate();

  const { setPopupOpen } = React.useContext(PopupContext)
  const { setMovieId } = React.useContext(MovieIdContext)

  const handleSaveButtonOnClick = () => {
    setMovieId(prop.id);
    setPopupOpen(true);
  }

  return (
    <>
      <div className={"cardContainer"} >
        <img src={`data:image/jpeg;base64,${prop.img}`} className={'cardImage'} onClick={() => { navigate(`/movie/${prop.id}`) }} />
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <div className={"cardName"} onClick={() => { navigate(`/movie/${prop.id}`) }}>
            {(prop.name.length > 13) ? `${prop.name.substring(0, 13)}...` : prop.name}
          </div>
          <div style={{ display: 'flex', flexDirection: 'row' }}>
            <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center', padding: 10, cursor: 'pointer' }} onClick={() => { navigate(`/comments/${prop.id}`) }} >
              <Comment />
              <span className={'cardText'}>comment</span>
            </div>
            <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center', margin: 10, cursor: 'pointer' }} onClick={handleSaveButtonOnClick}>
              <Save />
              <span className={'cardText'}>save</span>
            </div>
            {
              prop.wishlist &&
              <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center', margin: 10, cursor: 'pointer' }} onClick={prop.delete}>
                <Trash />
                <span className={'cardText'}>del</span>
              </div>
            }
          </div>
        </div>
      </div>
    </>
  )
}
