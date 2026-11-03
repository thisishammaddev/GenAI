import asyncio
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator, model_validator


class Address(BaseModel):
    street: str
    city: str
    postal_code: str


class Customer(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: Address

    @field_validator("name")
    @classmethod
    def clean_customer_name(cls, value: str) -> str:
        # Normalize whitespace and casing for consistent customer records.
        return " ".join(value.split()).title()


class FoodItem(BaseModel):
    name: str
    quantity: int = Field(gt=0, le=10)
    price: float = Field(gt=0)


class Order(BaseModel):
    customer: Customer
    food_items: list[FoodItem] = Field(min_length=1)
    delivery_instructions: Optional[str] = None
    payment_status: Literal["pending", "paid", "failed"]

    @model_validator(mode="after")
    def require_instructions_for_large_order(self) -> "Order":
        total_amount = sum(item.quantity * item.price for item in self.food_items)
        if total_amount > 3000 and not self.delivery_instructions:
            raise ValueError("Orders above Rs. 3000 require delivery instructions.")
        return self


class OrderConfirmation(BaseModel):
    customer_name: str
    total_amount: float
    all_items_available: bool
    delivery_available: bool
    order_status: Literal["confirmed", "rejected"]
    message: str


class SmartFoodDeliveryAgent:
    def __init__(self) -> None:
        self.inventory: dict[str, int] = {
            "burger": 25,
            "pizza": 15,
            "pasta": 20,
            "fries": 50,
        }
        self.serviceable_cities = {"islamabad", "lahore", "karachi", "rawalpindi"}

    async def calculate_total(self, order: Order) -> float:
        await asyncio.sleep(0.15)
        return round(sum(item.quantity * item.price for item in order.food_items), 2)

    async def check_item_availability(self, order: Order) -> bool:
        await asyncio.sleep(0.2)
        return all(self.inventory.get(item.name.lower(), 0) >= item.quantity for item in order.food_items)

    async def check_delivery_availability(self, order: Order) -> bool:
        await asyncio.sleep(0.1)
        return order.customer.address.city.strip().lower() in self.serviceable_cities

    async def process_order(self, order: Order) -> OrderConfirmation:
        total_task = asyncio.create_task(self.calculate_total(order))
        item_task = asyncio.create_task(self.check_item_availability(order))
        delivery_task = asyncio.create_task(self.check_delivery_availability(order))

        total_amount, all_items_available, delivery_available = await asyncio.gather(
            total_task,
            item_task,
            delivery_task,
        )

        if all_items_available and delivery_available:
            status = "confirmed"
            message = "Order confirmed and will be processed shortly."
        elif not all_items_available:
            status = "rejected"
            message = "Order rejected because one or more items are unavailable."
        else:
            status = "rejected"
            message = "Order rejected because delivery is unavailable for this location."

        return OrderConfirmation(
            customer_name=order.customer.name,
            total_amount=total_amount,
            all_items_available=all_items_available,
            delivery_available=delivery_available,
            order_status=status,
            message=message,
        )


async def run_demo() -> None:
    agent = SmartFoodDeliveryAgent()

    order = Order(
        customer={
            "name": "Abraham Lincoln",
            "email": "abraham.lincoln@example.com",
            "phone": "0300-1234567",
            "address": {
                "street": "Street 10",
                "city": "Islamabad",
                "postal_code": "44000",
            },
        },
        food_items=[
            {"name": "Burger", "quantity": 2, "price": 650},
            {"name": "Pizza", "quantity": 1, "price": 1800},
        ],
        delivery_instructions="Leave at gate and call on arrival.",
        payment_status="paid",
    )

    confirmation = await agent.process_order(order)
    print(confirmation.model_dump_json(indent=2))


if __name__ == "__main__":
    try:
        asyncio.run(run_demo())
    except ValidationError as error:
        print(error)