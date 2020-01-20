import React from 'react';
import axios from 'axios';
import NavBar from './NavBar';
import {Link} from 'react-router-dom';

class Login extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            email: "",
            password: "",
        }
    }

    handleChange(key, value){
        this.setState({
            [key]: value
        })
    }

    handleSubmit(e){
        e.preventDefault();
        axios.post('http://127.0.0.1:5000/login', {
            email: this.state.email,
            password: this.state.password
        })
        .then(res => {
            console.log(res.data)
            if(res.data['data'] !== "Email Not Registered") {
                localStorage.setItem('token', (res.data["data"]["token"].split('\'')[1]))
                localStorage.setItem('user', (JSON.stringify(res.data['data']['user'][0])))
                this.props.history.push("/")
            }
            else{
                alert(res.data['data'])
                this.props.history.push('/signup')
            }
        })
        .catch(err => {alert("Check email or password.")});
    }
    render(){
        return(
            <div>
                <NavBar />
                <div className="container mt-5">
                    <form onSubmit = {e => this.handleSubmit(e)}>
                        <div className="form-group">
                            <label for="exampleInputEmail1">Email address</label>
                            <input type="email" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email" name="email" onChange={e => this.handleChange(e.target.name, e.target.value)}/>
                            <small id="emailHelp" className="form-text text-muted">We'll never share your email with anyone else.</small>
                        </div>
                        <div className="form-group">
                            <label for="exampleInputPassword1">Password</label>
                            <input type="password" className="form-control" id="exampleInputPassword2" placeholder="Password" name="password" onChange={e => this.handleChange(e.target.name, e.target.value)}/>
                        </div>
                        <button type="submit" className="btn btn-info">Login</button>
                        <br/>
                        <br/>
                        <br/>
                        <small className="text-muted">New to Our Platform</small> <Link className="text-info"><small>Sign up now >></small></Link> 
                    </form>
                </div>
            </div>
        );
    }
}

export default Login;