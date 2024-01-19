const VerifyRegistration = () => {
    return (
        <div>
                <div className="form-toggle">
                    <button id="register-toggle">Подтвердите вашу электронную почту!</button>
                </div>
                <form id="login-form" className="form">
                    <h2>Введите код, отправленный на вашу электронную почту!</h2>
                    <div className="form-group">
                        <label htmlFor="login-password">Код</label>
                        <input type="password" id="login-password" name="login-password"
                               required/>
                    </div>
                    <button type="submit">Войти</button>
                </form>
        </div>
    )
}

export default VerifyRegistration