import csv
import random
import os
import uuid
from datetime import datetime, timedelta
from collections import defaultdict

# ⚙️ Config
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

GEN_CSV = os.path.join(DATA_DIR, "energy_generation.csv")
CONSUMPTION_CSV = os.path.join(DATA_DIR, "energy_consumption.csv")

START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 4, 8)

COUNTRIES = ["USA", "UK", "Australia"]
SOURCE_TYPES = ["wind", "solar", "biomass"]
SOURCE_COUNTS = {"wind": 2, "solar": 2, "biomass": 2}
LOCATIONS_PER_COUNTRY = {
    "USA": ["New York", "California"],
    "UK": ["London", "Manchester"],
    "Australia": ["Sydney", "Melbourne"],
}
SECTORS = ["residential", "commercial", "industrial"]
PRICE_MAP = {
    "residential": (0.10, 0.20),
    "commercial": (0.15, 0.30),
    "industrial": (0.12, 0.25),
}

def date_range(start: datetime, end: datetime):
    """Yields dates from start to end, one per day."""
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)

def generate_energy_generation_data(filename: str):
    system_map = []
    system_id_counter = defaultdict(int)

    for country in COUNTRIES:
        for source in SOURCE_TYPES:
            for _ in range(SOURCE_COUNTS[source]):
                system_id_counter[(country, source)] += 1
                system_id = f"SYS-{country.upper()}-{source.upper()}-{system_id_counter[(country, source)]}"
                system_map.append({
                    "system_id": system_id,
                    "country": country,
                    "source": source
                })

    rows = []
    all_dates = list(date_range(START_DATE, END_DATE))

    for system in system_map:
        for date in all_dates:
            energy_kwh = round(random.uniform(10.0, 500.0), 2)
            rows.append({
                "id": str(uuid.uuid4()),
                "timestamp": date.replace(hour=23, minute=59).isoformat(),
                "energy_kwh": energy_kwh,
                "source": system["source"],
                "location": system["country"],
                "system_id": system["system_id"]
            })

    rows.sort(key=lambda x: x["timestamp"])

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "timestamp", "energy_kwh", "source", "location", "system_id"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"⚡ Generated {len(rows)} generation rows in '{filename}'")

def load_generation_totals(filename: str):
    totals = defaultdict(float)
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            totals[row["location"]] += float(row["energy_kwh"])
    return totals

def generate_energy_consumption_data(generation_csv: str, output_csv: str):
    if not os.path.exists(generation_csv):
        print(f"⚠️ '{generation_csv}' not found. Generating it now...")
        generate_energy_generation_data(generation_csv)

    generation_totals = load_generation_totals(generation_csv)
    consumed_totals = defaultdict(float)

    consumer_id_counter = defaultdict(int)
    consumers = []

    for country, locations in LOCATIONS_PER_COUNTRY.items():
        for location in locations:
            selected_sectors = random.sample(SECTORS, k=random.randint(1, 3))
            for sector in selected_sectors:
                for _ in range(random.randint(2, 5)):
                    consumer_id_counter[(country, sector)] += 1
                    consumer_id = f"CON-{country.upper()}-{sector[:3].upper()}-{consumer_id_counter[(country, sector)]}"
                    consumers.append({
                        "consumer_id": consumer_id,
                        "country": country,
                        "location": location,
                        "sector": sector,
                    })

    rows = []
    all_dates = list(date_range(START_DATE, END_DATE))

    for consumer in consumers:
        for date in all_dates:
            country = consumer["country"]
            energy_kwh = round(random.uniform(5.0, 100.0), 2)

            if consumed_totals[country] + energy_kwh > generation_totals[country]:
                break  # stop if country is fully consumed

            consumed_totals[country] += energy_kwh
            price = round(random.uniform(*PRICE_MAP[consumer["sector"]]), 4)
            total = round(price * energy_kwh, 2)

            rows.append({
                "id": str(uuid.uuid4()),
                "timestamp": date.replace(hour=23, minute=59).isoformat(),
                "energy_kwh": energy_kwh,
                "location": consumer["location"],
                "sector": consumer["sector"],
                "consumer_id": consumer["consumer_id"],
                "price": price,
                "total": total
            })

    rows.sort(key=lambda x: x["timestamp"])

    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "timestamp", "energy_kwh", "location", "sector", "consumer_id", "price", "total"
        ])
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Generated {len(rows)} consumption rows in '{output_csv}'")

# 🚀 Main
if __name__ == "__main__":
    generate_energy_generation_data(GEN_CSV)
    generate_energy_consumption_data(GEN_CSV, CONSUMPTION_CSV)
