package com.volvo.models;

import com.volvo.models.City;

import java.util.Map;
import java.util.HashMap;

public class Gothenburg extends City {
    public Gothenburg() {
        super("Gothenburg");
    }

    @Override
    public Map<String, Integer> getTollSchedule() {
        Map<String, Integer> schedule = new HashMap<>();
        schedule.put("06:00-06:29", 8);
        schedule.put("06:30-06:59", 13);
        schedule.put("07:00-07:59", 18);
        schedule.put("08:00-08:29", 13);
        schedule.put("08:30-14:59", 8);
        schedule.put("15:00-15:29", 13);
        schedule.put("15:30-16:59", 18);
        schedule.put("17:00-17:59", 13);
        schedule.put("18:00-18:29", 8);
        schedule.put("18:30-05:59", 0);
        return schedule;
    }
}