const AUTHENTICATION_URL = 'http://172.29.1.1:5000/'
const MAIN_URL = 'http://172.29.1.2:5000/';
const NOTIFICATION_URL = 'http://172.29.1.3:5000/';

export const accessURL = async (url) => {
    let promise = null;

    try {
        const response = await fetch(url, { method: 'GET' })

        if (response.ok) {
            promise = Promise.resolve(response.json())
        } else {
            promise = Promise.resolve(response)
        }
    } catch (error) {
        promise = Promise.reject(error)
    }

    return promise
}

export const authenticate = async (login, password) => {
    const url = AUTHENTICATION_URL + 'authenticate/' + login + '/' + password
    
    return accessURL(url)
}

export const getUser = async (userId) => {
    const url = MAIN_URL + 'main/' + userId
    
    return accessURL(url)
}

export const getNotification = async (userId) => {
    const url = NOTIFICATION_URL + 'notification/' + userId
    
    return accessURL(url)
}