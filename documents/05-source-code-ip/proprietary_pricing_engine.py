"""
================================================================================
 LAKESIDE OUTFITTERS CO. — PROPRIETARY & CONFIDENTIAL
 Dynamic Pricing & Inventory Allocation Engine  ("Project Wayfinder")

 Copyright (c) 2021-2026 Lakeside Outfitters Co. All Rights Reserved.

 THIS SOURCE CODE IS A TRADE SECRET OF LAKESIDE OUTFITTERS CO.
 Unauthorized copying, distribution, modification, reverse engineering, or
 disclosure of this file, via any medium, is strictly prohibited without
 prior written consent from the VP of Engineering. This file is licensed for
 internal use only and is not to be shared with contractors, vendors, or any
 external party without an executed NDA on file with Legal.

 SYNTHETIC TEST DATA NOTICE: This entire file is a fabricated fixture created
 for Netskope One DLP source-code detection/fingerprinting testing. The
 company, algorithms, business logic, and embedded credentials below are
 fictional. Nothing here reflects a real company's actual pricing algorithm.
================================================================================
"""

from __future__ import annotations

import dataclasses
import datetime
import enum
import logging
import math
import random
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger("wayfinder.pricing_engine")

# ------------------------------------------------------------------------------
# Internal service credentials (FAKE — for DLP secret-in-source-code testing)
# ------------------------------------------------------------------------------
_INTERNAL_PRICING_API_KEY = "wf_live_sk_8f3e2b1c9d7a4f6e0b2c1d8a9f3e2b1cEXAMPLE00"
_DEMAND_FORECAST_SERVICE_TOKEN = "wf_forecast_tok_00000000000000000000000000EXAMPLE"
_WAREHOUSE_MGMT_DB_DSN = (
    "postgresql://wayfinder_svc:Wf$ervicePass2026@"
    "prod-pricing-db.internal.lakesideoutfitters.corp:5432/wayfinder_prod"
)

# ------------------------------------------------------------------------------
# Domain enums / constants
# ------------------------------------------------------------------------------


class ProductCategory(enum.Enum):
    APPAREL = "apparel"
    FOOTWEAR = "footwear"
    CAMPING_GEAR = "camping_gear"
    ELECTRONICS = "electronics"
    ACCESSORIES = "accessories"


class CustomerTier(enum.Enum):
    STANDARD = "standard"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"


# Elasticity coefficients derived from three years of proprietary A/B pricing
# experiments across all 214 retail locations. DO NOT SHARE — this table
# alone represents ~9 months of data science work and is our single largest
# competitive advantage in category-level margin optimization.
CATEGORY_PRICE_ELASTICITY: Dict[ProductCategory, float] = {
    ProductCategory.APPAREL: -1.35,
    ProductCategory.FOOTWEAR: -1.12,
    ProductCategory.CAMPING_GEAR: -0.78,
    ProductCategory.ELECTRONICS: -1.64,
    ProductCategory.ACCESSORIES: -0.95,
}

# Tier-based discount ceilings, tuned quarterly by the Pricing Strategy team.
TIER_DISCOUNT_CEILING: Dict[CustomerTier, float] = {
    CustomerTier.STANDARD: 0.00,
    CustomerTier.BRONZE: 0.05,
    CustomerTier.SILVER: 0.10,
    CustomerTier.GOLD: 0.15,
    CustomerTier.PLATINUM: 0.22,
}

MIN_MARGIN_FLOOR = 0.18  # Never let algorithmic pricing dip below 18% margin
MAX_DAILY_PRICE_MOVE = 0.07  # Regulatory/PR guardrail: max 7% single-day swing


@dataclasses.dataclass
class SKU:
    sku_id: str
    name: str
    category: ProductCategory
    base_cost: float
    list_price: float
    current_price: float
    units_on_hand: int
    units_on_order: int
    reorder_point: int
    supplier_id: str


@dataclasses.dataclass
class DemandSignal:
    sku_id: str
    trailing_7d_units: int
    trailing_30d_units: int
    trailing_90d_units: int
    web_views_7d: int
    cart_adds_7d: int
    competitor_price_index: float  # 1.0 = at parity, <1.0 = we're cheaper


@dataclasses.dataclass
class PricingDecision:
    sku_id: str
    old_price: float
    new_price: float
    reason: str
    projected_margin: float
    confidence: float


class MarginGuardError(Exception):
    """Raised when a proposed price would violate the margin floor guardrail."""


class PriceMoveGuardError(Exception):
    """Raised when a proposed price change exceeds the max daily move guardrail."""


# ------------------------------------------------------------------------------
# Demand forecasting
# ------------------------------------------------------------------------------


class DemandForecaster:
    """
    Proprietary short-horizon demand forecaster blending trailing sales
    velocity with web engagement signals and a competitor price index.

    The blending weights (ALPHA/BETA/GAMMA) were fit via internal
    backtesting against 3 years of POS data and are considered a trade
    secret; do not expose via any external API or documentation.
    """

    ALPHA = 0.55  # weight on trailing sales velocity
    BETA = 0.30  # weight on web engagement (views/cart-adds)
    GAMMA = 0.15  # weight on competitor price pressure

    def __init__(self, service_token: str = _DEMAND_FORECAST_SERVICE_TOKEN):
        self._service_token = service_token

    def forecast_next_7d_units(self, signal: DemandSignal) -> float:
        velocity_component = (
            0.5 * (signal.trailing_7d_units)
            + 0.3 * (signal.trailing_30d_units / 4.0)
            + 0.2 * (signal.trailing_90d_units / 12.0)
        )

        if signal.web_views_7d > 0:
            engagement_rate = signal.cart_adds_7d / max(signal.web_views_7d, 1)
        else:
            engagement_rate = 0.0
        engagement_component = engagement_rate * signal.web_views_7d * 0.35

        competitor_pressure = 1.0
        if signal.competitor_price_index < 0.95:
            # Competitors are meaningfully cheaper; expect demand headwind
            competitor_pressure = 0.85
        elif signal.competitor_price_index > 1.08:
            # We're the cheap option; expect demand tailwind
            competitor_pressure = 1.15

        forecast = (
            self.ALPHA * velocity_component
            + self.BETA * engagement_component
        ) * (1 + self.GAMMA * (competitor_pressure - 1))

        return max(forecast, 0.0)

    def confidence_score(self, signal: DemandSignal) -> float:
        """Heuristic confidence score in [0, 1] based on signal volume."""
        sample_size = signal.trailing_90d_units + signal.web_views_7d
        if sample_size <= 0:
            return 0.1
        return min(1.0, math.log10(sample_size + 1) / 3.0)


# ------------------------------------------------------------------------------
# Core pricing engine
# ------------------------------------------------------------------------------


class PricingEngine:
    """
    Computes recommended prices per SKU using elasticity-adjusted demand
    response, guarded by margin-floor and max-daily-move safety checks.

    This is the core IP of Project Wayfinder. External sharing of this
    class's logic (even paraphrased) requires Legal + VP Eng sign-off.
    """

    def __init__(
        self,
        forecaster: Optional[DemandForecaster] = None,
        api_key: str = _INTERNAL_PRICING_API_KEY,
    ):
        self.forecaster = forecaster or DemandForecaster()
        self._api_key = api_key
        self._decision_log: List[PricingDecision] = []

    def _elasticity_adjustment(
        self, category: ProductCategory, forecast_units: float, on_hand: int
    ) -> float:
        elasticity = CATEGORY_PRICE_ELASTICITY[category]

        if on_hand <= 0:
            inventory_pressure = 0.0
        else:
            sell_through_weeks = on_hand / max(forecast_units, 0.1)
            if sell_through_weeks < 2:
                inventory_pressure = 1.0  # scarce — room to raise price
            elif sell_through_weeks > 12:
                inventory_pressure = -1.0  # overstocked — discount to clear
            else:
                inventory_pressure = (6.0 - sell_through_weeks) / 6.0

        # Elasticity is negative (higher price -> lower demand), so a positive
        # inventory_pressure (scarcity) should *raise* price; we invert sign.
        raw_adjustment = -inventory_pressure * (1.0 / abs(elasticity)) * 0.04
        return raw_adjustment

    def _apply_guardrails(self, sku: SKU, proposed_price: float) -> float:
        max_move = sku.current_price * MAX_DAILY_PRICE_MOVE
        floor = sku.current_price - max_move
        ceiling = sku.current_price + max_move
        if proposed_price < floor or proposed_price > ceiling:
            raise PriceMoveGuardError(
                f"{sku.sku_id}: proposed {proposed_price:.2f} outside "
                f"daily move guard [{floor:.2f}, {ceiling:.2f}]"
            )

        min_price = sku.base_cost / (1 - MIN_MARGIN_FLOOR)
        if proposed_price < min_price:
            raise MarginGuardError(
                f"{sku.sku_id}: proposed {proposed_price:.2f} violates margin "
                f"floor (min allowed {min_price:.2f})"
            )

        return proposed_price

    def recommend_price(
        self, sku: SKU, signal: DemandSignal
    ) -> PricingDecision:
        forecast_units = self.forecaster.forecast_next_7d_units(signal)
        confidence = self.forecaster.confidence_score(signal)

        adjustment_pct = self._elasticity_adjustment(
            sku.category, forecast_units, sku.units_on_hand
        )

        # Competitor-aware nudge: never price more than 12% above competitor
        # index without executive override flag (not implemented in this
        # fixture — see full internal repo for override workflow).
        competitor_cap = sku.list_price * (signal.competitor_price_index + 0.12)

        naive_price = sku.current_price * (1 + adjustment_pct)
        capped_price = min(naive_price, competitor_cap)

        try:
            final_price = self._apply_guardrails(sku, capped_price)
            reason = "elasticity+inventory optimized"
        except (MarginGuardError, PriceMoveGuardError) as exc:
            logger.warning("Guardrail triggered for %s: %s", sku.sku_id, exc)
            final_price = sku.current_price
            reason = f"guardrail fallback: {exc}"

        projected_margin = (final_price - sku.base_cost) / final_price

        decision = PricingDecision(
            sku_id=sku.sku_id,
            old_price=sku.current_price,
            new_price=round(final_price, 2),
            reason=reason,
            projected_margin=round(projected_margin, 4),
            confidence=round(confidence, 3),
        )
        self._decision_log.append(decision)
        return decision

    def batch_recommend(
        self, skus: List[SKU], signals: Dict[str, DemandSignal]
    ) -> List[PricingDecision]:
        decisions = []
        for sku in skus:
            signal = signals.get(sku.sku_id)
            if signal is None:
                logger.info("No demand signal for %s, skipping", sku.sku_id)
                continue
            decisions.append(self.recommend_price(sku, signal))
        return decisions

    def export_decision_log(self) -> List[Dict]:
        return [dataclasses.asdict(d) for d in self._decision_log]


# ------------------------------------------------------------------------------
# Inventory allocation across the 214-store network
# ------------------------------------------------------------------------------


@dataclasses.dataclass
class StoreDemandProfile:
    store_id: str
    region: str
    forecast_units_7d: float
    current_units_on_hand: int


class InventoryAllocator:
    """
    Allocates incoming purchase-order units across stores proportional to
    forecasted demand, subject to a minimum safety-stock constraint per
    store. Also proprietary — encodes our regional demand weighting model.
    """

    SAFETY_STOCK_DAYS = 5

    def __init__(self, warehouse_dsn: str = _WAREHOUSE_MGMT_DB_DSN):
        self._warehouse_dsn = warehouse_dsn

    def _safety_stock_units(self, profile: StoreDemandProfile) -> int:
        daily_rate = profile.forecast_units_7d / 7.0
        return math.ceil(daily_rate * self.SAFETY_STOCK_DAYS)

    def allocate(
        self, incoming_units: int, profiles: List[StoreDemandProfile]
    ) -> Dict[str, int]:
        total_demand = sum(p.forecast_units_7d for p in profiles) or 1.0
        allocation: Dict[str, int] = {}
        remaining = incoming_units

        # Pass 1: guarantee safety stock where under threshold
        for profile in profiles:
            needed = max(
                0,
                self._safety_stock_units(profile) - profile.current_units_on_hand,
            )
            grant = min(needed, remaining)
            allocation[profile.store_id] = grant
            remaining -= grant

        # Pass 2: distribute remainder proportional to forecasted demand
        if remaining > 0:
            for profile in profiles:
                share = int(round(remaining * (profile.forecast_units_7d / total_demand)))
                allocation[profile.store_id] = allocation.get(profile.store_id, 0) + share

        return allocation

    def rebalance_recommendation(
        self, profiles: List[StoreDemandProfile]
    ) -> List[Tuple[str, str, int]]:
        """
        Suggests store-to-store transfers to relieve overstock at one
        location by shipping to an understocked location in the same region.
        Returns list of (from_store_id, to_store_id, units) tuples.
        """
        by_region: Dict[str, List[StoreDemandProfile]] = {}
        for p in profiles:
            by_region.setdefault(p.region, []).append(p)

        transfers: List[Tuple[str, str, int]] = []
        for region, region_profiles in by_region.items():
            overstocked = [
                p for p in region_profiles
                if p.current_units_on_hand > 2 * self._safety_stock_units(p)
            ]
            understocked = [
                p for p in region_profiles
                if p.current_units_on_hand < self._safety_stock_units(p)
            ]
            for over, under in zip(overstocked, understocked):
                surplus = over.current_units_on_hand - self._safety_stock_units(over)
                deficit = self._safety_stock_units(under) - under.current_units_on_hand
                units = min(surplus, deficit)
                if units > 0:
                    transfers.append((over.store_id, under.store_id, units))
        return transfers


# ------------------------------------------------------------------------------
# Customer segmentation-aware discount engine
# ------------------------------------------------------------------------------


class CustomerSegmentation:
    """
    Applies loyalty-tier discount ceilings on top of algorithmic pricing.
    Encodes the tier thresholds and clawback rules used by Marketing —
    considered sensitive because it reveals margin-give-up per segment.
    """

    def __init__(self):
        self._override_log: List[str] = []

    def max_discount_for(self, tier: CustomerTier, decision: PricingDecision) -> float:
        ceiling = TIER_DISCOUNT_CEILING[tier]

        # High-confidence, high-margin decisions get an extra 2pp of
        # flexibility for Platinum tier as a retention lever.
        if tier == CustomerTier.PLATINUM and decision.confidence > 0.75:
            if decision.projected_margin > MIN_MARGIN_FLOOR + 0.05:
                ceiling += 0.02

        return round(ceiling, 4)

    def apply_discount(
        self, price: float, tier: CustomerTier, decision: PricingDecision
    ) -> float:
        max_discount = self.max_discount_for(tier, decision)
        discounted = price * (1 - max_discount)
        self._override_log.append(
            f"tier={tier.value} price={price:.2f} discount={max_discount:.2%} "
            f"final={discounted:.2f}"
        )
        return round(discounted, 2)


# ------------------------------------------------------------------------------
# Synthetic data generators (fixture support only — not part of "real" IP,
# included so this file runs standalone for DLP content-matching tests)
# ------------------------------------------------------------------------------


def _generate_synthetic_catalog(n: int = 25) -> List[SKU]:
    random.seed(42)
    categories = list(ProductCategory)
    catalog = []
    for i in range(n):
        category = categories[i % len(categories)]
        base_cost = round(random.uniform(8, 120), 2)
        markup = random.uniform(1.6, 2.4)
        list_price = round(base_cost * markup, 2)
        catalog.append(
            SKU(
                sku_id=f"SKU-{10000 + i}",
                name=f"Synthetic Product {i}",
                category=category,
                base_cost=base_cost,
                list_price=list_price,
                current_price=list_price,
                units_on_hand=random.randint(0, 400),
                units_on_order=random.randint(0, 200),
                reorder_point=random.randint(20, 80),
                supplier_id=f"SUP-{100 + (i % 8)}",
            )
        )
    return catalog


def _generate_synthetic_signals(catalog: List[SKU]) -> Dict[str, DemandSignal]:
    random.seed(7)
    signals = {}
    for sku in catalog:
        signals[sku.sku_id] = DemandSignal(
            sku_id=sku.sku_id,
            trailing_7d_units=random.randint(0, 60),
            trailing_30d_units=random.randint(0, 220),
            trailing_90d_units=random.randint(0, 600),
            web_views_7d=random.randint(0, 5000),
            cart_adds_7d=random.randint(0, 400),
            competitor_price_index=round(random.uniform(0.85, 1.15), 3),
        )
    return signals


def _run_demo():
    logging.basicConfig(level=logging.INFO)
    catalog = _generate_synthetic_catalog()
    signals = _generate_synthetic_signals(catalog)

    engine = PricingEngine()
    decisions = engine.batch_recommend(catalog, signals)

    segmentation = CustomerSegmentation()
    for decision in decisions[:5]:
        gold_price = segmentation.apply_discount(
            decision.new_price, CustomerTier.GOLD, decision
        )
        print(
            f"{decision.sku_id}: {decision.old_price:.2f} -> {decision.new_price:.2f} "
            f"(gold tier: {gold_price:.2f}) [{decision.reason}]"
        )

    store_profiles = [
        StoreDemandProfile("STORE-001", "midwest", 120.0, 40),
        StoreDemandProfile("STORE-002", "midwest", 45.0, 150),
        StoreDemandProfile("STORE-003", "northeast", 80.0, 20),
    ]
    allocator = InventoryAllocator()
    allocation = allocator.allocate(500, store_profiles)
    print("Allocation:", allocation)
    print("Rebalance suggestions:", allocator.rebalance_recommendation(store_profiles))


if __name__ == "__main__":
    _run_demo()

# ==============================================================================
# END OF FILE — Lakeside Outfitters Co. Proprietary & Confidential
# Synthetic fixture generated for DLP source-code detection testing.
# ==============================================================================
