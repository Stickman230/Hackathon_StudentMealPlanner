export default function NutritionalInfo({recipe,servings}){
    const reference_servings = parseInt(recipe.servings);
    console.log(recipe)
    console.log(' servings',servings)
    return(
        
        <div className="nutrition-info">
            <p>Calories: {parseFloat(recipe.calories)*(parseFloat(servings)/reference_servings)}</p>
            <p>Fat: {parseFloat(recipe.fat)*(servings/reference_servings)}g</p>
            <p>Saturated Fat: {parseFloat(recipe.satfat)*(servings/reference_servings)}g</p>
            <p>Carbs: {parseFloat(recipe.carbs)*(servings/reference_servings)}g</p>
            <p>Fiber: {parseFloat(recipe.fiber)*(servings/reference_servings)}g</p>
            <p>Sugar: {parseFloat(recipe.sugar)*(servings/reference_servings)}g</p>
            <p>Protein: {parseFloat(recipe.protein)*(servings/reference_servings)}g</p>
      </div>
    )
}