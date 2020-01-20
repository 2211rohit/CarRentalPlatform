import React from 'react';
import NavBar from './NavBar';
import axios from 'axios';

class Home extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            cars: "",
        }
    }

    componentDidMount() {
        if(JSON.parse(localStorage.getItem('user')) !== null ){
            let user = JSON.parse(localStorage.getItem('user'));
            console.log(localStorage.getItem('token'))
            axios.post('http://127.0.0.1:5000/bookings', {
                user_id: user['user_id']
            }, {
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                }
            })
            .then(res => {
                console.log(res)
                this.setState({
                    cars: res.data['data']
                })
            })
            .catch(err => console.log(err))
        }
    }

    render(){
        var cars = []
        for(var key in this.state.cars) {
            cars.push(this.state.cars[key])
        }

        return(
            <div>
                <NavBar />
                {
                    localStorage.getItem('token') !== null ? 
                    cars.map(el => {
                        return(
                            <div key = {el['car_id']} className="card mt-2" style={{width:"70%", marginLeft:"15%"}}>
                                <div className="card-body">
                                    <h6 className="card-title text-muted">Car Model: {el['car_model']}</h6>
                                    <h6 className="card-title text-muted">Car Type: {el['car_type']}</h6>
                                    <h6 className="card-title text-muted">No. of Seats: {el['car_seats']}</h6>
                                    <h6 className="card-title text-muted">Car Color: {el['car_color']}</h6>
                                    <button className="btn btn-success">Complete/Delete</button>
                                </div>
                            </div>
                        );
                    })
                    :
                    <h3 className="text-center text-info" style={{marginTop:"15%"}}>Welcome To Rent a Car</h3>

                }
            </div>
        );
    }
}

export default Home;