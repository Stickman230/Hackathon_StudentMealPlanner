import logo from './logo.svg';
import './App.css';
import DropdownSearch from './components/DropdownSearch.js';
import ItemSearchAndDisplayPage from './components/ItemSearchAndDisplayPage.js';
import 'bootstrap/dist/css/bootstrap.min.css';//this imports the bootstrap css file for the project globally
// this replaces the need to import it in HTML
// Need to import every occurance of the component as it auto inserts the classes, and provides some js functionality

function App() {
  return (
    <div className="App">
      {/* <DropdownSearch APIEndPoint="/searchrecipes"/> */}

      <ItemSearchAndDisplayPage/>
      

    </div>
  );
}

export default App;
