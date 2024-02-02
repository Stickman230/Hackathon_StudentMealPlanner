import React, { useState } from 'react';
import { Button, Col, Container, Row } from 'react-bootstrap';
import { FiChevronRight, FiChevronLeft } from 'react-icons/fi';

const SidePanel = ({setIsSidePanelOpen,Child,...props}) => {
  const [isPanelOpen, setIsPanelOpen] = useState(false);

  const handleTogglePanel = () => {
    setIsPanelOpen(!isPanelOpen);
    setIsSidePanelOpen(!isPanelOpen)
  };

  return (
    <Container fluid>
      <Row>
        {/* Button to Open Panel */}
        <Button
          variant="primary"
          onClick={handleTogglePanel}
          style={{
            position: 'fixed',
            left: '10px',
            top: '50%',
            transform: 'translateY(-50%)',
            zIndex: '999',
            width: '40px',
            height: '40px',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderRight: isPanelOpen ? '1px solid #ccc' : 'none', // Add border style
          }}
        >
          {isPanelOpen ? <FiChevronLeft /> : <FiChevronRight />}
        </Button>


        {/* Side Panel */}
        <Col
          xs={12}
          md={3}
          style={{
            position: 'fixed',
            top: '0',
            left: isPanelOpen ? '0' : '-250px',
            height: '100vh',
            width: '250px',
            overflowY: 'auto',
            transition: 'all 0.3s',
          }}
        >
          <div>
            
            {/* Add content for the side panel */}
            <Child {...props}/> {/*this is the child component that is passed in as a prop, and all other key word values are unpacked and passed to the child. 
                                for example <SidePanel setSidePanel = {x} child = {y} param1={z} param2={w}*, this would be the equivelent of <Child param1={x} param2={w}/> */}
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default SidePanel;
