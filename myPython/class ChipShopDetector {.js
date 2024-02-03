class ChipShopDetector {
    constructor() {
        this.apiKey = 'AIzaSyB5GmwKRaZnm7-pHlj23TWo601eXUXH29o';
        this.baseUrl = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json';
    }

    async searchChipShop(location) {
        const params = {
            'location': location,
            'radius': 10000,  // Searching within a 10km radius
            //'type': 'restaurant',
            'keyword': 'Fish & chips shop',
            'key': this.apiKey,
        };

        const url = new URL(this.baseUrl);
        url.search = new URLSearchParams(params).toString();

        const response = await fetch(url);
        const data = await response.json();

        const results = [];

        for (const place of data.results || []) {
            if ((place.user_ratings_total || 0) >= 200 && (place.rating || 0) >= 4.2) {
                const result = {
                    'name': place.name,
                    'address': place.vicinity,
                    'rating': place.rating,
                    'user_ratings_total': place.user_ratings_total,
                    'has_restaurant': place.types.includes('restaurant'),
                    'place_id': place.place_id,
                };
                results.push(result);
            }
        }

        results.sort((a, b) => b.user_ratings_total - a.user_ratings_total);
        return results;
    }

    async getPlaceDetails(placeId) {
        const detailsUrl = 'https://maps.googleapis.com/maps/api/place/details/json';
        const params = {
            'place_id': placeId,
            'key': this.apiKey,
        };

        const url = new URL(detailsUrl);
        url.search = new URLSearchParams(params).toString();

        const response = await fetch(url);
        const details = (await response.json()).result || {};

        return details;
    }
}

// Example usage
const chipDetector = new ChipShopDetector();

// Example: Search for chip shops near a specific location
const currentLocation = "53.51302102475046, -2.1475010000006867";  // Enter your coords
chipDetector.searchChipShop(currentLocation)
    .then(chipResults => {
        if (chipResults.length > 0) {
            console.log("Chip Shops found:");
            chipResults.forEach((result, index) => {
                console.log(`${index + 1}. ${result.name} - Rating: ${result.rating} - Rated by ${result.user_ratings_total} people`);
            });

            // Example: Display details for the first chip shop
            const selectedChipShop = chipResults[0];
            chipDetector.getPlaceDetails(selectedChipShop.place_id)
                .then(details => {
                    console.log("\nDetails for selected Chip Shop:");
                    console.log(`Name: ${details.name}`);
                    console.log(`Address: ${details.formatted_address}`);
                    console.log(`Phone: ${details.formatted_phone_number}`);
                    console.log(`Opening Hours: ${details.opening_hours ? details.opening_hours.weekday_text : 'Not available'}`);
                })
                .catch(error => console.error("Error fetching place details:", error));
        } else {
            console.log("No suitable Chip Shops found.");
        }
    })
    .catch(error => console.error("Error fetching chip shops:", error));