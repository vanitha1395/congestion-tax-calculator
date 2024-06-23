package com.volvo.server;

import com.volvo.models.*;
import com.volvo.algorithm.CongestionTaxCalculator;
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.time.LocalDateTime;

import org.json.JSONObject;
import org.json.JSONArray;

public class SimpleHttpServer {

    public static void main(String[] args) throws IOException {
        // Todo: endpoints and port ids shall be configured using configuration mechanism
        int port = 8080;
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
        server.createContext("/CalculateCongestionTax", new TaxCalculatorHandler());
        server.setExecutor(null); // Use the default executor
        server.start();
        System.out.println("Server is listening on port " + port);
    }

    static class TaxCalculatorHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("GET".equals(exchange.getRequestMethod())) {
                // Read the request body
                InputStream inputStream = exchange.getRequestBody();
                String requestBody = new String(inputStream.readAllBytes(), StandardCharsets.UTF_8);

                // Parse the JSON input
                JSONObject jsonInput = new JSONObject(requestBody);
                String city = jsonInput.getString("city");
                String vehicleType = jsonInput.getString("vehicleId");
                JSONArray jsonDateTimes = jsonInput.getJSONArray("travelDates");
                List<String> dateTimes = new ArrayList<>();
                for (int i = 0; i < jsonDateTimes.length(); i++) {
                    dateTimes.add(jsonDateTimes.getString(i));
                }

                // Create an instance of CongestionTaxCalculator
                CongestionTaxCalculator taxCalculator = new CongestionTaxCalculator(city, vehicleType);

                // Calculate the tax
                int tax = taxCalculator.calculateTax(dateTimes);

                // Prepare the response
                JSONObject jsonResponse = new JSONObject();
                LocalDateTime currentDateTime = LocalDateTime.now();
                jsonResponse.put("Congestion Tax:", tax);
                jsonResponse.put("Vehicle type:", vehicleType);
                jsonResponse.put("Timestamp:", currentDateTime);
                String response = jsonResponse.toString();

                exchange.getResponseHeaders().set("Content-Type", "application/json");
                exchange.sendResponseHeaders(200, response.length());

                // Send the response
                try (OutputStream os = exchange.getResponseBody()) {
                    os.write(response.getBytes());
                }
            } else {
                // todo: improve error handling requirements and implementation
                // Method not allowed
                String response = "Method Not Allowed";
                exchange.sendResponseHeaders(405, response.length());
                try (OutputStream os = exchange.getResponseBody()) {
                    os.write(response.getBytes());
                }
            }
        }
    }
}