import DropdownSearch from "./DropdownSearch"
import {useState} from 'react';

import { InputGroup, FormControl, Button, Badge, Card, CloseButton } from 'react-bootstrap';

const IngredientSearch = ({ ingredients,setIngredients }) => {
  const addIngredient = (inputValue) => {
    setIngredients([...ingredients, inputValue]);
  };
    console.log(ingredients);
  const [inputValue, setInputValue] = useState('');

  const handleAddIngredient = () => {
    if (inputValue.trim() !== '') {
      // Create a new array with the current ingredients and the new ingredient
    //   const newIngredients = [...ingredients, inputValue.trim()];
      addIngredient(inputValue.trim());
      setInputValue('');
    }
  };

  const handleRemoveIngredient = (index) => {
    const newIngredients = [...ingredients];
    newIngredients.splice(index, 1);
    console.log('new ingreds')
    console.log(newIngredients);
    setIngredients(newIngredients);
  };
  
  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleAddIngredient();
    }
  };

  return (
    <div>
        <h3>Ingredients</h3>
      <InputGroup className="mb-3">
        <FormControl
          placeholder="Enter ingredient..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <Button variant="primary" onClick={handleAddIngredient}>
          Add
        </Button>
      </InputGroup>

      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        {ingredients.map((ingredient, index) => (
          <Card key={index} bg="purple" text="white" style={{ margin: '4px' }}>
            <Card.Body>
              <Badge bg="secondary">{ingredient}</Badge>
              <CloseButton onClick={() => handleRemoveIngredient(index)} />
            </Card.Body>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default IngredientSearch;
