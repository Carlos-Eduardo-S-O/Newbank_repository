import React from 'react';
import Toast from 'react-native-simple-toast';
import logo from '../../assets/Nubank_Logo.png';

import {authenticate} from '../../api';

import {
    InputField,
    SafeAreaView,
    SignInButton,
    SignInButtonText,
    Logo,
    Text,
    Container,
} from './styles';

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
        if (authentication["result"] == "authenticated") {
            this.openMainScreen(authentication["token"])
        } else {
            Toast.show("ERRO! Usuário e/ou senha estão incorretos.",
                Toast.LONG
            )
        }
    }
    
    openMainScreen = (token) => {
        this.props.navigation.navigate("Main",  {token: token});
    }
}
