import React from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import '../App.css'
import { TokenContext } from '../context/TokenContext'

function ResetPassword() {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [code, setCode] = React.useState('');
  const [confirm, setConfirm] = React.useState('');
  const [error, setError] = React.useState(false);

  const { setToken } = React.useContext(TokenContext);
  const navigate = useNavigate();

  const handleEmailInputChange = event => {
    setEmail(event.target.value);
  };

  const handlePasswordInputChange = event => {
    setPassword(event.target.value);
  }

  const handleCodeChange = event => {
    setCode(event.target.value);
  }

  const handleConfirmChange = event => {
    setConfirm(event.target.value);
  }

  React.useEffect(() => {
    setError(false)
  }, [email, password, code, confirm])

  return (
    <>
      <div className='pinkButton' style={{ position: 'absolute', right: 5, top: 10, width: 200, paddingLeft: 0 }} onClick={() => navigate('/')}>Sign in</div>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', rowGap: 20, height: '100vh', justifyContent: 'center' }}>
        <div className='title'>
          Delphinus
        </div>
        <div className='login-subtitle'>
          Login with your email
        </div>
        <input className='blackButton' placeholder='email' type='text' onChange={handleEmailInputChange}></input>
        {
          email.length > 0 &&
          <button className="pinkButton" style={{ width: 120, height: 60, padding: 0 }}
            onClick={async () => {
              await axios.post('http://127.0.0.1:9002/auth/reset_psw/send_mail', {
                email: email
              })
            }}>send</button>
        }
        <input className='blackButton' placeholder='code' type='text' onChange={handleCodeChange}></input>
        <input className='blackButton' placeholder='password' type='password' onChange={handlePasswordInputChange}></input>
        <input className='blackButton' placeholder='confirm' type='password' onChange={handleConfirmChange}></input>
        <div className={'pinkButton'} onClick={
          async () => {
            if (password !== confirm) {
              setError(true)
              return;
            }

            const res = await axios.post('http://127.0.0.1:9002/auth/reset_psw',
              {
                email: email,
                code: code,
                new_psw: password
              }, {
              headers: {
                'Content-Type': 'application/json'
              }
            });
            if (res.status === 200) {
              navigate('/dashboard')
            }
            // if (res.data.token) {
            //   setToken(res.data.token)
            //   navigate('/dashboard')
            // } else {
            //   setLoginError(true)
            // }
          }}>
          Reset
        </div>
        {
          error &&
          <div className='login-boldText' style={{ color: 'red' }}>
            Your email or password or code is invalid
          </div>
        }
      </div>
    </>
  );
}

export default ResetPassword;
