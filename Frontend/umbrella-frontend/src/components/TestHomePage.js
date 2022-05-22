import React from 'react'
import { useNavigate } from "react-router-dom";
import "../App.css";
import { Link } from "react-router-dom"
import Navbar from './Navbar';

function TestHomePage() {
    const navigate = useNavigate()
    const navbar = Navbar;

  return (
    <>
    <Navbar />
    <div className="jumbotron text-center">
        <h1 className="display-3">Poll the Room!</h1>
        <h2 className="display-5">How Does it Work?</h2>
        <p className="lead">
            Welcome to Poll the Room! Please enter the Twitter query you would like sentiment analysis on. 
            If you have multiple queries or hashtags you would like to research, please separate them with a 
            comma. 
        </p>

        <hr className="my-4" />
        <h2 className='display-5'>Create Your Query Here</h2>
        <p className='lead'>
            Enter your query here. Please keep your query under 500 words or else it can't be processed!
            {/* Twitter Query search bar here */}

            Please enter a number of Tweets up to 5000
            {/* Number of Tweets bar here */}
            <button className='btn btn-success' onClick={() => navigate('/graphPage')}
                    >Start Search
            </button>
        </p>
    </div>
    </>
   
  )
}

export default TestHomePage