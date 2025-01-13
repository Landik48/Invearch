import {ref} from "vue";

const user = ref(null);
const startups = ref(null);

const getData = async (object, name_operation) => {
    try {
        let url = ''
        if (name_operation === 'user') {
            url = `http://localhost/api/users/user/`
        } else if (name_operation === 'startups') {
            url = `http://localhost/api/startups/`;
        }
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        });
        if (response.status === 403) {
            object.value = null
        } else if (!response.ok) {
            alert("Ошибка на стороне сервера, повторите попытку позже")
            throw new Error('Network response was not ok');
        } else {
            object.value = await response.json();
        }
    } catch {
        alert("Ошибка на стороне сервера, повторите попытку позже")
    }
}

function getCookie(name) {
    const matches = document.cookie.match(new RegExp(
        '(?:^|; )' + name.replace(/([.$?*|{}()[\]\/+^])/g, '\$1') + '=([^;]*)(;|$)'
    ));
    return matches ? decodeURIComponent(matches[1]) : null;
}

export {user as default, user, getData, getCookie, startups};