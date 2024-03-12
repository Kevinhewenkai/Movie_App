import React from "react";
import { useNavigate } from "react-router-dom";
import { TokenContext } from '../context/TokenContext'
import axios from "axios";

function RegisterForm() {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [name, setName] = React.useState('');
  const [loginError, setLoginError] = React.useState(true);
  const { setToken } = React.useContext(TokenContext);
  const navigate = useNavigate();

  const handleEmailInputChange = event => {
    setEmail(event.target.value);
  };

  const handlePasswordInputChange = event => {
    setPassword(event.target.value);
  }

  const handleNameInputChange = event => {
    setName(event.target.value);
  }

  React.useEffect(() => {
    setLoginError(false)
  }, [email, password, name])

  return (<>
    <div className='pinkButton' style={{ position: 'absolute', right: 5, top: 10, width: 200, paddingLeft: 0 }} onClick={() => navigate('/')}>Sign in</div>
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', rowGap: 40, height: '100vh', justifyContent: 'center' }}>
      <div className='title'>
        Delphinus
      </div>
      <div className='register-subtitle'>
        A movie finder system, you can search any movies here
      </div>
      <input className='blackButton' placeholder='email' type='text' onChange={handleEmailInputChange}></input>
      <input className='blackButton' placeholder='password' type='password' onChange={handlePasswordInputChange}></input>
      <input className='blackButton' placeholder='name' type='text' onChange={handleNameInputChange}></input>
      <div className={'pinkButton'} onClick={
        async () => {
          const res = await axios.post('http://127.0.0.1:9002/auth/register',
            {
              name: name,
              email: email,
              password: password
            }, {
            headers: {
              'Content-Type': 'application/json'
            }
          });
          if (res.data.token) {
            setToken(res.data.token)
            navigate('/dashboard');
          } else {
            setLoginError(true);
          }
        }}>
        Register
      </div>
      {
        loginError &&
        <div className='login-boldText' style={{ color: 'red' }}>
          The password need at least 8 charactor
        </div>
      }
    </div>
  </>);
}

export default RegisterForm;
