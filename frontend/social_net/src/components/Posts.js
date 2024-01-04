import './Posts.css'
import Post from "./Post";

const Posts = (props) => {
    {props.data.length > 0 ? props.data.map(post =>
                console.log(post)

            ) : console.log(0)}
    return (

        <div className="container">
            {props.data.length > 0 ? props.data.map(post =>
                <Post data={post}></Post>

            ) : <div>Нет постов</div>}

        </div>
    )
}

export default Posts