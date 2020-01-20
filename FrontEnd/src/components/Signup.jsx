import React from 'react';
import axios from 'axios';
import NavBar from './NavBar';

class Signup extends React.Component{
    constructor(props){
        super(props);

        this.state = {
            name: "",
            email: "",
            password: "",
            number: "",
            license: ""
        }
    }

    handleChange(key, value){
        this.setState({
            [key]: value
        })
    }

    handleSubmit(e){
        e.preventDefault();

        axios.post('http://127.0.0.1:5000/signup',{
            name: this.state.name,
            email: this.state.email,
            password: this.state.password,
            number: this.state.number,
            license: this.state.license,
        })
        .then(res => {
            console.log(res)
            this.props.history.push("/login")
        })
        .catch(err => console.log(err))
    }

    render(){
        return(
            <div>
                <NavBar />
                <div className="container mt-5">
                    <form onSubmit = {e => this.handleSubmit(e)}>
                        <div className="form-group">
                            <label for="exampleInputPassword1">Name</label>
                            <input type="text" className="form-control" id="exampleInputPassword1" placeholder="Name" name="name" onChange={e => this.handleChange(e.target.name, e.target.value)}/>
                        </div>
                        <div className="form-group">
                            <label for="exampleInputEmail1">Email address</label>
                            <input type="email" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email" name="email" onChange={e => this.handleChange(e.target.name, e.target.value)}/>
                            <small id="emailHelp" className="form-text text-muted">We'll never share your email with anyone else.</small>
                        </div>
                        <div className="form-group">
                            <label for="exampleInputPassword1">Password</label>
                            <input type="password" className="form-control" id="exampleInputPassword2" placeholder="Password" name="password" onChange={e => this.handleChange(e.target.name, e.target.value)}/>
                        </div>
                        <button type="submit" className="btn btn-info">Signup</button>
                    </form>
                </div>
            </div>
        );
    }
}

export default Signup;