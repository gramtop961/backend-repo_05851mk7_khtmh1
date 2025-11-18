"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Disaster relief app schemas

class Disaster(BaseModel):
    title: str = Field(..., description="Name of the disaster")
    description: str = Field(..., description="Short summary of the situation")
    location: str = Field(..., description="Affected location")
    severity: str = Field(..., description="Severity level: low/medium/high/critical")
    status: str = Field("ongoing", description="Status: ongoing/resolved/monitoring")
    date: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Reported date")

class Donation(BaseModel):
    name: str = Field(..., description="Donor full name")
    email: str = Field(..., description="Donor email")
    type: str = Field(..., description="Type of help: money/food/supplies")
    amount: Optional[float] = Field(None, ge=0, description="Amount in USD for money donations")
    items: Optional[str] = Field(None, description="List of items for food/supplies")
    message: Optional[str] = Field(None, description="Optional note from the donor")
    disaster_id: Optional[str] = Field(None, description="Related disaster id if applicable")

class Volunteer(BaseModel):
    name: str = Field(..., description="Volunteer full name")
    email: str = Field(..., description="Volunteer email")
    phone: Optional[str] = Field(None, description="Contact number")
    skills: Optional[List[str]] = Field(default=None, description="Skills to help (first aid, logistics, cooking, etc.)")
    availability: Optional[str] = Field(None, description="When they can help")
    location: Optional[str] = Field(None, description="Preferred location to help")
    disaster_id: Optional[str] = Field(None, description="Related disaster id if any")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
