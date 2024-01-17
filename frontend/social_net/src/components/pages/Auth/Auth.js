import {useState} from "react";
import './Auth.css'
import {requestApiRegister, requestApiLogin} from "./AuthServer";


const Auth = () => {


    const [usernameRegisterValue, setUsernameRegisterValue] = useState('')
    const [emailRegisterValue, setEmailRegisterValue] = useState('')
    const [passRegisterValue, setPassRegisterValue] = useState('')
    const handleRegisterUsernameChange = (e) => {
        setUsernameRegisterValue(e.target.value);
    }
    const handleRegisterEmailChange = (e) => {
        setEmailRegisterValue(e.target.value);
    }

    const handleRegisterPassChange = (e) => {
        setPassRegisterValue(e.target.value);
    }

    const onSudmitRegister = (e) => {
        e.preventDefault()
        const postDataRegister = {
            username: usernameRegisterValue, email: emailRegisterValue, password: passRegisterValue
        }
        requestApiRegister(postDataRegister)

    }


    const [inputUsernameValue, setInputUsernameValue] = useState('');
    const [inputPassValue, setInputPassValue] = useState('')
    const handleInputUsernameChange = (e) => {
        setInputUsernameValue(e.target.value);
    }

    const handleInputPassChange = (e) => {
        setInputPassValue(e.target.value)
    }
    const onSudmitEntry = (e) => {
        e.preventDefault()
        const postData = {
            username: inputUsernameValue, password: inputPassValue
        }
        requestApiLogin(postData)
    }

    return (<div className="form-container">
        <div className="form-toggle">
            <button id="login-toggle">Вход</button>
            <button id="register-toggle">Регистрация</button>
        </div>
        <form id="login-form" className="form" onSubmit={onSudmitEntry}>
            <h2>Вход</h2>
            <div className="form-group">
                <label htmlFor="login-username">Имя пользователя</label>
                <input type="text" id="login-username" name="login-username" value={inputUsernameValue}
                       onChange={handleInputUsernameChange} required/>
            </div>
            <div className="form-group">
                <label htmlFor="login-password">Пароль</label>
                <input type="password" id="login-password" name="login-password" value={inputPassValue}
                       onChange={handleInputPassChange} required/>
            </div>
            <button type="submit">Войти</button>
        </form>
        <form id="register-form" className="form" onSubmit={onSudmitRegister}>
            <h2>Регистрация</h2>
            <div className="form-group">
                <label htmlFor="register-username">Email пользователя</label>
                <input type="text" id="register-username" name="register-username" value={usernameRegisterValue}
                       onChange={handleRegisterUsernameChange} required/>
            </div>
            <div className="form-group">
                <label htmlFor="register-email">Email</label>
                <input type="email" id="register-email" name="register-email" required value={emailRegisterValue}
                       onChange={handleRegisterEmailChange}/>
            </div>
            <div className="form-group">
                <label htmlFor="register-password">Пароль</label>
                <input type="password" id="register-password" name="register-password" required
                       value={passRegisterValue} onChange={handleRegisterPassChange}/>
            </div>
            <button type="submit">Зарегистрироваться</button>
        </form>
    </div>);
}


export default Auth