import heapq
from collections import deque
from datetime import datetime

class Driver:
    def __init__(self, driver_id, location, rating):
        self.driver_id = driver_id
        self.location = location  # (x, y) tuple
        self.rating = rating

    def __repr__(self):
        return f"Driver(id={self.driver_id}, loc={self.location}, rating={self.rating})"

class Rider:
    def __init__(self, rider_id, location):
        self.rider_id = rider_id
        self.location = location  # (x, y) tuple

    def __repr__(self):
        return f"Rider(id={self.rider_id}, loc={self.location})"

def distance(loc1, loc2):
    # Euclidean distance
    return ((loc1[0]-loc2[0])**2 + (loc1[1]-loc2[1])**2)**0.5

class RideSharingSimulator:
    def __init__(self):
        self.available_drivers = []  # priority queue: (distance, -rating, driver_id, driver_obj)
        self.waiting_riders = deque()  # FIFO queue of riders waiting for a driver
        self.ride_history = []  # List of assigned rides: (timestamp, driver_id, rider_id)

    def add_driver(self, driver):
        # For simplicity, assume drivers become available at a fixed location
        # They join the pool with no immediate rider assigned
        # Distance is 0 for now because no rider yet
        # We push with a dummy distance of 0 and rating for sorting later
        # Actually, distance depends on rider, so we wait for ride requests to calculate distances
        # So drivers will be stored in a dict instead of queue until assigned.
        # To handle this, let's keep drivers in a set and calculate priority dynamically when matching.
        # But priority queue requires known priority at push time.
        # Alternative: We'll store drivers in a list and push them when a rider requests.
        # So here we keep them in a dict:
        self.drivers_pool[driver.driver_id] = driver

    def add_rider(self, rider):
        self.waiting_riders.append(rider)
        self.match_rides()

    def match_rides(self):
        # We attempt to match riders with nearest drivers
        # For each waiting rider:
        # - Build a priority queue of available drivers sorted by distance to this rider and rating
        # - Assign nearest driver and remove from available drivers pool
        
        # But to simplify, let's store available drivers in a dict, and on each rider,
        # we compute distances and push all drivers into a temp priority queue for that rider.

        while self.waiting_riders and self.drivers_pool:
            rider = self.waiting_riders[0]
            pq = []
            for d_id, driver in self.drivers_pool.items():
                dist = distance(driver.location, rider.location)
                # priority: distance ascending, rating descending
                heapq.heappush(pq, (dist, -driver.rating, d_id, driver))

            if not pq:
                break  # no drivers available

            dist, neg_rating, d_id, driver = heapq.heappop(pq)
            # Assign this driver to the rider
            self.waiting_riders.popleft()
            del self.drivers_pool[d_id]
            self.ride_history.append((datetime.now(), d_id, rider.rider_id))
            print(f"Assigned Driver {d_id} (Rating: {driver.rating}, Distance: {dist:.2f}) to Rider {rider.rider_id}")
    
    def add_available_driver(self, driver):
        # Adds driver to pool and tries to match waiting riders
        self.drivers_pool[driver.driver_id] = driver
        self.match_rides()

    def print_ride_history(self):
        print("\nRide History:")
        for ts, d_id, r_id in self.ride_history:
            print(f"{ts.strftime('%Y-%m-%d %H:%M:%S')}: Driver {d_id} assigned to Rider {r_id}")

    def start(self):
        self.drivers_pool = {}

# Example usage
if __name__ == "__main__":
    sim = RideSharingSimulator()
    sim.start()

    # Add some drivers
    sim.add_available_driver(Driver("D1", (0,0), 4.7))
    sim.add_available_driver(Driver("D2", (5,5), 4.9))
    sim.add_available_driver(Driver("D3", (2,1), 4.5))

    # Add some riders
    sim.add_rider(Rider("R1", (1,1)))
    sim.add_rider(Rider("R2", (6,6)))
    sim.add_rider(Rider("R3", (0,2)))
    sim.add_rider(Rider("R4", (10,10)))  # Will wait (no driver nearby enough)

    # Add one more driver later
    sim.add_available_driver(Driver("D4", (9,9), 4.8))

    sim.print_ride_history()
