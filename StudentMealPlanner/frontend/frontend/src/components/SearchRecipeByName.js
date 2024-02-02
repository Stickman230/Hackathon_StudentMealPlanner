import Button from 'react-bootstrap/Button';
import { Card, Col, Container, Row } from 'react-bootstrap';
import { Offcanvas } from 'react-bootstrap';

import DropdownSearch from "./DropdownSearch";
import RecipeData from "./RecipeData";

import React, { useState, useEffect } from 'react';


export default function SearchRecipeByName({addSelectedRecipe}){
    const [similarRecipes, setSimilarRecipes] = useState(null);
    const [recipeNumber, setRecipeNumber] = useState(null);
    function onViewMore(){
        //this function is called when the user clicks the "view similar recipes" button
        //it will display the next recipe in the list of similar recipes
        if(recipeNumber===null){
            alert('Please select a recipe first');
        }
        else{
            fetch('/getsimilarrecipe',{
                body: JSON.stringify({recipeNumber: recipeNumber}),
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                },
            }).then((response) => response.json()).then((data) => {
                console.log(data);
                setSimilarRecipes(data.recipe);
            })
        }
    }
    return(
        <div>
            <DropdownSearch APIEndPoint="/searchrecipes" setRecipeNumber={setRecipeNumber} />
            {recipeNumber === null ? null : <Button variant='info' onClick={onViewMore}>View similar recipes</Button>}
            {similarRecipes === null ? null : (
            <Row style={{ overflow: 'auto' }}>
            {similarRecipes.map((recipe, index) => (
                <Col key={index} xs={12} md={6} lg={4}>
                <Card>
                    <Card.Body>
                    <Card.Title>{recipe.name}</Card.Title>
                    {/* Add additional card content as needed */}
                    </Card.Body>
                </Card>
                </Col>
            ))}
            </Row>
            )}
            {recipeNumber === null ? null : <RecipeData recipeNumber={recipeNumber} addSelectedRecipe={addSelectedRecipe}></RecipeData>}
        </div>
    );
}
