#!/usr/bin/env python3

from products_feed import feed_update
from products_feed import feed_extract
from products_feed.file_sync_mngr import fscmngr_main as file_sync_mngr
from products_feed.file_sync_mngr.bol_stock_update_via_excel import (
    create_bol_stock_file,
)


def update_and_extract_feeds():
    print("Aktualizacja i ekstrakcja feedów...")
    feed_update.update_vida_feed()
    feed_update.update_big_buy_feed()
    feed_extract.extract_feeds()


def filter_products_feeds():
    while True:
        try:
            word_for_filter = input(
                "Wpisz słowo, aby filtrować produkty, lub q, aby wyjść: "
            )
            if word_for_filter == "q":
                break
            else:
                file_sync_mngr.create_standard_feed_by(word_for_filter)
                file_sync_mngr.create_presta_feed(word_for_filter)
                print("Wybrano produkty z frazą: ", word_for_filter)
                print("Pliki zostały wygenerowane. Kontynuuj...")
        except KeyboardInterrupt:
            print("Przerwano przez użytkownika.")
        except Exception as e:
            print("Wystąpił błąd: ", e)


if __name__ == "__main__":
    while True:
        print("1. Update and extract feeds")
        print("2. Filter products feeds based on words")
        print("3. Create bol stock file for excel update.")
        print("Naciśnij q, aby wyjść.")
        try:
            choice = input("Wybierz opcję: ")

            if choice == "q":
                break
            elif int(choice) == 1:
                update_and_extract_feeds()
            elif int(choice) == 2:
                filter_products_feeds()
            elif int(choice) == 3:
                create_bol_stock_file()
            else:
                print("Niepoprawny wybór. Spróbuj ponownie.")
        except KeyboardInterrupt:
            print("Przerwano przez użytkownjsonika.")
        except Exception as e:
            print("Wystąpił błąd: ", e)
