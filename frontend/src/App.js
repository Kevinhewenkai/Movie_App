import './App.css';
import {
  BrowserRouter,
  Route,
  Routes
} from 'react-router-dom';
import Login from "./page/Login";
import Register from "./page/Register";
import Dashboard from "./page/Dashboard";
import WishList from "./page/WishList";
import Comments from "./page/Comments";
import MovieNew from "./page/MovieNew";
import Profile from "./page/profile";
import OtherProfile from "./page/OtherProfile";
import ResetPassword from "./page/ResetPassword";
import SearchResult from "./page/PageResult";
import { TokenContext } from './context/TokenContext'
import { PopupContext } from './context/PopupContext'
import { MovieIdContext } from './context/MovieIdContext'
import "@fontsource/inter";
import React from 'react';

function App() {
  const [token, setToken] = React.useState('')
  const [popupOpen, setPopupOpen] = React.useState(false)
  const [movieId, setMovieId] = React.useState(0)

  return (
    <div>
      <TokenContext.Provider value={{ token, setToken }} >
        <PopupContext.Provider value={{ popupOpen, setPopupOpen }}>
          <MovieIdContext.Provider value={{ movieId, setMovieId }}>
            <BrowserRouter>
              <Routes>
                <Route path='/' element={<Login />} />
                <Route path='/register' element={<Register />} />
                <Route path='/dashboard' element={<Dashboard />} />
                <Route path='/wishlist/:id' element={<WishList />} />
                <Route path='/comments/:id' element={<Comments />} />
                <Route path='/movie/:id' element={<MovieNew />} />
                <Route path='/reset' element={<ResetPassword />} />
                <Route path='/searchResult/:searchContent/:by' element={<SearchResult />} />
                <Route path='/profile' element={<Profile />} />
                <Route path='/profile/:id' element={<OtherProfile />} />
              </Routes>
            </BrowserRouter>
          </MovieIdContext.Provider>
        </PopupContext.Provider>
      </TokenContext.Provider>
    </div>
  );
}

export default App;
