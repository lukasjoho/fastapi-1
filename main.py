from typing import Optional
from fastapi import FastAPI, Path
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from fastapi import Query
# An API endpoint is the point of entry in a communication channel when two systems interact. It refers to touchpoints of communication between an APi and a server. 
app = FastAPI()

class Item(BaseModel):
	name: str
	price: float
	brand: Optional[str] = None

class UpdateItem(BaseModel):
	name: Optional[str] = None
	price: Optional[float] = None
	brand: Optional[str] = None

inventory = {}

# GET items

@app.get("/get-items")
def get_items():
	return inventory
	
# GET by id

@app.get("/get-item/{item_id}")
# Multiple path parameters
def get_item(item_id: int = Path(None, description="The ID of the item you would like to view.", gt=0)):
	return inventory[item_id]


# How to accept query parameters for your endpoint

# GET by name
@app.get("/get-by-name")
# Multiple path parameters
def get_item(name: str = Query(None, title="Name", description="Name of item.")):
	for item_id in inventory:
		if inventory[item_id].name == name:
			return inventory[item_id]
	raise HTTPException(status_code=404, detail="Item ID not found")

# CREATE
@app.post("/create-item/{item_ id}")
def create_item(item_id: int, item: Item):
	if item_id in inventory:
		raise HTTPException(status_code=400, detail="Item ID already exists")
	inventory[item_id] = item
	return inventory[item_id]  

# UPDATE
@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
	if item_id not in inventory:
		raise HTTPException(status_code=404, detail="Item ID does not exist")
	if item.name != None:
		inventory[item_id].name = item.name
	if item.price != None:
		inventory[item_id].price = item.price
	if item.brand != None:
		inventory[item_id].brand = item.brand
	return inventory[item_id]

# DELETE
@app.delete("/delete-item/{item_id}")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete")):
	 if item_id not in inventory:
		 return {"Error:" "Item ID not exists"}
	 del inventory[item_id]
	 return {"Success:" "Item successfully deleted!"}