"""
Greedy Algorithms Assignment
Implement three greedy algorithms for delivery optimization.
"""

import json
import time


# ============================================================================
# PART 1: PACKAGE PRIORITIZATION (Activity Selection)
# ============================================================================

def maximize_deliveries(time_windows):
    """
    Schedule the maximum number of deliveries given time window constraints.
    """
    # Sort deliveries by end time
    sorted_windows = sorted(time_windows, key=lambda x: x['end'])

    selected_deliveries = []
    current_end = 0

    for delivery in sorted_windows:
        if delivery['start'] >= current_end:
            selected_deliveries.append(delivery['delivery_id'])
            current_end = delivery['end']

    return selected_deliveries


# ============================================================================
# PART 2: TRUCK LOADING (Fractional Knapsack)
# ============================================================================

def optimize_truck_load(packages, weight_limit):
    """
    Maximize total priority value of packages loaded within weight constraint.
    """
    # Sort packages by priority-to-weight ratio
    sorted_packages = sorted(
        packages,
        key=lambda x: x['priority'] / x['weight'],
        reverse=True
    )

    total_priority = 0
    total_weight = 0
    loaded_packages = []

    for pkg in sorted_packages:
        if total_weight >= weight_limit:
            break

        remaining_capacity = weight_limit - total_weight

        if pkg['weight'] <= remaining_capacity:
            # Take whole package
            total_weight += pkg['weight']
            total_priority += pkg['priority']
            loaded_packages.append({
                'package_id': pkg['package_id'],
                'fraction': 1.0
            })
        else:
            # Take fraction of package
            fraction = remaining_capacity / pkg['weight']
            total_weight += remaining_capacity
            total_priority += pkg['priority'] * fraction
            loaded_packages.append({
                'package_id': pkg['package_id'],
                'fraction': round(fraction, 2)
            })
            break

    return {
        'total_priority': round(total_priority, 2),
        'total_weight': round(total_weight, 2),
        'packages': loaded_packages
    }


# ============================================================================
# PART 3: DRIVER ASSIGNMENT (Interval Scheduling)
# ============================================================================

def minimize_drivers(deliveries):
    """
    Assign deliveries to the minimum number of drivers needed.
    """
    # Sort deliveries by start time
    deliveries_sorted = sorted(deliveries, key=lambda x: x['start'])

    drivers = []

    for delivery in deliveries_sorted:
        assigned = False

        for driver in drivers:
            last_delivery = driver[-1]
            if delivery['start'] >= last_delivery['end']:
                driver.append(delivery)
                assigned = True
                break

        if not assigned:
            drivers.append([delivery])

    assignments = []
    for driver in drivers:
        assignments.append([d['delivery_id'] for d in driver])

    return {
        'num_drivers': len(drivers),
        'assignments': assignments
    }


# ============================================================================
# TESTING & BENCHMARKING
# ============================================================================

def load_scenario(filename):
    """Load a scenario from JSON file."""
    with open(f"scenarios/{filename}", "r") as f:
        return json.load(f)


def test_package_prioritization():
    print("=" * 70)
    print("TESTING PACKAGE PRIORITIZATION")
    print("=" * 70 + "\n")

    test1 = [
        {'delivery_id': 'A', 'start': 1, 'end': 2},
        {'delivery_id': 'B', 'start': 3, 'end': 4},
        {'delivery_id': 'C', 'start': 5, 'end': 6}
    ]
    result1 = maximize_deliveries(test1)
    print("Test 1:", "✓ PASS" if len(result1) == 3 else "✗ FAIL")

    test2 = [
        {'delivery_id': 'A', 'start': 1, 'end': 5},
        {'delivery_id': 'B', 'start': 2, 'end': 4},
        {'delivery_id': 'C', 'start': 3, 'end': 6}
    ]
    result2 = maximize_deliveries(test2)
    print("Test 2 result:", result2)

    test3 = [
        {'delivery_id': 'A', 'start': 1, 'end': 3},
        {'delivery_id': 'B', 'start': 2, 'end': 5},
        {'delivery_id': 'C', 'start': 4, 'end': 7},
        {'delivery_id': 'D', 'start': 6, 'end': 9}
    ]
    result3 = maximize_deliveries(test3)
    print("Test 3:", "✓ PASS" if len(result3) == 2 else "✗ FAIL")


def test_truck_loading():
    print("=" * 70)
    print("TESTING TRUCK LOADING")
    print("=" * 70 + "\n")

    packages = [
        {'package_id': 'A', 'weight': 10, 'priority': 60},
        {'package_id': 'B', 'weight': 20, 'priority': 100},
        {'package_id': 'C', 'weight': 30, 'priority': 120}
    ]

    result = optimize_truck_load(packages, 50)
    print("Total priority:", result['total_priority'])
    print("Total weight:", result['total_weight'])
    print("Packages:", result['packages'])


def test_driver_assignment():
    print("=" * 70)
    print("TESTING DRIVER ASSIGNMENT")
    print("=" * 70 + "\n")

    deliveries = [
        {'delivery_id': 'A', 'start': 1, 'end': 3},
        {'delivery_id': 'B', 'start': 2, 'end': 4},
        {'delivery_id': 'C', 'start': 4, 'end': 6},
        {'delivery_id': 'D', 'start': 5, 'end': 7}
    ]

    result = minimize_drivers(deliveries)
    print("Drivers needed:", result['num_drivers'])
    print("Assignments:", result['assignments'])


def benchmark_scenarios():
    print("=" * 70)
    print("BENCHMARKING REAL SCENARIOS")
    print("=" * 70 + "\n")

    data = load_scenario("package_prioritization.json")
    start = time.perf_counter()
    maximize_deliveries(data)
    print("Package prioritization time:",
          (time.perf_counter() - start) * 1000, "ms")

    data = load_scenario("truck_loading.json")
    start = time.perf_counter()
    optimize_truck_load(data['packages'], data['truck_capacity'])
    print("Truck loading time:",
          (time.perf_counter() - start) * 1000, "ms")

    data = load_scenario("driver_assignment.json")
    start = time.perf_counter()
    minimize_drivers(data)
    print("Driver assignment time:",
          (time.perf_counter() - start) * 1000, "ms")


if __name__ == "__main__":
    test_package_prioritization()
    test_truck_loading()
    test_driver_assignment()
    # benchmark_scenarios()