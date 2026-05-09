"""
models.py
---------
Data models for GameTop — a Codashop-style game top-up platform.

Supabase SQL to create the tables:
------------------------------------

CREATE TABLE products (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    brand       TEXT NOT NULL,
    description TEXT,
    image_file  TEXT,
    original_price    NUMERIC(10,2) NOT NULL,
    secondhand_price  NUMERIC(10,2) NOT NULL DEFAULT 0,
    stock_original    INT DEFAULT 999,
    stock_secondhand  INT DEFAULT 0,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE orders (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id      UUID REFERENCES products(id),
    product_name    TEXT NOT NULL,
    quantity        INT NOT NULL DEFAULT 1,
    condition       TEXT DEFAULT 'original',
    payment_method  TEXT CHECK (payment_method IN ('cash','gcash','credit_card','bank_transfer')) NOT NULL,
    unit_price      NUMERIC(10,2) NOT NULL,
    total_price     NUMERIC(10,2) NOT NULL,
    customer_name   TEXT,
    customer_email  TEXT,
    game_uid        TEXT,
    game_server     TEXT,
    denom_label     TEXT,
    status          TEXT DEFAULT 'pending',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- SEED DATA (run after creating tables):
INSERT INTO products (name, brand, description, original_price, secondhand_price, stock_original) VALUES
('Mobile Legends', 'MOONTON', 'Top up Diamonds for Mobile Legends: Bang Bang. Instant delivery to your account.', 20.00, 0, 999),
('Call of Duty Mobile', 'Activision', 'Top up COD Points for Call of Duty Mobile. Buy bundles, skins, and Battle Pass.', 39.00, 0, 999),
('Valorant', 'Riot Games', 'Top up Valorant Points for exclusive skins and agents. PC tactical shooter.', 99.00, 0, 999),
('Dota 2', 'Valve', 'Top up Dota Coins for Battle Pass, sets, and cosmetics in Dota 2.', 55.00, 0, 999),
('Clash of Clans', 'Supercell', 'Top up Gems for Clash of Clans. Build your village and crush your enemies!', 39.00, 0, 999),
('PUBG Mobile', 'Krafton', 'Top up Unknown Cash (UC) for PUBG Mobile. Get skins, outfits, and Royal Pass.', 39.00, 0, 999);
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
    stock_original: int = 999
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
            stock_original=int(data.get("stock_original", 999)),
            stock_secondhand=int(data.get("stock_secondhand", 0)),
        )


@dataclass
class Order:
    id: Optional[str] = None
    product_id: Optional[str] = None
    product_name: str = ""
    quantity: int = 1
    condition: str = "original"
    payment_method: str = "gcash"
    unit_price: float = 0.0
    total_price: float = 0.0
    customer_name: str = ""
    customer_email: str = ""
    game_uid: str = ""        # In-game User ID
    game_server: str = ""     # Server/Zone (for ML, PUBG, etc.)
    denom_label: str = ""     # e.g. "112 💎", "60 UC"
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
    stock_original: int = 999
    stock_secondhand: int = 0

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "stock_original": self.stock_original,
            "stock_secondhand": self.stock_secondhand,
        }