import requests

class ChipShopDetector:
    def __init__(self):
        self.api_key = 'AIzaSyB5GmwKRaZnm7-pHlj23TWo601eXUXH29o'
        self.base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    def search_chip_shop(self, location):
        params = {
            'location': location,
            'radius': 10000,  # Searching within a 10km radius
            #'type': 'restaurant',
            'keyword': 'barber',
            'key': self.api_key,
        }

        response = requests.get(self.base_url, params=params)
        data = response.json()

        results = []

        for place in data.get('results', []):
            if place.get('user_ratings_total', 0) >= 150 and place.get('rating', 0) >= 4.2: #set  parameters of min user ratings total and minimum stars
                result = {
                    'name': place['name'],
                    'address': place['vicinity'],
                    'rating': place['rating'],
                    'user_ratings_total': place['user_ratings_total'],
                    'has_restaurant': 'restaurant' in place['types'],
                    'place_id': place['place_id'],
                }
                results.append(result)
        results = sorted(results, key=lambda x: x['user_ratings_total'], reverse=True)
        return results

    def get_place_details(self, place_id):
        details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
        params = {
            'place_id': place_id,
            'key': self.api_key,
        }

        response = requests.get(details_url, params=params)
        details = response.json().get('result', {})

        return details

if __name__ == "__main__":
    chip_detector = ChipShopDetector()

    # Example: Search for chip shops near a specific location
    current_location = "53.645822351561506, -1.7832425234801499"  # Enter you coords
    chip_results = chip_detector.search_chip_shop(current_location)

    if chip_results:
        print("Chip Shops found:")
        for index, result in enumerate(chip_results, start=1):
            print(f"{index}. {result['name']} - Rating: {result['rating']} - Rated by {result['user_ratings_total']} people")

        # Example: Display details for the first chip shop
        selected_chip_shop = chip_results[0]
        details = chip_detector.get_place_details(selected_chip_shop['place_id'])

        print("\nDetails for selected Chip Shop:")
        print(f"Name: {details.get('name')}")
        print(f"Address: {details.get('formatted_address')}")
        print(f"Phone: {details.get('formatted_phone_number')}")
        print(f"Opening Hours: {details.get('opening_hours', {}).get('weekday_text')}")

    else:
        print("No suitable Chip Shops found.")