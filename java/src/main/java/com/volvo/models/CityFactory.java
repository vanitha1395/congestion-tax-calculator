package com.volvo.models;

public class CityFactory {
    public static City createCity(String cityName) {
        switch (cityName.toLowerCase()) {
            case "gothenburg":
                return new Gothenburg();
            // extend for further cities
            default:
                throw new IllegalArgumentException("Unknown city: " + cityName);
        }
    }
}