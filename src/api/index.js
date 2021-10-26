import RNFetchBlob from 'react-native-fetch-blob'

const AUTHENTICATION_URL = 'https://172.29.1.1:5000/';
const MAIN_URL = 'https://172.29.1.2:5000/';
const NOTIFICATION_URL = 'https://172.29.1.3:5000/';

export const accessURL = async (url) => {
    let promise = null;    
    
    try{
        //With this line the api could to has access to fetch using selfsinged certificate
        const response = await RNFetchBlob.config({
            trusty : true
        }).fetch('GET', url)

        if (response) {
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
    const credentials = '{"login": "' + login + '", "password": "' + password + '"}'

    const url = AUTHENTICATION_URL + 'authenticate?data=' + credentials
    
    return accessURL(url)
}

export const getUser = async (token) => {
    const url = MAIN_URL + 'main?token=' + token
    
    return accessURL(url)
}

export const getNotification = async (token) => {
    const url = NOTIFICATION_URL + 'notification?token=' + token
    
    return accessURL(url)
}
