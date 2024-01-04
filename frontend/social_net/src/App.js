import Posts from "./components/Posts";
import './App.css'

const myArray = [
    {
        id: 1,
        date: '28.11.2018',
        content: 'oaksd iqwje a sikd;a sidwq ipowdiqwidkjsk;a k;ds ka d;ksjak; dqo;kjdw ipdjspjqadlk; sjql wjdlksjqa;lk ',
        name: 'Danil'
    },
    {
        id: 2,
        date: '29.11.2018',
        content: 'oaksd iqwje a sikd;a sidwq ipowdiqwidkjsk;a k;ds ka d;ksjak; dqo;kjdw ipdjspjqadlk; sjql wjdlksjqa;lk ',
        name: 'Danil'
    },
    {
        id: 3,
        date: '28.11.2018',
        content: 'oaksd iqwje a sikd;a sidwq ipowdiqwidkjsk;a k;ds ka d;ksjak; dqo;kjdw ipdjspjqadlk; sjql wjdlksjqa;lk ',
        name: 'Danil'
    },
    {
        id: 4,
        date: '28.11.2018',
        content: 'oaksd iqwje a sikd;a sidwq ipowdiqwidkjsk;a k;ds ka d;ksjak; dqo;kjdw ipdjspjqadlk; sjql wjdlksjqa;lk ',
        name: 'Danil'
    },
    {
        id: 5,
        date: '28.11.2018',
        content: 'oaksd iqwje a sikd;a sidwq ipowdiqwidkjsk;a k;ds ka d;ksjak; dqo;kjdw ipdjspjqadlk; sjql wjdlksjqa;lk ',
        name: 'Danil'
    },
]


const App = () => {
    return (
        <div className={'main'}>
            <Posts data={myArray}></Posts>
        </div>
    )
}

export default App;
