package com.volvo.algorithm;

import com.volvo.models.*;

import com.volvo.models.VehicleFactory;

import java.time.LocalDateTime;
import java.time.MonthDay;
import java.time.format.DateTimeFormatter;
import java.util.*;

public class CongestionTaxCalculator {
    private final City city;
    private final Vehicle vehicle;
    private static final Set<MonthDay> PUBLIC_HOLIDAYS = new HashSet<>();
    private static final Set<String> EXEMPT_VEHICLE_TYPES = new HashSet<>(Arrays.asList("motorcycle", "emergency", "diplomat", "foreign", "military"));

    static {
        // Todo: Improve handling how the year's public holidays are handled
        // Public holiday list for year 2023
        PUBLIC_HOLIDAYS.add(MonthDay.of(1, 1));  // New Year's Day
        PUBLIC_HOLIDAYS.add(MonthDay.of(1, 6));  // Epiphany
        PUBLIC_HOLIDAYS.add(MonthDay.of(4, 7));  // Good Friday (2023)
        PUBLIC_HOLIDAYS.add(MonthDay.of(4, 9));  // Easter Sunday (2023)
        PUBLIC_HOLIDAYS.add(MonthDay.of(4, 10)); // Easter Monday (2023)
        PUBLIC_HOLIDAYS.add(MonthDay.of(5, 1));  // Labour Day
        PUBLIC_HOLIDAYS.add(MonthDay.of(5, 18)); // Ascension Day (2023)
        PUBLIC_HOLIDAYS.add(MonthDay.of(5, 28)); // Whit Sunday (2023)
        PUBLIC_HOLIDAYS.add(MonthDay.of(6, 6));  // National Day
        PUBLIC_HOLIDAYS.add(MonthDay.of(6, 24)); // Midsummer's Day (2023)
        PUBLIC_HOLIDAYS.add(MonthDay.of(11, 4)); // All Saints' Day (2023)
        PUBLIC_HOLIDAYS.add(MonthDay.of(12, 24)); // Christmas Eve
        PUBLIC_HOLIDAYS.add(MonthDay.of(12, 25)); // Christmas Day
        PUBLIC_HOLIDAYS.add(MonthDay.of(12, 26)); // Boxing Day
        PUBLIC_HOLIDAYS.add(MonthDay.of(12, 31)); // New Year's Eve
    }

    public CongestionTaxCalculator(String city, String vehicleType) {

        // Todo: The factories can be utilized in a separate class to
        // separation of dependency from HTTP Server
        // Create respective city using Factory method
        this.city = CityFactory.createCity(city);
        // utilize vehicle factory to create vehicle instance
        this.vehicle = VehicleFactory.createVehicle(vehicleType);

    }


    public int calculateTax(List<String> dateTimes) {
        // check if the vehicle type is exempt from taxes
        if (EXEMPT_VEHICLE_TYPES.contains(vehicle.getType())) {
            return 0;
        }

        // if the datetimes list is empty or null, there is no taxes
        if (dateTimes == null || dateTimes.isEmpty()) {
            return 0;
        }

        // Converting string into Date and time types
        List<LocalDateTime> sortedTimes = new ArrayList<>();
        for (String dateTime : dateTimes) {
            sortedTimes.add(LocalDateTime.parse(dateTime, DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        }
        Collections.sort(sortedTimes);

        int totalTax = 0;
        LocalDateTime lastChargeTime = sortedTimes.get(0).minusHours(1); // Initialize to 1 hour before first entry
        int highestTaxInInterval = 0;

        for (LocalDateTime currentTime : sortedTimes) {
            if (isWeekend(currentTime) || isPublicHoliday(currentTime)) {
                continue; // Skip weekends and holidays
            }

            int currentTax = getSingleTax(currentTime);

            if (currentTime.isBefore(lastChargeTime.plusHours(1))) {
                // Within one hour of last charge, update highest tax if necessary
                highestTaxInInterval = Math.max(highestTaxInInterval, currentTax);
            } else {
                // More than one hour since last charge, add highest tax from previous interval
                totalTax += highestTaxInInterval;
                highestTaxInInterval = currentTax;
                lastChargeTime = currentTime;
            }
        }

        // Add the highest tax from the last interval
        totalTax += highestTaxInInterval;

        return totalTax;
    }

    private int getSingleTax(LocalDateTime dt) {
        String time = dt.format(DateTimeFormatter.ofPattern("HH:mm"));
        Map<String, Integer> tollSchedule = city.getTollSchedule();
        for (Map.Entry<String, Integer> entry : tollSchedule.entrySet()) {
            String[] range = entry.getKey().split("-");
            if (isTimeInRange(time, range[0], range[1])) {
                return entry.getValue();
            }
        }
        return 0;
    }

    private boolean isWeekend(LocalDateTime dt) {
        int dayOfWeek = dt.getDayOfWeek().getValue();
        return dayOfWeek == 6 || dayOfWeek == 7;
    }

    private boolean isPublicHoliday(LocalDateTime dt) {
        MonthDay monthDay = MonthDay.from(dt);
        return PUBLIC_HOLIDAYS.contains(monthDay);
    }

    private boolean isTimeInRange(String time, String start, String end) {
        return (time.compareTo(start) >= 0 && time.compareTo(end) <= 0);
    }
}