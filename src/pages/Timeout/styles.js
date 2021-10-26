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

export const Logo = styled.Image`
`;

export const Text = styled.Text`
    color: #fff;
    font-weight: bold;
    font-size: 11px;
    text-align: center;
`;

export const Clock = styled.Text`
    color: #fff;
    font-weight: bold;
    font-size: 22px;
    text-align: center;
`;

export const RoundInContainer = styled.View`
    height: 60px;
    width: 60px;
    align-items: center;
`;

export const RoundContainer = styled.View`
    margin-top: 30%;
    border: 4px solid #fff;
    border-radius: 999999999px;
    padding: 90px;
`;
