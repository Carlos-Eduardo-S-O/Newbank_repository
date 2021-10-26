import RNFetchBlob from 'react-native-fetch-blob'
import { encrypt, decrypt } from './cipher';
import keyfile from './keyfile.json'

const AUTHENTICATION_URL = 'https://172.29.1.1:5000/';
const MAIN_URL = 'https://172.29.1.2:5000/';
const NOTIFICATION_URL = 'https://172.29.1.3:5000/';

const PRIVATE_KEY = keyfile.private

export const accessURL = async (url) => {
    let promise = null;    
    
    try{
        //With this line the api could to has access to fetch using selfsinged certificate
        const response = await RNFetchBlob.config({
            trusty : true
        }).fetch('GET', url)

        if (response) {
            if (response.data == "error user not found"){
                const result = {"result": response.data}
                promise = Promise.resolve(result)
            }else{
                // Decrypt the data sent by back-end
                let data = await decrypt(response.data, PRIVATE_KEY)
                data = JSON.parse(data)
                promise = Promise.resolve(data)           
            }
        } else {
            promise = Promise.resolve(response)
        }
        
    } catch (error) {
        promise = Promise.reject(error)
    }

    return promise
}

export const authenticate = async (login, password) => {
    // Setting the data to send to back-end
    const preparedLogin = '"login": "' + login + '"'
    const preparedPassword = '"password": "' + password + '"'
    
    const jsonString = encodeURIComponent(await encrypt('{' + preparedLogin + ', ' + preparedPassword + '}'))
    
    const url = AUTHENTICATION_URL + 'authenticate?data=' + jsonString 

    return accessURL(url)
}

export const getUser = async (token) => {
    const preparedToken = encodeURIComponent(await encrypt(token))

    const url = MAIN_URL + 'main?token=' + preparedToken
    
    return accessURL(url)
}

export const getNotification = async (token) => {
    const preparedToken = encodeURIComponent(await encrypt(token))

    const url = NOTIFICATION_URL + 'notification?token=' + preparedToken
    
    return accessURL(url)
}


