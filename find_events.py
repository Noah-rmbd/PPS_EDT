import re
import icalendar
from datetime import datetime, timedelta

##RÉSOLU : il manque systématiquement le dernier cours de la semaine
##Ajouter infos sur les profs et le cas où il y aurait trop ou trop peu d'info
##Ajouter des jours feriés
##Ne parcourir dans le site web que la partie emploi du temps et pas le reste
##Créer un bot qui parcourt chaque semaine et crée les calendriers ical avant de parcourir

class FindEvents():
    def __init__(self, document):
        # Define tags that surrounds the classes
        start_classes = '<b unselectable="on" class="eventText">'
        end_classes = '</div></div></div><div' #style="cursor: auto; position: absolute; left:'

        # Regex pattern to find the classes information between the two tags
        pattern = re.escape(start_classes) + r'(.*?)' + re.escape(end_classes)

        # Use re.findall to find all the classes between the two tags defined later
        matches = re.findall(pattern, document, re.DOTALL)

        classes_count = 0
        classes_list = []

        for classes in matches:
            classes_count += 1

            # Split and clean informations in classes text
            classes = classes.replace("</b>", "")
            class_informations = classes.replace("<br>", ",")
            class_informations = class_informations.split(",")
            class_informations = class_informations[:-1]
            classes_list.append(class_informations)

        # Define tags that surround the dates
        start_day_tag = '<span style="display: inline-block;height: 50%;width: 1px;"></span>'
        end_day_tag = '</div>'

        # Regex pattern to find the date between the two tags
        pattern_date = re.escape(start_day_tag) + r'(.*?)' + re.escape(end_day_tag)

        # Use re.findall to find all the dates between the two tags defined later
        dates = re.findall(pattern_date, document, re.DOTALL)
        dates = dates[1:]

        week_list = []
        vacation_dates = ['11/11/2024']
        for element in dates:
            if element[-10:] not in vacation_dates:
                week_list.append(element[-10:])

        week_index = 0

        # Sort classes per day
        # Initialize the first day for the first class
        classes_list[0].append(week_list[week_index])

        # Add the day that corresponds to each class in the classes_list
        for classes_index in range(1, len(classes_list)):
            if classes_list[classes_index][1][:5] < classes_list[classes_index-1][1][:5]:
                week_index += 1

            classes_list[classes_index].append(week_list[week_index])

        # List of classes groups
        groups_list = (('ET3 INFO', 'ET3 INFO Gr1', 'ET3 INFO Gr2', 'ET3 Promo'), ('ET3 MATE', 'ET3 MATE Gr1',
               'ET3 MATE Gr2', 'ET3 Promo'), ('ET3 ELEC', 'ET3 ELEC Gr1', 'ET3 ELEC Gr2', 'ET3 Promo'), ('ET3 PHOT',
               'ET3 PHOT Gr1', 'ET3 PHOT Gr2', 'ET3 Promo'), ('ET3 ANG 1', 'ET3 COM 1'), ('ET3 ANG 2', 'ET3 COM 2'),
               ('ET3 ANG 3', 'ET3 COM 3'), ('ET3 ANG 4', 'ET3 COM 4'), ('ET3 ANG 1', 'ET3 COM 1'),
               ('ET3 ANG 6', 'ET3 COM 6'), ('ET3 ANG 7', 'ET3 COM 7'), ('ET3 ANG 8', 'ET3 COM 8'), ('ET3 ECO 1', ''),
               ('ET3 ECO 2', ''), ('ET3 ECO 3', ''), ('ET3 TC Gr1',''), ('ET3 TC Gr2', ''), ('ET3 TC Gr3', ''),
               ('ET3 TC Gr4', ''), ('ET3 TC Gr5', ''))

        # Dictionnary that contain the list of classes (attributes) for each group (keys)
        self.dict_classes = {}
        for group in groups_list:
            self.dict_classes[group] = []
            # Search in classes_list the classes for the selected group
            for classes in classes_list:
                if classes[-2] in group:
                    self.dict_classes[group].append(classes)

        #self.generate_calendar(dict_classes, groups_list)
        #print(classes_list)
        #print(self.dict_classes)
        #print(dict_classes[('ET3 TC Gr1', 'ET3 TC Gr2', 'ET3 TC Gr3', 'ET3 TC Gr4', 'ET3 TC Gr5', 'ET3 TC Gr6', 'ET3 TC Gr7', 'ET3 TC Gr8')])
        #for group in groups_list:
        #    print(group, dict_classes[group])

    def generate_calendar(self, dict_classes, groups_list):
        from icalendar import Calendar, Event
        from datetime import datetime, timedelta

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

                hours = event[1]
                start = (hours[:2], hours[3:5])
                end = (hours[8:10], hours[11:])
                duration = int(end[0]) - int(start[0]) + (int(end[1]) - int(start[1]))/60

                date = event[-1]
                year = int(date[-4:])
                month = int(date[3:5])
                day = int(date[:2])
                group = event[-2]
                location = event[-3]
                #print(title, duration, start, day, month, year, group, location)

                # Ajouter des événements
                add_event(cal, title, datetime(year, month, day, int(start[0]), int(start[1])), timedelta(hours=duration),
                          location, group)


            # Écrire le calendrier dans un fichier .ics
            with open(str(groups[0])+'.ics', 'wb') as f:
                f.write(cal.to_ical())

            print("Calendrier créé avec succès et enregistré dans " + str(groups[0]) + ".ics'")


# Exemple de chaîne de caractères
#with open('et3_html/13.html', 'r') as file:
#    long_string = file.read()

#resultat = FindEvents(long_string)