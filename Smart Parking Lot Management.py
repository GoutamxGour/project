class CarNode:
    def __init__(self, license_plate, slot_number):
        self.license_plate = license_plate
        self.slot_number = slot_number
        self.next = None

class ParkingLot:
    def __init__(self, total_slots):
        self.total_slots = total_slots
        self.free_slots = list(range(1, total_slots+1))  # dynamic allocation of slots
        self.head = None  # head of linked list for parked cars
        self.size = 0

    def is_full(self):
        return self.size == self.total_slots

    def park_car(self, license_plate):
        if self.is_full():
            print(f"Parking Lot Full! Car {license_plate} cannot be parked.")
            return False
        
        # Allocate a slot dynamically
        slot = self.free_slots.pop(0)
        new_car = CarNode(license_plate, slot)

        # Insert new car at the end of the linked list
        if not self.head:
            self.head = new_car
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_car
        
        self.size += 1
        print(f"Car {license_plate} parked at slot {slot}.")
        return True

    def exit_car(self, license_plate):
        prev = None
        current = self.head

        while current:
            if current.license_plate == license_plate:
                # Remove node from linked list
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                
                # Free the slot
                self.free_slots.append(current.slot_number)
                self.free_slots.sort()  # Keep slots sorted for better allocation
                self.size -= 1
                print(f"Car {license_plate} exited from slot {current.slot_number}.")
                return True
            
            prev = current
            current = current.next
        
        print(f"Car {license_plate} not found in parking lot.")
        return False

    def display_parked_cars(self):
        if not self.head:
            print("Parking Lot is empty.")
            return
        current = self.head
        print("Currently parked cars:")
        while current:
            print(f"Slot {current.slot_number}: Car {current.license_plate}")
            current = current.next

# Example usage
if __name__ == "__main__":
    lot = ParkingLot(3)

    lot.park_car("ABC123")
    lot.park_car("XYZ789")
    lot.park_car("LMN456")
    lot.display_parked_cars()

    # Lot is full now
    lot.park_car("JKL111")

    lot.exit_car("XYZ789")
    lot.display_parked_cars()

    lot.park_car("JKL111")
    lot.display_parked_cars()
