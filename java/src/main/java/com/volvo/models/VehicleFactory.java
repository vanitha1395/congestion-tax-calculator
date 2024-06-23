package com.volvo.models;

import com.volvo.models.*;

public class VehicleFactory {
    public static Vehicle createVehicle(String vehicleName) {
        switch (vehicleName.toLowerCase()) {
            case "car":
                return new Car();
            case "motorbike":
                return new Motorbike();
            case "motorcycle":
                return new Motorcycle();
            case "truck":
                return new Truck();
            case "military":
                return new Military();
            case "diplomat":
                return new Diplomat();
            case "foreign":
                return new Foreign();
            case "emergency":
                return new Emergency();
            // extend for further vehicles
            default:
                throw new IllegalArgumentException("Unknown vehicle: " + vehicleName);
        }
    }
}