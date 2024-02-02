import { useEffect,useState } from "react";
import './recipeData.css';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import NutritionalInfo from './NutritionalInfo.js';
import { Button } from "react-bootstrap";
function function_multiply(n1,d1,n2,d2){
    //multiplies two fractions
    //returns the numerator and denominator of the result
    let numerator = n1*n2;
    let denominator = d1*d2;
    //now we need to simplify the fraction
    //find the greatest common divisor
    let gcd = 1;
    for(let i=1;i<=Math.min(numerator,denominator);i++){
        if(numerator%i===0 && denominator%i===0){
            gcd = i;
        }
    }
    numerator = numerator/gcd;
    denominator = denominator/gcd;

    return [numerator,denominator];

}
export default function RecipeData({recipeNumber,addSelectedRecipe}){
    console.log('recipe data')
    console.log(recipeNumber);
    const [recipe, setRecipe] = useState(null);
    const [servings, setServings] = useState(null);
    console.log('SERVINGS ',servings)
    function changeServings (newServing) {
      // if the ingredient has quantity, we need to change it depending on the number of servings

        setServings(newServing);
        const fractionRegex = /\b(\d+)\/(\d+)\b/g;
        
        for (const [ingredient, details] of Object.entries(recipe.ingredients)) {
          var fractions =details.quantity.match(fractionRegex);
          if (fractions!==null){
          console.log(details.quantity)

          console.log('found fractions')
          console.log(fractions)
          let newFractions = fractions.map((fraction) => {
            const [numerator, denominator] = fraction.split("/");
            const [newNumerator, newDenominator] = function_multiply(
              numerator,
              denominator,
              newServing,
              servings
            );
            return `${newNumerator}/${newDenominator}`;
 
          });
         for(var fraction of fractions){
            details.quantity = details.quantity.replace(fraction,newFractions.shift());
          }
        }
        else{
          ;
          if(!isNaN(details.quantity)){
            details.quantity = `${details.quantity*(newServing/servings)}`;
            
          }
        }


      
        
      }
    }

    
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
                setServings(data.recipe.servings);
                
            })
            .catch((error) => {
                console.log(error);
            });
    }, [recipeNumber]);
    if(!recipe){
        return (
        <div>
        <p>loading</p>
        </div>
        )
        ; //this is a temporary solution, we should probably have a loading screen
    };
    const servingsArray = Array.from({ length: recipe.servings }, (_, index) => index + 1);
    return(
        
            <div className="recipe-container">
              <div className="header">
                <h1>{recipe.name}</h1>
                <Button variant="success" onClick={() => addSelectedRecipe(recipeNumber)}>Add Recipe</Button>
                <p className="source">Source: {recipe.source}</p>
              </div>
        
              <div className="time-servings">
                <p>Prep Time: {recipe.preptime} minutes</p>
                <p>Cook Time: {recipe.cooktime} minutes</p>
                {/* <p>Servings: {servings}</p> */}
                <label htmlFor="servings">Servings:</label>
                
              <select
                id="servings"
                value={servings}
                onChange={(e) => changeServings(parseInt(e.target.value))}
              >
                {servingsArray.map((number) => (
                  <option key={number} value={number}>
                    {number}
                  </option>
                ))}
              </select>

              <dropdown>

              </dropdown>
              </div>
        
              <div className="ingredients-container">
                <h2>Ingredients:</h2>
                <ul>
                  {Object.entries(recipe.ingredients).map(([ingredient, details]) => (
                    <li key={ingredient}>
                      {details.quantity} {ingredient}{" "}
                      {details.state && `(${details.state})`}
                    </li>
                  ))}
                </ul>
              </div>
        
              <div className="instructions-container">
                <h2>Instructions:</h2>
                <p>{recipe.instructions}</p>
              </div>
        
              {/* <div className="nutrition-info">
                <h2>Nutrition Information:</h2>
                <p>Calories: {recipe.calories}</p>
                <p>Fat: {recipe.fat}g</p>
                <p>Saturated Fat: {recipe.satfat}g</p>
                <p>Carbs: {recipe.carbs}g</p>
                <p>Fiber: {recipe.fiber}g</p>
                <p>Sugar: {recipe.sugar}g</p>
                <p>Protein: {recipe.protein}g</p>
              </div> */}
              <h2>Nutrition Information:</h2>

              <NutritionalInfo recipe={recipe} servings={servings}/>
        
              <div className="comments-container">
                <h2>Comments:</h2>
                <p>{recipe.comments}</p>
              </div>
        
              <div className="tags-container">
                <h2>Tags:</h2>
                <ul>
                  {recipe.tags.map((tag, index) => (
                    <li key={index}>{tag}</li>
                  ))}
                </ul>
              </div>
              </div>
    )
}