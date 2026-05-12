"""
models.py
---------
Data models for Pison Phone Store — a premium mobile phone retail platform.

Supabase SQL to create the tables:
------------------------------------

CREATE TABLE products (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name              TEXT NOT NULL,
    brand             TEXT NOT NULL,
    description       TEXT,
    image_file        TEXT,
    original_price    NUMERIC(10,2) NOT NULL,
    secondhand_price  NUMERIC(10,2) NOT NULL DEFAULT 0,
    stock_original    INT DEFAULT 10,
    stock_secondhand  INT DEFAULT 0,
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE orders (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id       UUID REFERENCES products(id),
    product_name     TEXT NOT NULL,
    quantity         INT NOT NULL DEFAULT 1,
    condition        TEXT DEFAULT 'brand_new',
    payment_method   TEXT CHECK (payment_method IN ('cash','gcash','credit_card','bank_transfer')) NOT NULL,
    unit_price       NUMERIC(10,2) NOT NULL,
    total_price      NUMERIC(10,2) NOT NULL,
    customer_name    TEXT,
    customer_email   TEXT,
    game_uid         TEXT,   -- used for customer phone number
    game_server      TEXT,   -- used for delivery address
    denom_label      TEXT,   -- used for phone variant (color/storage)
    status           TEXT DEFAULT 'pending',
    created_at       TIMESTAMPTZ DEFAULT NOW()
);

-- SEED DATA (run after creating tables):
INSERT INTO products (name, brand, description, original_price, secondhand_price, stock_original, stock_secondhand) VALUES
('iPhone 16 Pro Max', 'Apple', 'The most powerful iPhone ever. Titanium design, A18 Pro chip, and a revolutionary camera system with 5x optical zoom. Available in Black Titanium, White Titanium, Natural Titanium, and Desert Titanium.', 89990.00, 72000.00, 10, 5),
('Samsung Galaxy S25 Ultra', 'Samsung', 'Ultimate Android flagship with built-in S Pen, 200MP camera, and Snapdragon 8 Elite processor. Features titanium frame and AI-powered photography.', 79990.00, 62000.00, 8, 3),
('Google Pixel 9 Pro', 'Google', 'The smartest Pixel yet. Powered by Google Tensor G4 chip with industry-leading computational photography, 7 years of OS updates, and exclusive Google AI features.', 64990.00, 50000.00, 6, 2),
('OnePlus 13', 'OnePlus', 'Flagship killer with Snapdragon 8 Elite, Hasselblad triple camera, and 100W SuperVOOC charging. Premium build with Silk Glass back panel.', 49990.00, 38000.00, 12, 4),
('Xiaomi 15 Ultra', 'Xiaomi', 'Photography powerhouse featuring Leica Summilux optics, 1-inch main sensor, and HyperOS 2. Master your creativity with 50MP periscope telephoto.', 59990.00, 45000.00, 7, 2),
('OPPO Find X8 Pro', 'OPPO', 'Co-engineered with Hasselblad for cinematic photography. Features dual periscope cameras, a gorgeous curved display, and 80W SuperVOOC charging.', 54990.00, 42000.00, 9, 3);
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    id: Optional[str] = None
    name: str = ""
    brand: str = ""
    description: str = ""
    image_file: str = ""
    original_price: float = 0.0
    secondhand_price: float = 0.0
    stock_original: int = 10
    stock_secondhand: int = 0

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "description": self.description,
            "image_file": self.image_file,
            "original_price": self.original_price,
            "secondhand_price": self.secondhand_price,
            "stock_original": self.stock_original,
            "stock_secondhand": self.stock_secondhand,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            brand=data.get("brand", ""),
            description=data.get("description", ""),
            image_file=data.get("image_file", ""),
            original_price=float(data.get("original_price", 0)),
            secondhand_price=float(data.get("secondhand_price", 0)),
            stock_original=int(data.get("stock_original", 10)),
            stock_secondhand=int(data.get("stock_secondhand", 0)),
        )


@dataclass
class Order:
    id: Optional[str] = None
    product_id: Optional[str] = None
    product_name: str = ""
    quantity: int = 1
    condition: str = "brand_new"
    payment_method: str = "gcash"
    unit_price: float = 0.0
    total_price: float = 0.0
    customer_name: str = ""
    customer_email: str = ""
    game_uid: str = ""        # customer phone number
    game_server: str = ""     # delivery address
    denom_label: str = ""     # phone variant (color / storage)
    status: str = "pending"

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "condition": self.condition,
            "payment_method": self.payment_method,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "game_uid": self.game_uid,
            "game_server": self.game_server,
            "denom_label": self.denom_label,
            "status": self.status,
        }


@dataclass
class Inventory:
    id: Optional[str] = None
    product_id: Optional[str] = None
    stock_original: int = 10
    stock_secondhand: int = 0

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "stock_original": self.stock_original,
            "stock_secondhand": self.stock_secondhand,
        }