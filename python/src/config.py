from datetime import datetime, time

toll_free_vehicles = [
    "emergency_vehicles",
    "bus",
    "diplomat_vehicles",
    "motorcyles",
    "military_vehicles",
    "foreign_vehicles"
]

##
gothenburg_toll_fee_schedule = [
    (time(6, 0), time(6, 29), 8),
    (time(6, 30), time(6, 59), 13),
    (time(7, 0), time(7, 59), 18),
    (time(8, 0), time(8, 29), 13),
    (time(8, 30), time(14, 59), 8),
    (time(15, 00), time(15, 29), 13),
    (time(15, 30), time(16, 59), 18),
    (time(17, 00), time(17, 59), 13),
    (time(18, 00), time(18, 29), 8),
]