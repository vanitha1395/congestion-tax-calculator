package com.volvo.models;

import java.util.Map;

public abstract class City {
    protected String name;

    public City(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public abstract Map<String, Integer> getTollSchedule();
}