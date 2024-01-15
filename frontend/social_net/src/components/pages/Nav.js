import {Route, Routes} from "react-router-dom";
import Home from "./Home/Home";
import Auth from "./Auth/Auth";
import Tape from "./Tape/Tape";


const Nav = () => {
    return(
        <div className={'routes'}>
            <Routes>
                <Route path={'/'} element={<Home />}></Route>
                <Route path={'/auth'} element={<Auth />}></Route>
                <Route path={'/tape'} element={<Tape />}></Route>


            </Routes>

        </div>
    )
}


export default Nav