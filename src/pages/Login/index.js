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

        authenticate(login, password).then((authenticationResult) => {
            this.isAuthenticated(authenticationResult["result"], authenticationResult["token"])
        }).catch((error) => {
            console.error("Error authenticating the user.   \n Details: ", error)
        })

    }

    isAuthenticated = (authentication, token) =>{
        
        if (authentication == "authenticated") {
            this.openMainScreen(token)
        } else {
            Toast.show("ERRO! Usuário e/ou senha estão incorretos.",
                Toast.LONG
            )
        }
    }

    openMainScreen = (token) => {
        //navigator.navigate("Details", {feedId: feed._id, navigator: navigator})
        this.props.navigation.navigate("Main",  {token: token});
    }
}