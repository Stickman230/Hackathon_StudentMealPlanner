
import DropdownSearch from "./DropdownSearch";
import RecipeData from "./RecipeData";
import React, { useState, useEffect } from 'react';

import Button from 'react-bootstrap/Button';
import { Card, Col, Container, Row } from 'react-bootstrap';
import { Offcanvas } from 'react-bootstrap';
import {Tabs} from 'react-bootstrap';
import {Tab} from 'react-bootstrap';

import { FaShoppingBag } from 'react-icons/fa';

import SearchRecipeByName from "./SearchRecipeByName";

import IngredientSearch from "./IngredientsList";
import SearchRecipeByIngredients from "./SearchRecipeByIngredients";
import SelectedView from "./SelectedView";

export default function ItemSearchAndDisplayPage() {
    const [ingredients, setIngredient] = useState([]);
    const [isSidePanelOpen, setIsSidePanelOpen] = useState(false);
    const [page, setPage] = useState('');
    const [selectedRecipe, setSelectedRecipe] = useState([]);
    const addIngredient = (inputValue) => {
      setIngredient([...ingredients, inputValue]);
    };
    function addSelectedRecipe(recipe){
        setSelectedRecipe([...selectedRecipe, recipe]);
    }
  
    const handleTabSelect = (key) => {
      // If the "ingredients list" tab is clicked, open the Offcanvas
      if (key === "ingredientsList") {
        setIsSidePanelOpen(true);
      } else {
        // If a different tab is clicked, update the page state
        setPage(key);
        // Close the Offcanvas
        setIsSidePanelOpen(false);
      }
    };
  
    return (
      <Container fluid style={{ overflow: 'hidden', position: 'relative' }}>
        {/* Offcanvas */}
        <Offcanvas show={isSidePanelOpen} onHide={() => setIsSidePanelOpen(false)}>
          <Offcanvas.Header closeButton>
            <Offcanvas.Title>Ingredients</Offcanvas.Title>
          </Offcanvas.Header>
          <Offcanvas.Body>
            <IngredientSearch ingredients={ingredients} setIngredients={setIngredient} />
          </Offcanvas.Body>
        </Offcanvas>
  
        {/* Main Content */}
        <Row>
          <Col xs={12}>
            <Tabs
              id="controlled-tab-example"
              activeKey={page}
              onSelect={handleTabSelect}
              className="mb-3"
            >
              <Tab eventKey="ingredientsList" title="Ingredients">
                {/* Content for the "ingredients list" tab */}
              </Tab>
              <Tab eventKey="SBname" title="Search By Recipe Name">
                {/* to show when this tab is clicked */}
                <SearchRecipeByName addSelectedRecipe = {addSelectedRecipe}/>
              </Tab>
              <Tab eventKey="SBingredients" title="Search By Ingredients I Have">
                <SearchRecipeByIngredients addSelectedRecipe = {addSelectedRecipe} ingredients={ingredients}/>
              </Tab>
              <Tab eventKey="shoppingBag" title={<><FaShoppingBag /> Short Listed</>}>
                <SelectedView selected={selectedRecipe} setSelected={setSelectedRecipe} />
              </Tab>
            </Tabs>
          </Col>
        </Row>
      </Container>
    );
  }
  


