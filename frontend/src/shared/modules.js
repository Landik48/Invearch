import {ref} from "vue";

const user = ref(null);

const getUser = async () => {
    try {
        const response = await fetch(`http://localhost/api/users/user/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        });
        if (response.status === 403) {
            user.value = null
        } else if (!response.ok) {
            alert("Ошибка на стороне сервера, повторите попытку позже")
            throw new Error('Network response was not ok');
        } else {
            user.value = await response.json();
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

export {user as default, user, getUser, getCookie};