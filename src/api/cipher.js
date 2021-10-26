import {RSA} from 'react-native-rsa-native'
import keyfile from './keyfile.json'

const PUBLIC_KEY = keyfile.public

export const encrypt = async (plainText) => {
    let promise = null

    try {
        let encrypted = await RSA.encrypt((plainText), PUBLIC_KEY)

        promise = Promise.resolve(encrypted)
    } catch (error) {
        console.debug("ERROR, it was not possible to encrypt: " + error)

        promise = Promise.reject(error)
    }

    return promise
}

export const decrypt = async (encrypted, private_key) => {
    let promise = null

    try {
        let plainText = await RSA.decrypt(encrypted, private_key)
        
        promise = Promise.resolve(plainText)
    } catch (error) {
        console.debug("ERROR, it was not possible to decrypt: " + error)

        promise = Promise.reject(error)
    }

    return promise
}
