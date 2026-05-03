import json
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path
from faker import Faker

fake = Faker()

OUTPUT_DIR = Path("data/streaming")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PRODUCT_CATEGORIES = [
    "pain_relief",
    "vitamins",
    "skin_care",
    "baby_care",
    "cold_flu",
    "personal_care",
    "prescription",
    "fitness"
]

DEVICES = ["mobile", "desktop", "tablet"]
COUNTRIES = ["Germany", "Netherlands", "Belgium", "Austria", "France"]


def create_event(user_id, session_id, event_type, product_id, category, event_time):
    return {
        "event_id": fake.uuid4(),
        "user_id": user_id,
        "session_id": session_id,
        "event_time": event_time.isoformat(),
        "event_type": event_type,
        "product_id": product_id,
        "category": category,
        "device": random.choice(DEVICES),
        "country": random.choice(COUNTRIES),
        "price": round(random.uniform(3.99, 149.99), 2),
        "quantity": random.randint(1, 5)
    }


def generate_session(session_number):
    user_id = f"user_{random.randint(1, 300)}"
    session_id = f"session_{session_number}"
    product_id = f"prod_{random.randint(1, 200)}"
    category = random.choice(PRODUCT_CATEGORIES)

    base_time = datetime.now(timezone.utc) - timedelta(minutes=random.randint(1, 5000))

    events = []

    # Every session starts with a page view
    events.append(create_event(user_id, session_id, "page_view", product_id, category, base_time))

    # Around 70% continue to product view
    if random.random() < 0.70:
        events.append(create_event(user_id, session_id, "product_view", product_id, category, base_time + timedelta(minutes=1)))

        # Around 40% of product viewers add to cart
        if random.random() < 0.40:
            events.append(create_event(user_id, session_id, "add_to_cart", product_id, category, base_time + timedelta(minutes=2)))

            # Around 50% of cart users go to checkout
            if random.random() < 0.50:
                events.append(create_event(user_id, session_id, "checkout", product_id, category, base_time + timedelta(minutes=3)))

                # Around 60% of checkout users purchase
                if random.random() < 0.60:
                    events.append(create_event(user_id, session_id, "purchase", product_id, category, base_time + timedelta(minutes=4)))

    return events


def generate_clickstream(total_sessions=500, records_per_file=200):
    all_events = []

    for session_number in range(1, total_sessions + 1):
        all_events.extend(generate_session(session_number))

    random.shuffle(all_events)

    file_number = 1
    for start in range(0, len(all_events), records_per_file):
        batch = all_events[start:start + records_per_file]
        output_file = OUTPUT_DIR / f"clickstream_batch_{file_number}.json"

        with output_file.open("w", encoding="utf-8") as file:
            for event in batch:
                file.write(json.dumps(event) + "\n")

        print(f"Generated {len(batch)} events: {output_file}")
        file_number += 1

    print(f"Total events generated: {len(all_events)}")


if __name__ == "__main__":
    generate_clickstream()