import './App.css';
import Homepage from './components/Homepage';

function App() {
  return (
    <div className="App">
      <header>Filler Header</header>
      <body>
      <img src={require('./images/filler.jpg')} width={200} height={200} />
        <Homepage />
      </body>
    </div>
  );
}

export default App;
