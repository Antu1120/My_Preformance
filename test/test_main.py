from fastapi.testclient import TestClient
from src.main import api, tickets, Ticket

client = TestClient(api)

# Setup function to clear tickets before each test
def setup_function():
    tickets.clear()

def test_index():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Ticket Booking System"}

def test_get_tickets_empty():
    """Test getting tickets when no tickets exist"""
    response = client.get("/ticket")
    assert response.status_code == 200
    assert response.json() == []

def test_add_ticket():
    """Test adding a new ticket"""
    ticket_data = {
        "id": 1,
        "flight_name": "AA123",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "New York"
    }
    response = client.post("/ticket", json=ticket_data)
    assert response.status_code == 200
    assert response.json() == ticket_data
    
    # Verify the ticket was added to the list
    assert len(tickets) == 1
    assert tickets[0].id == 1

def test_get_tickets_with_data():
    """Test getting tickets after adding one"""
    # First add a ticket
    ticket_data = {
        "id": 1,
        "flight_name": "AA123",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "New York"
    }
    client.post("/ticket", json=ticket_data)
    
    # Then get all tickets
    response = client.get("/ticket")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["flight_name"] == "AA123"

def test_update_ticket():
    """Test updating an existing ticket"""
    # First add a ticket
    ticket_data = {
        "id": 1,
        "flight_name": "AA123",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "New York"
    }
    client.post("/ticket", json=ticket_data)
    
    # Then update it
    updated_data = {
        "id": 1,
        "flight_name": "AA456",
        "flight_date": "2025-10-16",
        "flight_time": "15:30",
        "destination": "Los Angeles"
    }
    response = client.put("/ticket/1", json=updated_data)
    assert response.status_code == 200
    assert response.json() == updated_data
    
    # Verify the ticket was actually updated
    assert tickets[0].flight_name == "AA456"
    assert tickets[0].destination == "Los Angeles"

def test_update_nonexistent_ticket():
    """Test updating a ticket that doesn't exist"""
    updated_data = {
        "id": 999,
        "flight_name": "AA999",
        "flight_date": "2025-10-17",
        "flight_time": "16:30",
        "destination": "Chicago"
    }
    response = client.put("/ticket/999", json=updated_data)
    assert response.status_code == 200
    assert response.json() == {"error": "Ticket Not Found"}

def test_delete_ticket():
    """Test deleting an existing ticket"""
    # First add a ticket
    ticket_data = {
        "id": 1,
        "flight_name": "AA123",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "New York"
    }
    client.post("/ticket", json=ticket_data)
    
    # Then delete it
    response = client.delete("/ticket/1")
    assert response.status_code == 200
    assert response.json() == ticket_data
    
    # Verify the ticket was actually removed
    assert len(tickets) == 0

def test_delete_nonexistent_ticket():
    """Test deleting a ticket that doesn't exist"""
    response = client.delete("/ticket/999")
    assert response.status_code == 200
    assert response.json() == {"error": "Ticket not found, deletion failed"}