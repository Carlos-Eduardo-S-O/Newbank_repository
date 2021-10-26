import React, { useState, useEffect } from 'react';
import Icon from 'react-native-vector-icons/MaterialIcons';

import { Animated } from 'react-native';
import { PanGestureHandler, State } from 'react-native-gesture-handler';

import Header from '../../components/Header';
import Tabs from '../../components/Tabs';
import Menu from '../../components/Menu';

import { getUser, getNotification } from '../../api'

import {
  Container,
  Content,
  Card, CardHeader, CardContent, CardFooter, Title, Description, Annotation, SafeAreaView,
} from './styles';

export default function Main( props ) {

  let offset = 0;
  const translateY = new Animated.Value(0);
  const [ userId, setUserId ] = useState(props.navigation.state.params.userId)
  const [ user, setUser ] = useState(null)
  const [ notification, setNotification ] = useState(null)

  useEffect(() => {
    getUser(userId).then((user) => {
      setUser(user)
    }).catch((error) => {
      console.error("Error searching user.\n Details: ", error)
    })
    
    getNotification(userId).then((notification) => {
      setNotification(notification)
    }).catch((error) => {
      console.error("Error searching notification.\n Details: ", error)
    })
  }, []);
  
  const animatedEvent = Animated.event(
    [
      {
        nativeEvent: {
          translationY: translateY,
        },
      },
    ],
    { useNativeDriver: true },
  );

  function onHandlerStateChanged(event) {
    console.log(user+"\n"+notification)
    if (event.nativeEvent.oldState === State.ACTIVE) {
      let opened = false;
      const { translationY } = event.nativeEvent;

      offset += translationY;

      if (translationY >= 100) {
        opened = true;
      } else {
        translateY.setValue(offset);
        translateY.setOffset(0);
        offset = 0;
      }

      Animated.timing(translateY, {
        toValue: opened ? 380 : 0,
        duration: 200,
        useNativeDriver: true,
      }).start(() => {
        offset = opened ? 380 : 0;
        translateY.setOffset(offset);
        translateY.setValue(0);
      });
    }
  }

  if (user && notification){
    return (
      <SafeAreaView>
        <Container>
          <Header name={user.name}/>
          <Content>
            <Menu translateY={translateY} />

            <PanGestureHandler
              onGestureEvent={animatedEvent}
              onHandlerStateChange={onHandlerStateChanged}
            >
              <Card style={{
                transform: [{
                  translateY: translateY.interpolate({
                    inputRange: [-350, 0, 380],
                    outputRange: [-50, 0, 380],
                    extrapolate: 'clamp',
                  }),
                }],
              }}
              >
                <CardHeader>
                  <Icon name="attach-money" size={28} color="#666" />
                  <Icon name="visibility-off" size={28} color="#666" />
                </CardHeader>
                <CardContent>
                  <Title>Saldo disponível</Title>
                  <Description>R$ {user.account.balance} </Description>
                </CardContent>
                <CardFooter>
                  <Annotation>
                  {notification.notification}
                  </Annotation>
                </CardFooter>
              </Card>
            </PanGestureHandler>

          </Content>

          <Tabs translateY={translateY} />
        </Container>
      </SafeAreaView>
    );
  } else {
    return null
  }
}
