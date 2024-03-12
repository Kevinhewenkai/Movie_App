import React from "react";
import Navbar from "../components/Navbar";
import { Stack } from "@mui/material";
import ResetPWForm from "../components/ResetPWForm";

function ResetPassword() {
  return (
    <>
      <div className="backgroundImage">
        <ResetPWForm />
      </div>
    </>
  )
}

export default ResetPassword;
