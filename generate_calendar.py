from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pickle


class generate_calendar():
    def __init__(self, dict_classes, groups_list):
        # Fonction pour ajouter un événement
        def add_event(calendar, summary, start_time, duration, location=None, description=None):
            event = Event()
            event.add('summary', summary)
            event.add('dtstart', start_time)
            event.add('duration', duration)
            if location:
                event.add('location', location)
            if description:
                event.add('description', description)
            calendar.add_component(event)

        for groups in groups_list:
            list_classes = dict_classes[groups]

            # Créer un objet Calendar
            cal = Calendar()

            # Définir les propriétés du calendrier
            cal.add('prodid', '-//My Calendar//example.com//')
            cal.add('version', '2.0')

            for event in list_classes:
                print(event)
                title = event[0]
                type = event[2]

                hours = event[1]
                start = (hours[:2], hours[3:5])
                end = (hours[8:10], hours[11:])
                duration = int(end[0]) - int(start[0]) + (int(end[1]) - int(start[1])) / 60

                date = event[-1]
                year = int(date[-4:])
                month = int(date[3:5])
                day = int(date[:2])
                group = event[-2]
                location = event[-3]
                # print(title, duration, start, day, month, year, group, location)

                # Ajouter des événements
                add_event(cal, type+" - "+title+" - "+group, datetime(year, month, day, int(start[0]), int(start[1])), timedelta(hours=duration),
                          location, group)

            # Écrire le calendrier dans un fichier .ics
            with open('et3_cal/' + str(groups[0]).replace(" ", "") + '.ics', 'wb') as f:
                f.write(cal.to_ical())

            print("Calendrier créé avec succès et enregistré dans " + str(groups[0]) + ".ics'")


with open("et3_classes.pkl", "rb") as file:
    dict_saved_classes = pickle.load(file)
    print(dict_saved_classes)

groups_list = (('ET3 INFO', 'ET3 INFO Gr1', 'ET3 INFO Gr2', 'ET3 Promo'), ('ET3 MATE', 'ET3 MATE Gr1',
               'ET3 MATE Gr2', 'ET3 Promo'), ('ET3 ELEC', 'ET3 ELEC Gr1', 'ET3 ELEC Gr2', 'ET3 Promo'), ('ET3 PHOT',
               'ET3 PHOT Gr1', 'ET3 PHOT Gr2', 'ET3 Promo'), ('ET3 ANG 1', 'ET3 COM 1'), ('ET3 ANG 2', 'ET3 COM 2'),
               ('ET3 ANG 3', 'ET3 COM 3'), ('ET3 ANG 4', 'ET3 COM 4'), ('ET3 ANG 1', 'ET3 COM 1'),
               ('ET3 ANG 6', 'ET3 COM 6'), ('ET3 ANG 7', 'ET3 COM 7'), ('ET3 ANG 8', 'ET3 COM 8'), ('ET3 ECO 1', ''),
               ('ET3 ECO 2', ''), ('ET3 ECO 3', ''), ('ET3 TC Gr1',''), ('ET3 TC Gr2', ''), ('ET3 TC Gr3', ''),
               ('ET3 TC Gr4', ''), ('ET3 TC Gr5', ''))

calendar_update = generate_calendar(dict_saved_classes, groups_list)