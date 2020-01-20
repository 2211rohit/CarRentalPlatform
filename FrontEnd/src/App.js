import React from 'react';
import { BrowserRouter, Route } from 'react-router-dom';
import Home from './components/Home';
import Signup from './components/Signup';
import Login from './components/Login';
import Bookings from './components/Bookings.jsx';

function App() {
  return (
    <BrowserRouter>
      <React.Fragment>
        <Route path="/" exact component={Home} />
        <Route path="/signup" component={Signup} />
        <Route path="/login" component={Login} />
        <Route path="/bookings" component={Bookings} />
      </React.Fragment>
    </BrowserRouter>
  );
}

export default App;
