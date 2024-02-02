import React, {useState, useEffect} from 'react';
import { Dropdown, Form } from 'react-bootstrap';
export default function DropdownSearch({APIEndPoint,setRecipeNumber}){
    //takes in the api endpoint to send the current search query to
    //expects the api to return a list of options to display
    //setRecipeNumber is a function that allowes the index of the chosen recipe to be passed back to the parent component
    const [searchQuery, setSearchQuery] = useState("");
    const [options, setOptions] = useState([]);
    useEffect(() => {
        //fetch the data from the api endpoint
        fetch(APIEndPoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({searchQuery: searchQuery}),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data.recipes);
                setOptions(data.recipes);
                
            })
            .catch((error) => {
                console.log(error);
            });
    }, [searchQuery]);// [searchQuery] is the dependency array, which means that the effect will only run if searchQuery changes, which happens when the user types something
    function handleView(){
        if(options.length!==1){
            //it means the user hasnt selected a recipe
            alert("Please select a recipe");
            return
        }
        console.log('id to be added ')
        console.log(options[0].index);
        setRecipeNumber(options[0].index);
    }
    return (
        <div>
          <Form>
            <Form.Group>
              <Form.Label>Select a recipe:</Form.Label>
              <Dropdown>
                <Form.Control
                  list="fruits"
                  id="fruitInput"
                  name="fruit"
                  placeholder="Type to search..."
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <datalist id="fruits">
                  {options.map((option, index) => (
                    <option key={index} value={option.title} />
                  ))}
                </datalist>
              </Dropdown>
            </Form.Group>
          </Form>
    
          <button onClick={() => handleView()}>View</button>
        </div>
      );
}