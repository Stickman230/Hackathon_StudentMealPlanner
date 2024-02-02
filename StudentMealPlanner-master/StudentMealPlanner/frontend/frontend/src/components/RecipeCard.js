import {useState, useEffect} from 'react';
import { Card, Button, Modal, Spinner } from 'react-bootstrap';


export default function RecipeCard({recipeNumber, handleQuickView,index,addSelectedRecipe}){
    console.log(recipeNumber)
    const [recipe, setRecipe] = useState({name:'loading'});
    useEffect(() => {
        //fetch the data from the api endpoint
        fetch("/getrecipe", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({recipeNumber: recipeNumber}),
        })
            .then((response) => response.json())
            .then((data) => {
                // console.log(data.recipe);
                //setOptions(data.recipes);
                setRecipe(data.recipe);
                
            })
            .catch((error) => {
                console.log(error);
            });
    }, []);
    return(
        <Card key={index} style={{ width: '18rem', margin: '10px' }}>
        <Card.Body>
          <Card.Title>{recipe.name}</Card.Title>
          <Button variant="primary" onClick={() => handleQuickView(recipeNumber)}>
            Quick View
          </Button>
          <Button variant="success" onClick={() => addSelectedRecipe(recipeNumber)}>
            Select
          </Button>
        </Card.Body>
      </Card>
    )
}