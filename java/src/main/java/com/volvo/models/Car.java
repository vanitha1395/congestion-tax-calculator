package com.volvo.models;

import com.volvo.models.Vehicle;

public class Car extends Vehicle {
    @Override
    public String getType() {
        return "Car";
    }
}

