import styled from 'styled-components/native'
import { StyleSheet } from 'react-native'

export const SafeAreaView = styled.SafeAreaView`
    flex: 1;
    background-color: #8B10AE;
`;

export const Container = styled.View`
    align-items: center;
    padding: 40px 0 30px;
`;

export const InputField = styled.TextInput`
    padding: 4px;
    height: 40px;
    width: 80%;
    margin-top: 20px;
    background-color: #fff;
    border-color: #c7c7c7;
    border-width: 1px;
    border-radius: 4px;
`;

export const SignInButton = styled.TouchableOpacity`
    border-width: ${StyleSheet.hairlineWidth}px;
    border-color: rgba(255, 255, 255, 0.8);
    border-radius: 4px;
    justify-content: center;
    align-items: center;
    padding: 12px;
    width: 80%;
    margin-top: 30px;
`;

export const SignInButtonText = styled.Text`
    color: #fff;
    font-weight: bold;
    font-size: 13px;
`;

export const Logo = styled.Image`
    margin-top: 90px;
    margin-bottom: 20px;
`;

export const Text = styled.Text`
    margin-top: 120px;
    color: #fff;
    font-weight: bold;
    font-size: 11px;
`;