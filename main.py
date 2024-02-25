import time

import requests

from config import TG_BOT_TOKEN, TG_CHAT_ID, stations
from targets.e_kvytok import TrainChecker


def make_message(trains):
    result_message = "Квитки в наявності:\n\n"
    for i in trains:
        result_message += f"Поїзд: {i['train_number']}\n"
        result_message += f"Відправлення: {i['departure_time']}\n Прибуття: {i['arrival_time']}\n Час в дорозі: {i['travel_time']}\n\n"
        for place in i['places']:
            result_message += f"{place['type']} - {place['count']}шт\n"
        result_message += "\n\n"
    return result_message


def check_and_send(data, from_station, to_station):
    checker = TrainChecker(data, from_station, to_station)

    while True:
        trains = checker.check()
        # filter
        trains = [train for train in trains if '098 Л' in train['train_number']]

        if trains:
            message = make_message(trains)
            requests.get(f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={TG_CHAT_ID}&text={message}")
        else:
            print("No trains")
        time.sleep(20)


if __name__ == "__main__":
    check_and_send("25.02.2024", stations["Луцьк"], stations["Київ"])
