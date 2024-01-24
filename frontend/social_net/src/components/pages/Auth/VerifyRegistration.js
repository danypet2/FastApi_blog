import {useState} from "react";
import {verificationEmail} from "./AuthServer";

const VerifyRegistration = (props) => {
    const [inputCodeValue, setInputCodeValue] = useState('')
    const handleInputCodeValue = (e) => {
        setInputCodeValue(e.target.value);
    }

    const onSudmitEntry = (e) => {
        e.preventDefault()
        const data = {
            code : inputCodeValue,
            email : props.props
        }
        verificationEmail(data)
    }


    return (
        <div>
            <div className="form-toggle">
                <button id="register-toggle">Подтвердите вашу электронную почту!</button>
            </div>
            <form id="login-form" className="form" onSubmit={onSudmitEntry}>
                <h2>Введите код, отправленный на вашу электронную почту!</h2>
                <div className="form-group">
                    <label htmlFor="login-password">Код</label>
                    <input type="password" id="login-password" name="login-password" onChange={handleInputCodeValue}
                           required/>
                </div>
                <button type="submit">Войти</button>
            </form>
        </div>
    )
}

export default VerifyRegistration