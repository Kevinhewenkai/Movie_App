import React from "react";
import { ReactComponent as Home } from "../assets/Home_fill.svg"
import { ReactComponent as Video } from "../assets/Video_fill.svg"
import { ReactComponent as User } from "../assets/user.svg"
import { ReactComponent as SigOnut } from "../assets/Sign_out.svg"
import SearchBar from "./SearchBar";
import { useNavigate } from "react-router-dom";

export default function NavbarNew(prop) {
  const navigate = useNavigate();
  const [showSearchFilter, setShowSearchFilter] = React.useState(false);

  const handleShowSearchFilterChange = () => {
    setShowSearchFilter(!showSearchFilter);
  }

  return (
    <>
      <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', width: '100%', alignItems: 'flex-start', position: 'absolute', left: 0, top: 10 }}>
        <div className={'rowCenter'} style={{ marginLeft: 10, cursor: 'pointer' }} onClick={() => { navigate('/dashboard') }}>
          <img src={require('../assets/smallDelphius.png')} alt={'small Delphnius'} />
          <div className={'login-boldText'} style={{ padding: 10 }}> Delphinus </div>
        </div>
        {
          prop.searchBar &&
          <SearchBar />
        }
        <div style={{ display: 'flex', flexDirection: 'row' }}>
          <div className={"logoPadding"} onClick={() => { navigate('/profile') }}>
            <User />
          </div>
          <div className={"logoPadding"} onClick={() => { navigate('/') }}>
            <SigOnut />
          </div>
        </div>
      </div>
    </>
  )
}
