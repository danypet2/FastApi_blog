import axios from "axios";
import {type} from "@testing-library/user-event/dist/type";

export const requestApiLogin = (array) => {

    axios.post('http://127.0.0.1:8000/auth/login', {
        grant_type: '',
        username: array.username,
        password: array.password,
        scope: '',
        client_id: '',
        client_secret: ''
    }, {
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
        .then(response => {
            console.log(response.data);
            // Обработка успешного ответа
        })
        .catch(error => {
            console.error(error);
            // Обработка ошибки
        });
}

export const requestApiRegister = (array) => {
    axios.post('http://127.0.0.1:8000/auth/register', {
        email: array.email,
        username: array.username,
        hashed_password: array.password,

    },)
        .then(response => {
            if (response.status == 200) {
                array.setIsSuccess(true)
                axios.post('http://127.0.0.1:8000/auth/verify_email', {
                    email_user: array.email
                })
                    .then(response => {
                        console.log(response)
                    })
                    .catch(error => {
                        console.log(error + '123123123123123123123123')
                    })


            }
        })
        .catch(error => {
            console.log(error)
        })
}


