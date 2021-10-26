import React from 'react';
import logo from '../../assets/Nubank_Logo.png';
import CountDown from 'react-native-countdown-component';

import {
    SafeAreaView,
    Logo,
    Text,
    Container,
    RoundContainer,
    RoundInContainer,
} from './styles';

export default class Login extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            timer: this.props.navigation.state.params.time
        }
    }

    render = () => {
        const {timer} = this.state

        return (
            <SafeAreaView>
                <Container>
                    <RoundContainer>
                        <RoundInContainer>
                            <Logo source={logo} />
                            <Text>Timeout</Text>
                            <CountDown
                                until={timer}
                                onFinish={this.openLoginScreen}
                                size={15}
                                digitStyle={{backgroundColor: '#8B10AE'}}
                                digitTxtStyle={{color: '#fff', fontSize: 22}}
                                separatorStyle={{color: '#fff'}}
                                timeToShow={['M', 'S']}
                                timeLabels={{m: null, s: null}}
                                showSeparator
                            />
                        </RoundInContainer>
                    </RoundContainer>
                </Container>
            </SafeAreaView>
        )
    }
    
    openLoginScreen = () => {
        this.props.navigation.navigate("Login");
    }
}
