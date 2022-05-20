import React, { Component } from 'react';



export class Homepage extends Component {

    constructor(props) {
      super(props)
    
      this.state = {
         query: '',
         numTweets: '',

      }
    }
  render() {
      const { query, numTweets } = this.state
    return (
      <form onSubmit={this.handleSubmit}>
          <h1>Poll The Room</h1>
          <p>
            Welcome to Poll the Room! Find out what people are saying about a subject or hashtag on Twitter.
          </p>
          <div>
          <p>
            Enter your query below. Please keep your query under 500 words or else we can't process it!
          </p>
              <label>Twitter Query: </label>
              <input
              type='text'
              value={query}
              onChange={this.handleQueryEntry} />
          </div>
          <p>
              Please enter a number of tweets up to 5000
          </p>
          <div>
              <label>Number of Tweets: </label>
              <input 
              type='text'
              value={numTweets}
              onChange={this.handleNumTweetsChange}/>
          </div>

      </form>
    )
  }
}

export default Homepage