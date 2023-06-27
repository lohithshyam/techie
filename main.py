from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField

# import info_collector
import socket
import json
import requests

from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.transition import MDFadeSlideTransition

Builder.load_string('''
<MainScreen>:
    MDLabel:
        text:"Techi"
        pos_hint:{"center_y":0.8}
        halign:"center"
        font_size:"30dp"
        bold:True
        
    MDRaisedButton:
        text: "Info Collector"
        pos_hint:{"center_x":0.2,"center_y":0.5}
        on_release: root.manager.current = "info_collector"
        
    MDRaisedButton:
        text: "Number Tracker"
        pos_hint:{"center_x":0.8,"center_y":0.5}
        on_release: root.manager.current = "number_tracker"
        
    

<InfoCollector>:
    MDLabel:
        text:"Info Collector"
        pos_hint:{"center_y":0.9}
        halign:"center"
        font_size:"30dp"
        bold:True
    MDTextField:
        id:get_text
        mode:"rectangle"
        hint_text:"Enter the URL"
        size_hint:0.5,.1
        pos_hint:{"center_x":0.5,"center_y":0.8}
    MDRaisedButton:
        text:"Get"
        pos_hint:{"center_x":0.8,"center_y":0.8}
        on_release:root.clicked()
    MDBoxLayout:
        orientation:"vertical"
        size_hint:0.5,0.7
        pos_hint:{"center_x":0.5}
        MDLabel:
            id:location
            text:"Location : "
            pos_hint:{"center_y":0.7}
            halign:"center"
        MDLabel:
            id:region
            text:"Region : "
            pos_hint:{"center_y":0.6}
            halign:"center"
        MDLabel:
            id:city
            text:"City : "
            pos_hint:{"center_y":0.5}
            halign:"center"
        MDLabel:
            id:country
            text:"Country : "
            pos_hint:{"center_y":0.4}
            halign:"center"
        MDLabel:
            id:timezone
            text:"Timezone : "
            pos_hint:{"center_y":0.3}
            halign:"center"
        MDLabel:
            id:org
            text:"Organization : "
            pos_hint:{"center_y":0.2}
            halign:"center"
        MDLabel:
            id:postal
            text:"Postal : "
            pos_hint:{"center_y":0.1}
            halign:"center"
        
    
    MDRaisedButton:
        text:"Back"
        pos_hint:{"center_x":0.05,"center_y":0.05}
        on_release: 
            root.manager.current = "main_screen"
    
<NumberTracker>:
    MDLabel:
        id:header
        text:"Number Tracker"
        pos_hint:{"center_y":0.9}
        halign:"center"
        font_size:"30dp"
        bold:True
    MDTextField:
        id:get_number
        hint_text:"Enter Phone Number"
        helper_text: "Enter with country code ( Eg : +91xxxxxxxxxx )"
        mode:"rectangle"
        size_hint:0.5,.1
        pos_hint:{"center_x":0.5,"center_y":0.8}
    MDRaisedButton:
        text:"Get"
        pos_hint:{"center_x":0.8,"center_y":0.8}
        on_release:root.clicked()
    MDBoxLayout:
        orientation:"vertical"
        size_hint:0.5,0.7
        pos_hint:{"center_x":0.5}
        MDLabel:
            id:location
            text:"Location : "
            pos_hint:{"center_y":0.7}
            halign:"center"
        MDLabel:
            id:carrier
            text:"Carrier Name :"
            pos_hint:{"center_y":0.6}
            halign:"center"
        MDLabel:
            id:latitude
            text:"Latitude : "
            pos_hint:{"center_y":0.5}
            halign:"center"
        MDLabel:
            id:longitude
            text:"Longitude : "
            pos_hint:{"center_y":0.4}
            halign:"center"           
    MDRaisedButton:
        text:"Back"
        pos_hint:{"center_x":0.05,"center_y":0.05}
        on_release: 
            root.manager.current = "main_screen"
''')


class Techi(MDApp):
    def build(self):
        screen = MDScreenManager(transition=MDFadeSlideTransition())
        screen.add_widget(MainScreen(name="main_screen"))
        screen.add_widget(InfoCollector(name="info_collector"))
        screen.add_widget(NumberTracker(name="number_tracker"))
        return screen


class MainScreen(MDScreen):
    pass


class InfoCollector(MDScreen):

    def clicked(self):
        url = self.ids.get_text.text

        print("THE IP FOR " + url + " IS ", socket.gethostbyname(url))

        host_ip = socket.gethostbyname(url)

        req_two = requests.get("https://ipinfo.io/" + host_ip + "/json")
        resp_ = json.loads(req_two.text)

        print("Location: " + resp_["loc"])
        self.ids.location.text = "Location : " + resp_["loc"]
        print("Region: " + resp_["region"])
        self.ids.region.text = "Region : " + resp_["region"]
        print("City: " + resp_["city"])
        self.ids.city.text = "City : " + resp_["city"]
        print("Country: " + resp_["country"])
        self.ids.country.text = "Country : " + resp_["country"]
        print("Timezone:" + resp_["timezone"])
        self.ids.timezone.text = "Timezone : " + resp_["timezone"]
        print("Org:" + resp_["org"])
        self.ids.org.text = "Organization : " + resp_["org"]
        print("Postal:" + resp_["postal"])
        self.ids.postal.text = "Postal : " + resp_["postal"]


class NumberTracker(MDScreen):

    def clicked(self):
        import phonenumbers
        import opencage
        # import folium
        from phonenumbers import geocoder

        number = self.ids.get_number.text

        pepnumber = phonenumbers.parse(number)
        location = geocoder.description_for_number(pepnumber, "en")
        print(location)
        self.ids.location.text = "Location : " + location

        from phonenumbers import carrier

        service_pro = phonenumbers.parse(number)
        print(carrier.name_for_number(service_pro, "en"))
        self.ids.carrier.text = "Carrier Name : " + carrier.name_for_number(service_pro, "en")

        from opencage.geocoder import OpenCageGeocode

        key = '4edf23a515ba4f1e910f3b1824748aaf'

        geocoder = OpenCageGeocode(key)
        query = str(location)
        results = geocoder.geocode(query)

        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']

        print(lat, lng)
        self.ids.latitude.text = "Latitude : " + str(lat)
        self.ids.longitude.text = "Longitude : " + str(lng)
        # mymap = folium.Map(location=[lat, lng], zoom_start=9)
        # folium.Marker([lat, lng], popup=location).add_to(mymap)
        # mymap.save("mylocation.html")


if __name__ == '__main__':
    Techi().run()
