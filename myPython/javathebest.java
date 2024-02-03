import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ChipShopDetector {

    private final String apiKey = "AIzaSyB5GmwKRaZnm7-pHlj23TWo601eXUXH29o";
    private final String baseUrl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json";
    private final String detailsUrl = "https://maps.googleapis.com/maps/api/place/details/json";

    public List<Result> searchChipShop(String location) {
        String searchUrl = baseUrl + "?location=" + location + "&radius=10000&keyword=Fish+%26+chips+shop&key=" + apiKey;
        List<Result> results = new ArrayList<>();

        try {
            URL url = new URL(searchUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");

            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            StringBuilder response = new StringBuilder();
            String line;

            while ((line = reader.readLine()) != null) {
                response.append(line);
            }

            reader.close();

            // Parse JSON response
            // (Assuming you have a Result class to store the data)
            // You need to implement the Result class accordingly.
            // The structure of Result class may vary based on the actual response from the API.
            // For simplicity, I'm assuming a basic structure here.
            results = parseResults(response.toString());

        } catch (Exception e) {
            e.printStackTrace();
        }

        // Sort the results by user ratings total in descending order
        Collections.sort(results, (result1, result2) -> Integer.compare(result2.getUserRatingsTotal(), result1.getUserRatingsTotal()));

        return results;
    }

    public Result getPlaceDetails(String placeId) {
        String detailsUrl = this.detailsUrl + "?place_id=" + placeId + "&key=" + apiKey;
        Result result = new Result();

        try {
            URL url = new URL(detailsUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");

            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            StringBuilder response = new StringBuilder();
            String line;

            while ((line = reader.readLine()) != null) {
                response.append(line);
            }

            reader.close();

            // Parse JSON response
            // (Assuming you have a Result class to store the data)
            // You need to implement the Result class accordingly.
            // The structure of Result class may vary based on the actual response from the API.
            // For simplicity, I'm assuming a basic structure here.
            result = parseResultDetails(response.toString());

        } catch (Exception e) {
            e.printStackTrace();
        }

        return result;
    }

    private List<Result> parseResults(String json) {
        // Implement the parsing logic based on the actual response from the API
        // For simplicity, I'm assuming a basic structure here.
        // You need to adapt this based on the actual JSON structure.
        List<Result> results = new ArrayList<>();

        // Parse the JSON and populate the results list

        return results;
    }

    private Result parseResultDetails(String json) {
        // Implement the parsing logic based on the actual response from the API
        // For simplicity, I'm assuming a basic structure here.
        // You need to adapt this based on the actual JSON structure.
        Result result = new Result();

        // Parse the JSON and populate the result object

        return result;
    }

    public static void main(String[] args) {
        ChipShopDetector chipDetector = new ChipShopDetector();

        // Example: Search for chip shops near a specific location
        String currentLocation = "53.871894644258305, -2.3913812786981548";  // Enter your coordinates
        List<Result> chipResults = chipDetector.searchChipShop(currentLocation);

        if (!chipResults.isEmpty()) {
            System.out.println("Chip Shops found:");
            for (int i = 0; i < chipResults.size(); i++) {
                Result result = chipResults.get(i);
                System.out.println((i + 1) + ". " + result.getName() + " - Rating: " + result.getRating() +
                        " - Rated by " + result.getUserRatingsTotal() + " people");
            }

            // Example: Display details for the first chip shop
            Result selectedChipShop = chipResults.get(0);
            Result details = chipDetector.getPlaceDetails(selectedChipShop.getPlaceId());

            System.out.println("\nDetails for selected Chip Shop:");
            System.out.println("Name: " + details.getName());
            System.out.println("Address: " + details.getAddress());
            System.out.println("Phone: " + details.getFormattedPhoneNumber());
            System.out.println("Opening Hours: " + details.getOpeningHours());

        } else {
            System.out.println("No suitable Chip Shops found.");
        }
    }
}