import React from "react";
import Comment from "../components/Comment";
import { useParams } from "react-router-dom";
import Navbar from "../components/NavbarNew";

function Comments() {
  const { id } = useParams();
  return (
    <div>
      <Navbar />
      <div className="contentBody">
        <Comment
          id={id} />
      </div>
    </div>
  )
}

export default Comments;
