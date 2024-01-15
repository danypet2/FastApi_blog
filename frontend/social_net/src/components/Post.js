import './Post.css'

const Post = (props) => {


    return (
        <div className={'container'}>
            <div className="card">
                <tr key={props.data.id}></tr>
                <p className={'title'}>{props.data.title}</p>
                <p>{props.data.content}</p>
                <p>{props.data.image}</p>
                <p className={'name'}>{props.data.username}</p>
                <p className={'date'}>{props.data.data_updated === null ? props.data.data_published.slice(0, -22) :
                    props.data.data_updated.slice(0, -22)}</p>

            </div>
        </div>

    )
}


export default Post