import csv
import os
import uuid
import random
from datetime import datetime, timedelta
from typing import List

# Paths
DATA_DIR = "data"
GEN_CSV = os.path.join(DATA_DIR, "energy_generation.csv")
CON_CSV = os.path.join(DATA_DIR, "energy_consumption.csv")
os.makedirs(DATA_DIR, exist_ok=True)

# Date range
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 4, 8)

# Generation config with initial capacities
GENERATION_CONFIG = {
    "USA": {
        "wind": {"SYS-USA-WIND-1": 100, "SYS-USA-WIND-2": 100},
        "solar": {"SYS-USA-SOLAR-1": 80, "SYS-USA-SOLAR-2": 85, "SYS-USA-SOLAR-3": 90},
        "biomass": {"SYS-USA-BIO-1": 70},
    },
    "UK": {
        "wind": {"SYS-UK-WIND-1": 90, "SYS-UK-WIND-2": 85, "SYS-UK-WIND-3": 80},
        "solar": {"SYS-UK-SOLAR-1": 75, "SYS-UK-SOLAR-2": 70},
        "biomass": {},
    },
    "Australia": {
        "wind": {"SYS-AUS-WIND-1": 95},
        "solar": {"SYS-AUS-SOLAR-1": 100, "SYS-AUS-SOLAR-2": 90},
        "biomass": {"SYS-AUS-BIO-1": 60},
    },
}

# Consumption config with price ranges
CONSUMPTION_CONFIG = {
    "USA": {
        "New York": {
            "residential": {"CON-USA-RES-1": (0.10, 0.20), "CON-USA-RES-2": (0.10, 0.20)},
            "industrial": {"CON-USA-IND-1": (0.12, 0.25)},
        },
        "Texas": {
            "commercial": {"CON-USA-COM-1": (0.15, 0.30)},
            "residential": {"CON-USA-RES-3": (0.10, 0.20)},
        },
    },
    "UK": {
        "London": {
            "residential": {"CON-UK-RES-1": (0.10, 0.20)},
            "commercial": {"CON-UK-COM-1": (0.15, 0.30)},
        },
        "Manchester": {
            "industrial": {"CON-UK-IND-1": (0.12, 0.25)},
        },
    },
    "Australia": {
        "Sydney": {
            "residential": {"CON-AUS-RES-1": (0.10, 0.20)},
            "commercial": {"CON-AUS-COM-1": (0.15, 0.30)},
        },
        "Melbourne": {
            "industrial": {"CON-AUS-IND-1": (0.12, 0.25)},
        },
    },
}


def date_range(start: datetime, end: datetime) -> List[datetime]:
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def month_index(date: datetime) -> int:
    return (date.year - START_DATE.year) * 12 + (date.month - START_DATE.month)


def generate_generation_data(filepath: str):
    rows = []
    for date in date_range(START_DATE, END_DATE):
        for country, sources in GENERATION_CONFIG.items():
            country_total = 0
            for source_type, systems in sources.items():
                system_ids = list(systems.items())
                if not system_ids:
                    continue

                active_systems = random.sample(system_ids, k=random.randint(1, len(system_ids)))
                for sys_id, base_capacity in system_ids:
                    # Capacity upgrade factor
                    monthly_increment = 0.02 * base_capacity  # 2% per month
                    upgrade = month_index(date) * monthly_increment
                    final_capacity = base_capacity + upgrade

                    if (sys_id, base_capacity) in active_systems:
                        energy_kwh = round(random.uniform(0.85, 1.0) * final_capacity, 2)
                        country_total += energy_kwh
                    else:
                        energy_kwh = round(random.uniform(0.0, 0.1) * final_capacity, 2)

                    rows.append({
                        "id": str(uuid.uuid4()),
                        "timestamp": date.replace(hour=23, minute=59).isoformat(),
                        "energy_kwh": energy_kwh,
                        "source": source_type,
                        "location": country,
                        "system_id": sys_id,
                    })

            if country_total < 10:
                print(f"⚠️ Warning: Very low generation for {country} on {date.date()}")

    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "timestamp", "energy_kwh", "source", "location", "system_id"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Generated {len(rows)} generation rows at {filepath}")


def generate_consumption_data(filepath: str):
    rows = []
    # Assign base capacity to each consumer only once
    consumer_base_capacity = {}

    for country, locations in CONSUMPTION_CONFIG.items():
        for loc, sectors in locations.items():
            for sector, consumers in sectors.items():
                for con_id in consumers:
                    # Assign base capacity between 30 and 70 kWh per day
                    consumer_base_capacity[con_id] = random.randint(30, 70)

    for date in date_range(START_DATE, END_DATE):
        for country, locations in CONSUMPTION_CONFIG.items():
            country_total = 0
            for loc, sectors in locations.items():
                for sector, consumers in sectors.items():
                    consumer_ids = list(consumers.items())

                    if not consumer_ids:
                        continue

                    # Randomly decide who is active today
                    active_consumers = random.sample(consumer_ids, k=random.randint(1, len(consumer_ids)))

                    for con_id, price_range in consumer_ids:
                        base_capacity = consumer_base_capacity[con_id]
                        monthly_growth = 0.01 * base_capacity  # 1% monthly capacity growth
                        upgrade = month_index(date) * monthly_growth
                        final_capacity = base_capacity + upgrade

                        if (con_id, price_range) in active_consumers:
                            energy_kwh = round(random.uniform(0.8, 1.0) * final_capacity, 2)
                            price = round(random.uniform(*price_range), 4)
                            total = round(energy_kwh * price, 2)
                            country_total += energy_kwh
                        else:
                            energy_kwh = price = total = 0.0

                        rows.append({
                            "id": str(uuid.uuid4()),
                            "timestamp": date.replace(hour=23, minute=59).isoformat(),
                            "energy_kwh": energy_kwh,
                            "location": loc,
                            "sector": sector,
                            "consumer_id": con_id,
                            "price": price,
                            "total": total,
                        })

            if country_total < 5:
                print(f"⚠️ Warning: Very low consumption for {country} on {date.date()}")

    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "timestamp", "energy_kwh", "location", "sector", "consumer_id", "price", "total"
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Generated {len(rows)} consumption rows at {filepath}")


if __name__ == "__main__":
    generate_generation_data(GEN_CSV)
    generate_consumption_data(CON_CSV)
