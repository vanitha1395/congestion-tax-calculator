package com.volvo.models;

import com.volvo.models.Vehicle;

public class Emergency extends Vehicle {
    @Override
    public String getType() {
        return "Emergency";
    }
}

