import requests
from bs4 import BeautifulSoup


class TrainChecker:

    def __init__(self, date, from_station, to_station):
        # date format: dd.mm.yyyy

        self.date = date
        self.from_station = from_station
        self.to_station = to_station

    @staticmethod
    def _parse_response(response):
        soup = BeautifulSoup(response.text, "html.parser")
        trains_html = soup.select(".results-table-item")

        trains = []
        for train in trains_html:
            train_data = {
                "train_number": train.select_one(".train-number").text.strip(),
                "departure_time": train.select_one(".col-custom-3").select_one(".trip-time").text.strip(),
                "arrival_time": train.select_one(".col-custom-5").select_one(".trip-time").text.strip(),
                "travel_time": train.select_one(".trip-duration").text.strip(),

            }
            places = []
            for place_elem in train.select(".col-custom-6"):
                places.append({
                    'type': place_elem.select_one(".wagon-type").text.strip(),
                    'count': place_elem.select_one(".place-count").text.strip(),
                })
            train_data['places'] = places
            trains.append(train_data)

        return trains

    def check(self):
        target_url = f"https://e-kvytok.ua/ru/search?date={self.date}&from={self.from_station}&to={self.to_station}"
        response = requests.get(target_url)
        return self._parse_response(response)
