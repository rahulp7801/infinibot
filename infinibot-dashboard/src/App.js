import './App.css';
import {Switch, Route} from 'react-router-dom'
import { DashboardPage, MenuPage } from './pages/'
import { LandingPage } from './pages/LandingPage';

function App() {
  return (
    <Switch>
      <Route path="/" exact={true} component={LandingPage}/>
      <Route path="/dashboard/server/:guildID/:page" exact={true} component={DashboardPage}/>
      <Route path="/dashboard/menu" exact={true} component={MenuPage}/>
    </Switch>
  );
}

export default App;
