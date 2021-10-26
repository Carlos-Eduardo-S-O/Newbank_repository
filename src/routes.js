import {createAppContainer, createSwitchNavigator} from 'react-navigation';

import Login from './pages/Login';
import Main from './pages/Main';
import Timeout from './pages/Timeout';

// Cat from phone's database and verify the time and choose the right route. 
const Routes = createAppContainer(
  createSwitchNavigator({
    Login,
    Main,
    Timeout,
  }),
);

export default Routes;
