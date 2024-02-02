// // import RecipeCard from './RecipeCard';
// // export default function SelectedView({selected,setSelected}){
// //     function removeSelectedRecipe(index){
// //         const newSelected = [...selected];
// //         newSelected.splice(index, 1);
// //         setSelected(newSelected);
// //     }
// //     return(
// //         <div>
// //         {selected.map((recipeNumber, index) => (
// //             <Col key={index}>
// //                 <RecipeCard index={index} recipeNumber={recipeNumber} handleQuickView={handleQuickView} select ={addSelectedRecipe} />
// //             </Col>
// //             ))
// //         }
        
// //         </div>

// //     )


// // }

import React, { useState } from 'react';
import { Col, Row,Button, Form, Dropdown, DropdownButton, Card } from 'react-bootstrap';
import RecipeCard from './RecipeCard';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTrash } from '@fortawesome/free-solid-svg-icons';

export default function SelectedView({ selected, setSelected }) {
  const [numberOfMeals, setNumberOfMeals] = useState(1);
  const [selectedNutrient, setSelectedNutrient] = useState('protein');
  const [optimizedMenu, setOptimizedMenu] = useState([]);


  const handleDeleteRecipe = (index) => {
    var newSelected = [...selected];
    console.log(newSelected)
        console.log(`need to remove ${newSelected[index]} from ${newSelected}`)
    newSelected=newSelected.splice(index, 1);
    setSelected(newSelected);
  };

  const handleOptimizeMenu = () => {
    // Prepare the data to be sent to /optimiseMenu
    const requestData = {
      menuItems: selected,
      numberOfMeals: numberOfMeals,
      nutrient: selectedNutrient,
    };

    // Make a request to /optimiseMenu
    fetch('/optimiseMenu', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => response.json())
      .then((data) => {
        // Update the state with the optimized menu
        console.log(data.optimizedMenu)
        setOptimizedMenu(data.optimizedMenu);
      })
      .catch((error) => {
        console.error('Error optimizing menu:', error);
      });
  };

  return (
    <div>
      <div>
        {/* List of selected recipes */}
        {selected.map((recipeNumber, index) => (
          <Col key={index}>
            <Row>
            {/* <FontAwesomeIcon
              icon={faTrash}
              className="bin-icon"
              onClick={() => {handleDeleteRecipe(index)}}
            /> */}
            <RecipeCard index={index} recipeNumber={recipeNumber} handleQuickView={()=>{}} select={setSelected} />

          </Row>
          </Col>
        ))}
      </div>

      {/* Optimization controls */}
      <Col>
        <Form>
          <Form.Group controlId="numberOfMeals">
            <Form.Label>Number of Meals</Form.Label>
            <Form.Control
              type="number"
              value={numberOfMeals}
              onChange={(e) => setNumberOfMeals(e.target.value)}
            />
          </Form.Group>
          <Form.Group controlId="nutrientDropdown">
            <Form.Label>Select Nutrient</Form.Label>
            <DropdownButton
              title={selectedNutrient}
              onSelect={(eventKey) => setSelectedNutrient(eventKey)}
            >
              <Dropdown.Item eventKey="protein">Protein</Dropdown.Item>
              <Dropdown.Item eventKey="satfat">Saturated Fat</Dropdown.Item>
              <Dropdown.Item eventKey="carbs">Carbohydrates</Dropdown.Item>
              <Dropdown.Item eventKey="fiber">Fibre</Dropdown.Item>
              <Dropdown.Item eventKey="sugar">Sugar</Dropdown.Item>
              {/* Add more nutrient options as needed */}
            </DropdownButton>
          </Form.Group>
          <Button variant="primary" onClick={handleOptimizeMenu}>
            Optimize
          </Button>
        </Form>
      </Col>

      {/* Optimized menu cards */}
      <div>
        {optimizedMenu.length!==0?<h2>{`Optimal Menu Of ${numberOfMeals} Recipe${numberOfMeals>1?'s':''}`}</h2>:null}
        {optimizedMenu.map((itemId) => (
          <Col key={itemId}>
            {/* <Card bg="success" text="white">
              <Card.Body>
                <Card.Text>{`Optimized Menu Item ${itemId.name}`}</Card.Text>
              </Card.Body>
            </Card> */}
            <RecipeCard recipeNumber ={itemId.id} handleQuickView ={()=>{}} index={1} addSelectedRecipe={()=>{}}></RecipeCard>
          </Col>
        ))}
      </div>
    </div>
  );
}


// import { Col, Button, Form, Dropdown, DropdownButton } from 'react-bootstrap';
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
// import { faTrash } from '@fortawesome/free-solid-svg-icons';
// import RecipeCard from './RecipeCard';




