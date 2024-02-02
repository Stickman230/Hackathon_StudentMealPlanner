import {useEffect,useState} from 'react';
import { Card, Button, Modal,Spinner,Row,Col } from 'react-bootstrap';
import RecipeCard from './RecipeCard';
import RecipeData from './RecipeData';
export default function SearchRecipeByIngredients({ingredients,addSelectedRecipe}){
    console.log("ingredients")
    console.log(ingredients)
    
    const [recipes, setRecipes] = useState(null);
    useEffect(() => {
        fetch('/searchrecipesbyingredients',{
            body: JSON.stringify({ingredients: ingredients}),
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
        }).then((response) => response.json()).then((data) => {
            console.log(data);
            setRecipes(data.recipe);
        })
    }
    ,[ingredients]);
    //when a user clicks on a recipe, it will display the recipe in a new tab

    const [selectedRecipe, setSelectedRecipe] = useState(null);
    const [showModal, setShowModal] = useState(false);
  
    const handleQuickView = (recipe) => {
      setSelectedRecipe(recipe);
      setShowModal(true);
    };
  
    const handleCloseModal = () => {
      setShowModal(false);
    };
  
    return (
        <div>
            <p>These are recipes that, given the ingredients you've given to us, are the best for you</p>
            {/* gotta be a better way to do this
            if recipes === null, then display spinner because it hasn't loaded yet
            if recipes is empty, then display "no recipes found"
            otherwise, display the recipes */}
            {recipes !== null ? (
                ingredients.length > 0 ? (
                    recipes.length > 0 ? (
                    <Row xs={1} md={2} lg={5} className="g-4">
                        {recipes.map((recipeNumber, index) => (
                        <Col key={index}>
                            <RecipeCard index={index} recipeNumber={recipeNumber} handleQuickView={handleQuickView} addSelectedRecipe ={addSelectedRecipe} />
                        </Col>
                        ))}
                    </Row>
                    ) : (
                    <p>No recipes found</p>
                    )
                ) : (
                    <p>Please add ingredients to search</p>
                )
                ) : (
                  <div>
                    <p>Please add ingredients to search</p>
                <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                </Spinner>
                </div>
                )}

  
        {/* Modal for Quick View */}
        <Modal show={showModal} onHide={handleCloseModal}>
          <Modal.Header closeButton>
            <Modal.Title>{selectedRecipe?.title}</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            {/* Render the detailed recipe view inside the modal */}
            {selectedRecipe && (
              <div>
                {/* Add recipe details here */}
                <RecipeData recipeNumber={selectedRecipe} />
                {/* Add more details as needed */}
              </div>
            )}
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={handleCloseModal}>
              Close
            </Button>
          </Modal.Footer>
        </Modal>
      </div>
      );
    
    };
  
    
    

