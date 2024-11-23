from dashboard import Dashboard
from web_scraper import WebScraper
import pickle

#webscraper = WebScraper()


promotions_calendars = {"ET3": ["et3_cal/ET3ANG", "et3_cal/ET3COM", "et3_cal/ET3ECO", "et3_cal/ET3ELEC",
                               "et3_cal/ET3INFO", "et3_cal/ET3MATE", "et3_cal/ET3PHOT", "et3_cal/ET3TC"]}

#with open("et3_classes.pkl", "rb") as file:
#    dict_saved_classes = pickle.load(file)
#print(dict_saved_classes)
dashboard = Dashboard()
#dashboard.webscraping()
dashboard.update_html()
