from web_scraper import WebScraper
from find_events import FindEvents
import pickle

class Dashboard():
    def __init__(self):
        self.promotions = ["ET3"]

        self.promotions_groups = {"ET3": (('ET3 INFO', 'ET3 INFO Gr1', 'ET3 INFO Gr2', 'ET3 Promo'),
            ('ET3 MATE', 'ET3 MATE Gr1', 'ET3 MATE Gr2', 'ET3 Promo'), ('ET3 ELEC', 'ET3 ELEC Gr1',
            'ET3 ELEC Gr2', 'ET3 Promo'), ('ET3 PHOT', 'ET3 PHOT Gr1', 'ET3 PHOT Gr2', 'ET3 Promo'),
            ('ET3 ANG 1', 'ET3 COM 1'), ('ET3 ANG 2', 'ET3 COM 2'), ('ET3 ANG 3', 'ET3 COM 3'),
            ('ET3 ANG 4', 'ET3 COM 4'), ('ET3 ANG 1', 'ET3 COM 1'), ('ET3 ANG 6', 'ET3 COM 6'),
            ('ET3 ANG 7', 'ET3 COM 7'), ('ET3 ANG 8', 'ET3 COM 8'), ('ET3 ECO 1', ''), ('ET3 ECO 2', ''),
            ('ET3 ECO 3', ''), ('ET3 TC Gr1', ''), ('ET3 TC Gr2', ''), ('ET3 TC Gr3', ''), ('ET3 TC Gr4', ''),
            ('ET3 TC Gr5', ''))}

    #
    def webscraping(self):
        webscraper = WebScraper()

    # Update the pickle dictionary classes database with the classes found in html
    def update_database(self, dict_found_classes):
        # Load database
        with open("et3_classes.pkl", "rb") as file:
            dict_saved_classes = pickle.load(file)

        # Update database with new classes
        for group in self.promotions_groups["ET3"]:
            for classes in dict_found_classes[group]:
                #if classes not in dict_saved_classes[group]:
                dict_saved_classes[group].append(classes)

        # Save database
        with open("et3_classes.pkl", "wb") as file:
            pickle.dump(dict_saved_classes, file)

    # Read every html file to detect classes into it and then update_classes with the found classes
    def update_html(self):
        self.delete_database()
        # For each html week file we read the file and detect classes
        for week in range(12, 19):
            with open('et3_html/' + str(week) + '.html', 'r') as file:
                html_file = file.read()

            # Find classes in the selected html file
            events_et3 = FindEvents(html_file)
            dict_found_classes = events_et3.dict_classes

            # Add the classes found in the pickle dictionary database
            self.update_database(dict_found_classes)

    def delete_database(self):
        reinitiated_database = dict()
        for group in self.promotions_groups["ET3"]:
            reinitiated_database[group] = []

        with open("et3_classes.pkl", "wb") as file:
            pickle.dump(reinitiated_database, file)
