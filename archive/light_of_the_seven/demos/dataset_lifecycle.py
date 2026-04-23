"""
GFashion ETL Pipeline
====================

A structured, object-oriented ETL pipeline for the GFashion dataset.
Follows the Medallion Architecture principles (Bronze/Silver/Gold) adapted for GRID.

Usage:
    etl = GFashionETL()
    etl.run_pipeline()
"""

import logging
import sys
import uuid
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from vinci_code.core.config import settings
from vinci_code.database.models import Event
from vinci_code.database.models_gfashion import Customer, Order, OrderItem, Product
from vinci_code.database.session import SessionLocal

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class GFashionETL:
    """
    Encapsulates the Extract-Transform-Load logic for the GFashion domain.
    """

    def __init__(self, session: Session = None):
        self.session = session or SessionLocal()
        self.run_id = str(uuid.uuid4())[:8]

    def _log_step(self, step_name: str):
        logger.info(f"\n[{step_name}] Starting step (RunID: {self.run_id})...")

    def ingest_reference_data(self) -> Dict[str, int]:
        """
        Stage 1: Ingestion (Bronze/Silver)
        Creates or updates reference data (Products, Customers).
        """
        self._log_step("INGESTION")

        # Products (Reference Data)
        products = [
            Product(
                product_id="P001",
                name="Neural Network Hoodie",
                category="Apparel",
                brand="GridWear",
                price=Decimal("59.99"),
            ),
            Product(
                product_id="P002",
                name="Quantum Coffee Mug",
                category="Accessories",
                brand="GridHome",
                price=Decimal("15.50"),
            ),
            Product(
                product_id="P003",
                name="Data Stream Sneakers",
                category="Footwear",
                brand="GridActive",
                price=Decimal("120.00"),
            ),
        ]

        # Customers (Master Data)
        customers = [
            Customer(customer_id="C001", email="alice@example.com", country="USA"),
            Customer(customer_id="C002", email="bob@example.com", country="UK"),
        ]

        for p in products:
            self.session.merge(p)
        for c in customers:
            self.session.merge(c)

        self.session.commit()
        logger.info(
            f"    ✓ Merged {len(products)} products and {len(customers)} customers"
        )
        return {"products": len(products), "customers": len(customers)}

    def process_transactions(self) -> Order:
        """
        Stage 2: Operation (Silver)
        Simulates business logic and transaction processing.
        """
        self._log_step("OPERATION")

        # Fetch reference data
        customer = self.session.get(Customer, "C001")
        p1 = self.session.get(Product, "P001")
        p2 = self.session.get(Product, "P002")

        if not all([customer, p1, p2]):
            raise ValueError("Missing reference data for transaction")

        # Business Logic: Create Order
        order_id = f"ORD-{self.run_id}"
        qty1, qty2 = 1, 2
        total = (p1.price * qty1) + (p2.price * qty2)

        new_order = Order(
            order_id=order_id,
            customer_id=customer.customer_id,
            order_status="COMPLETED",
            total_amount=total,
            order_timestamp=datetime.now(UTC),
        )

        items = [
            OrderItem(
                order_id=order_id,
                line_number=1,
                product_id=p1.product_id,
                quantity=qty1,
                unit_price=p1.price,
            ),
            OrderItem(
                order_id=order_id,
                line_number=2,
                product_id=p2.product_id,
                quantity=qty2,
                unit_price=p2.price,
            ),
        ]

        self.session.add(new_order)
        self.session.add_all(items)
        self.session.commit()

        logger.info(f"    ✓ Created Order {order_id} for {customer.email} (${total})")

        # Link to GRID Event System
        self._emit_grid_event(new_order, items)

        return new_order

    def _emit_grid_event(self, order: Order, items: List[OrderItem]):
        """Helper to emit GRID system events."""
        event = Event(
            event_type="ORDER_PLACED",
            source="GFashionETL",
            raw_text=f"Order {order.order_id} placed by {order.customer_id}",
            data={
                "order_id": order.order_id,
                "amount": float(order.total_amount),
                "items_count": len(items),
                "run_id": self.run_id,
            },
        )
        self.session.add(event)
        self.session.commit()
        logger.info(f"    ✓ Emitted GRID Event: {event.event_type}")

    def generate_insights(self) -> List[Any]:
        """
        Stage 3: Analysis (Gold)
        Aggregates data to derive business insights.
        """
        self._log_step("ANALYSIS")

        stmt = (
            select(
                Product.category,
                func.sum(OrderItem.quantity * OrderItem.unit_price).label("revenue"),
            )
            .join(OrderItem, Product.product_id == OrderItem.product_id)
            .group_by(Product.category)
            .order_by(func.sum(OrderItem.quantity * OrderItem.unit_price).desc())
        )

        results = self.session.execute(stmt).all()

        logger.info("    📊 Revenue by Category:")
        for category, revenue in results:
            logger.info(f"       - {category}: ${revenue:,.2f}")

        return results

    def run_pipeline(self):
        """Execute the full pipeline."""
        logger.info(f"🚀 Starting GFashion ETL Pipeline (RunID: {self.run_id})")
        try:
            self.ingest_reference_data()
            self.process_transactions()
            self.generate_insights()
            logger.info("\n✨ Pipeline Completed Successfully")
        except Exception as e:
            self.session.rollback()
            logger.error(f"❌ Pipeline Failed: {e}")
            raise
        finally:
            self.session.close()


if __name__ == "__main__":
    etl = GFashionETL()
    etl.run_pipeline()
