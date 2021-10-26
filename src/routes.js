import {createAppContainer, createSwitchNavigator} from 'react-navigation';

import Login from './pages/Login';
import Main from './pages/Main';

// Cat from phone's database and verify the time and choose the right route. 
const Routes = createAppContainer(
  createSwitchNavigator({
    Login,
    Main,
  }),
);

export default Routes;
