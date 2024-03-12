import React from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import '../App.css'
import { TokenContext } from '../context/TokenContext'

function LoginForm() {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [loginError, setLoginError] = React.useState(true);
  const { setToken } = React.useContext(TokenContext);
  const navigate = useNavigate();

  const handleEmailInputChange = event => {
    setEmail(event.target.value);
  };

  const handlePasswordInputChange = event => {
    setPassword(event.target.value);
  }

  React.useEffect(() => {
    setLoginError(false)
  }, [email, password])

  return (
    <>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', rowGap: 40, height: '100vh', justifyContent: 'center' }}>
        <div className='title'>
          Delphinus
        </div>
        <div className='login-subtitle'>
          Login with your email
        </div>
        <input className='blackButton' placeholder='email' type='text' onChange={handleEmailInputChange}></input>
        <input className='blackButton' placeholder='password' type='password' onChange={handlePasswordInputChange}></input>
        <div className={'pinkButton'} onClick={
          async () => {
            const res = await axios.post('http://127.0.0.1:9002/auth/login',
              {
                email: email,
                password: password
              }, {
              headers: {
                'Content-Type': 'application/json'
              }
            });
            if (res.data.token) {
              setToken(res.data.token)
              navigate('/dashboard')
            } else {
              setLoginError(true)
            }
          }}>
          Login
        </div>
        {
          loginError &&
          <div className='login-boldText' style={{ color: 'red' }}>
            Your email or password is invalid
          </div>
        }
        <div className='row'>
          <span className='login-text'>
            new to delphinus?
          </span>
          <span className='login-boldText' onClick={() => { navigate('/register') }}>
            Register
          </span>
        </div>
        <div className='row'>
          <span className='login-text'>
            forget password?
          </span>
          <span className='login-boldText' onClick={() => { navigate('/reset') }}>
            reset
          </span>
        </div>
      </div>
    </>
  );
}

export default LoginForm;
