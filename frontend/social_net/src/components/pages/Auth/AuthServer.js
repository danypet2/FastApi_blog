import axios from "axios";

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
    console.log(array + '123123123asdsda')
    // Дописать логику обращения к Api
}


