import './Posts.css'
import Post from "./Post";

const Posts = (props) => {
    if (!props.data || props.data.length === 0) {
        return <div><p>Нет постов</p></div>
    }
    return (

        <div className="container">
            {props.data.length > 0 ? props.data.map(post =>
                <Post data={post.post}></Post>
            ) : <div>Нет постов</div>}

        </div>
    )
}

export default Posts