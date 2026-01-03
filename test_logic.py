# FILE: test_logic.py
from database import RenovationLogic

print("STARTING LOGIC TEST")

# TEST 1: Safety Check (Should Fail)
print("\nTest 1: Wood in Bathroom...")
is_safe, msg = RenovationLogic.check_safety("Bathroom", "Solid Wood")
if is_safe == False:
    print("✅ SUCCESS: System correctly blocked unsafe material.")
    print(f"   Message: {msg}")
else:
    print("❌ FAIL: System allowed unsafe material.")

# TEST 2: Calculation Math
print("\nTest 2: Calculating Cost for 5x5m Room...")
# Setup: 5x5m floor, 3m height.
# Floor: Vinyl (RM 55/sqm). Wall: Paint (RM 22/sqm).
# Floor Area = 25 sqm. Cost = 25 * 55 = 1375
# Wall Area = (20 perimeter * 3 height) = 60 sqm. Cost = 60 * 22 = 1320
# Expected Total = 1375 + 1320 = 2695
result = RenovationLogic.calculate_project(5, 5, 3, "Vinyl", "Standard Paint", "30x30 cm")

print(f"   Calculated Total: RM {result['total_cost']}")
if result['total_cost'] == 2695.00:
    print("✅ SUCCESS: Math is perfect.")
else:
    print(f"❌ FAIL: Expected 2695, got {result['total_cost']}")

print("\n--- TEST COMPLETE ---")