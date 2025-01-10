import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
import '../styles/appNavbar.css'; // Custom CSS for styling

const AppNavbar = () => {
    return (
        <Navbar className="custom-navbar" expand="lg">
            <Container>
                {/* Logo/Brand Name */}
                <Navbar.Brand href="/" className="brand-name">
                    <img
                        src="/logo.png" // Path to your logo
                        alt="Uml2Code Logo"
                        width="35"
                        height="35"
                        className="d-inline-block align-top me-2"
                        />
                        Uml2Code
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="ms-auto">
                        <Nav.Link href="/">Home</Nav.Link>
                        <Nav.Link href="/features">Features</Nav.Link>
                        <Nav.Link href="/services">Services</Nav.Link>
                        <Nav.Link href="/work">Our Work</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
};

export default AppNavbar;
