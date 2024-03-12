import React from "react";
import { ReactComponent as Down } from "../assets/down.svg"
import { useNavigate } from "react-router-dom";

export default function SearchBar() {
  const [showSearchFilter, setShowSearchFilter] = React.useState(false);
  const [searchFilter, setSearchFilter] = React.useState('all');
  const [searchContent, setSearchContent] = React.useState('');
  const navigate = useNavigate();

  const handleShowSearchFilterChange = () => {
    setShowSearchFilter(!showSearchFilter);
  }

  const handleSearchContentChange = (event) => {
    setSearchContent(event.target.value);
  }

  const SearchFilter = () => {
    return (
      <div style={{ display: 'flex', flexDirection: 'row', columnGap: 20, backgroundColor: 'white', padding: 10, top: 200, borderRadius: 15 }}>
        <div
          className={"cardName"}
          onClick={() => {
            handleShowSearchFilterChange();
            setSearchFilter('all')
          }}
        >all</div>
        <div
          className={"cardName"}
          onClick={() => {
            handleShowSearchFilterChange();
            setSearchFilter('movie')
          }}
        >movie</div>
        <div
          className={"cardName"}
          onClick={() => {
            handleShowSearchFilterChange();
            setSearchFilter('director')
          }}
        >director</div>
        <div
          className={"cardName"}
          onClick={() => {
            handleShowSearchFilterChange();
            setSearchFilter('actor')
          }}
        >actor</div>
      </div>
    )
  }

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      navigate(`/searchResult/${searchContent}/${searchFilter}`)
    }
  }

  return (
    <>
      <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
        <div style={{ position: 'absolute', cursor: 'pointer' }} className={"rowCenter"}>
          <div className={"cardName"} style={{ marginLeft: 10, marginRight: 10 }} onClick={handleShowSearchFilterChange}>
            {searchFilter === 'all' && 'ALL'}
            {searchFilter === 'movie' && 'Mov'}
            {searchFilter === 'director' && 'Dir'}
            {searchFilter === 'actor' && 'Act'}
          </div>
          <Down onClick={handleShowSearchFilterChange} />
        </div>
        <input
          onKeyDown={handleKeyDown}
          onChange={handleSearchContentChange}
          placeholder={"search..."}
          className="searchBar"
          style={{
            display: 'flex',
            flexflexDirection: 'row',
            alignItems: 'center',
            fontSize: '48px'
          }}
        />
      </div>
      {
        showSearchFilter &&
        <SearchFilter />
      }
    </>
  )
}
