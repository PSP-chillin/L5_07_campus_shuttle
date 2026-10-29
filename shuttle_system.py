"""Campus shuttle timetable and fleet tracker."""

import json
import secrets
from datetime import datetime
from typing import Any


MIN_CAPACITY = 10
DRIVERS = ("Prakash", "Leela", "Imran", "Tom")
routes: dict[str, dict[str, Any]] = {
    "R1": {"name": "Main Gate - Library", "trips": []},
    "R2": {"name": "Hostel - Sports Complex", "trips": []},
    "R3": {"name": "Admin Block - Metro", "trips": []},
}


def add_trip_log(
    route_id: str, passenger_count: int, logs: list[str] | None = None
) -> list[str]:
    """Record a valid passenger count and return the log entries."""
    if route_id not in routes:
        raise ValueError(f"Unknown route: {route_id}")
    if not isinstance(passenger_count, int) or passenger_count < 0:
        raise ValueError("Passenger count must be a non-negative integer")

    if logs is None:
        logs = []
    routes[route_id]["trips"].append(passenger_count)
    logs.append(f"{datetime.now()}: {route_id} carried {passenger_count}")
    return logs


def remove_route(route_id: str) -> None:
    """Remove a route if it exists."""
    routes.pop(route_id, None)


def average_load(route_id: str) -> float:
    """Return the average number of passengers for a route."""
    if route_id not in routes:
        raise ValueError(f"Unknown route: {route_id}")

    trips = routes[route_id]["trips"]
    if not trips:
        raise ValueError(f"Route {route_id} has no recorded trips")
    return sum(trips) / len(trips)


def underused_routes() -> list[str]:
    """Return routes whose average load is below the minimum capacity."""
    return [
        route_id
        for route_id, route in routes.items()
        if route["trips"] and average_load(route_id) < MIN_CAPACITY
    ]


def assign_driver(route_id: str) -> str:
    """Assign a random driver to an existing route."""
    if route_id not in routes:
        raise ValueError(f"Unknown route: {route_id}")
    return secrets.choice(DRIVERS)


def sync_fleet_data(file: str = "fleet.json") -> None:
    """Write the current routes to disk and load them back."""
    with open(file, "w", encoding="utf-8") as fleet_file:
        json.dump(routes, fleet_file)
    with open(file, encoding="utf-8") as fleet_file:
        loaded_routes = json.load(fleet_file)
    routes.clear()
    routes.update(loaded_routes)


def main() -> None:
    add_trip_log("R1", 32)
    add_trip_log("R1", 28)
    add_trip_log("R2", 4)
    add_trip_log("R2", 6)
    add_trip_log("R3", 30)
    print("Driver for R1:", assign_driver("R1"))
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))
    sync_fleet_data()
    remove_route("R3")
    choice = input("Route to look up (Enter for R2): ") or "R2"
    if choice not in routes:
        print("Route not found:", choice)
        return
    print("Trips on", choice, ":", routes[choice]["trips"])


if __name__ == "__main__":
    main()
