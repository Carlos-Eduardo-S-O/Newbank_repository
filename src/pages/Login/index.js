import React from 'react';
import Toast from 'react-native-simple-toast';
import logo from '../../assets/Nubank_Logo.png';
import {authenticate} from '../../api';
import SyncStorage from 'sync-storage';

import {
    InputField,
    SafeAreaView,
    SignInButton,
    SignInButtonText,
    Logo,
    Text,
    Container,
} from './styles';

const MINUTE = 60
// You can control here the brute force implementation time
const BRUTE_FORCE_TIME = MINUTE * 5 // time in second

export default class Login extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            login: '',
            password: '',
        }
    }

    render = () => {

        return (
            <SafeAreaView>
                <Container>
                    <Logo source={logo} />
                    <InputField
                        placeholder="Login"
                        onChangeText={(text) => this.setState({ login: text })}
                    />
                    <InputField
                        placeholder="Senha"
                        secureTextEntry={true}
                        onChangeText={(text) => this.setState({ password: text })}
                    />
                    <SignInButton
                        onPress={this.authenticateUser}
                    >
                        <SignInButtonText>Entrar</SignInButtonText>
                    </SignInButton>
                    <Text>Seja bem vindo ao Newbank</Text>
                </Container>
            </SafeAreaView>
        )
    }

    authenticateUser = () => {
        const { login, password } = this.state
        
        if (!this.isTheFieldEmpty(login, password)){
            authenticate(login, password).then((authenticationResult) => {
                this.isAuthenticated(authenticationResult)
            }).catch((error) => {
                console.error("Error authenticating the user.   \n Details: ", error)
            })
        }else{
            Toast.show("ERRO! Por favor preencha todos os campos.",
                Toast.LONG
            )   
        }
    }

    isTheFieldEmpty = (login, password) =>{
        let empty = false
        
        if(login == "" || password == ""){
            empty = true  
        }

        return empty
    }

    isAuthenticated = (authentication) => {
        let attempts = SyncStorage.get("attempts")
        
        if (isNaN(attempts)){
            attempts = 1
            SyncStorage.set("attempts", 0)
        }

        if (authentication["result"] == "authenticated") {
            this.clearAttempts()
            this.openMainScreen(authentication["token"])
        } else {
            this.addAttempts()

            Toast.show("Usuário e/ou senha estão incorretos.",
                Toast.SHORT
            )
                
            if (attempts === 3 || attempts === 6 || attempts >= 9){
                    

                Toast.show("Você fez "+ attempts +" tentativas erradas, tente mais tarde.",
                    Toast.LONG
                )
                    
                this.openTimeoutScreen(this.setTimeout(attempts))
            }
            
        }
        
    }
    
    addAttempts = () => {
        const attempts = SyncStorage.get("attempts")
        const newAttemptsNumber = attempts + 1

        SyncStorage.set('attempts', newAttemptsNumber);
    }

    clearAttempts = () => {
        SyncStorage.set('attempts', 0);
    }

    setTimeout = (attempts) => {
        let time = BRUTE_FORCE_TIME
        
        switch(attempts){
            case 6:{
                time = time * 2
                break
            }
            case 9:{
                time = time * 3
                break
            }
            default :{
                if (attempts > 9){
                    time = time * 4
                }
            }
        }

        return time
    }

    openMainScreen = (token) => {
        this.props.navigation.navigate("Main",  {token: token});
    }

    openTimeoutScreen = (time) => {
        this.props.navigation.navigate("Timeout", {time: time})
    }
}
