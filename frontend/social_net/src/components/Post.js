import './Post.css'

const Post = (props) => {

    return (
        <div className={'container'}>
            <div className="card">

                <p>{props.data.id}</p>
                <p>{props.data.content}</p>
                <p className={'name'}>{props.data.name}</p>
                <p className={'date'}>{props.data.date}</p>
            </div>
        </div>

    )
}


export default Post