import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class NavBar extends Component {
    render() {
        let user = JSON.parse(localStorage.getItem('user'));
        return(
            <div className="bg-info p-2">
                <p>Rent a Car</p>
                <Link to="/" className="text-white">Home</Link>
                {
                localStorage.getItem('token') === null
                ?
                <div className="d-flex float-right">
                    <Link to="/login" className="text-white mr-5">Login</Link>
                    <Link to="/signup" className="text-white">Signup</Link>
                </div>
                :
                <div className="d-flex float-right">
                    <Link to="/bookings" className="text-white mr-5">My Bookings</Link> 
                    <Link to="/" className="text-white mr-5" onClick = {() => {
                    localStorage.clear();
                    }}>Logout {user['name']}</Link>
                </div>
                }
            </div>
        );
    }
}

export default NavBar;