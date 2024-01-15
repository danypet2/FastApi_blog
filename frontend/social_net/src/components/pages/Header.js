import Nav from "./Nav";
import {NavLink} from "react-router-dom";
import './Header.css'

const Header = () => {
    return (
        <div className={'content'}>
            <div className={'nav-wrapper'}>
                <div className={'nav-list'}>
                    <ul>

                        <li>
                            <NavLink to={'/'}>Домой</NavLink>
                        </li>
                        <li className={'auth'}><NavLink to={'/auth'}>Авторизация</NavLink>
                        </li>
                        <li className={'posts'}>
                            <NavLink to={'/tape'}>Лента новостей</NavLink>
                        </li>
                    </ul>

                </div>

            </div>
            <Nav/>
        </div>
    )
}


export default Header