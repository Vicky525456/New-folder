import kivy
import os
import json
import mysql.connector as sql
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from  connector import sql_cnnection,sql_update,sql_delete



class RegistrationForm(App):
    def build(self):
        self.title="Basic form"
        layout = BoxLayout(orientation='vertical',padding=30,spacing=10)

        head_label=Label(text="Basic Registration Form",font_size=26,bold=True,height=40)
        id_label=Label(text="IDno",font_size=18)
        self.id_input=TextInput(multiline=False,font_size=15)
        name_label=Label(text="Name",font_size=18)
        self.name_input=TextInput(multiline=False,font_size=15)
        age_label=Label(text="Age",font_size=18)
        self.age_input=TextInput(multiline=False,font_size=15)
        mobilenumber_label=Label(text="Mobile Number",font_size=18)
        self.mobilenumber_input=TextInput(multiline=False,font_size=15)
        mail_label=Label(text="Mail ID",font_size=18)
        self.mail_input=TextInput(multiline=False,font_size=15)
        submit_button=Button(text="Register",font_size=18,on_press=self.register)
        sql_button = Button(text="Saved Data", font_size=18)
        dropdown = DropDown()

        show_button = Button(text='Show Stored Data ', size_hint_y=None, height=40)
        show_button.bind(on_release=lambda btn: self.show_button())
        dropdown.add_widget(show_button)

        sql_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(sql_button, 'text', x))
        update_button = Button(text="update Data", font_size=18, on_press=self.update_entry)
        delete_button = Button(text="Delete Data", font_size=18, on_press=self.delete)


        layout.add_widget(head_label)
        layout.add_widget(id_label)
        layout.add_widget(self.id_input)
        layout.add_widget(name_label)
        layout.add_widget(self.name_input)
        layout.add_widget(age_label)
        layout.add_widget(self.age_input)
        layout.add_widget(mobilenumber_label)
        layout.add_widget(self.mobilenumber_input)
        layout.add_widget(mail_label)
        layout.add_widget(self.mail_input)
        layout.add_widget(submit_button)
        layout.add_widget(sql_button)
        layout.add_widget(update_button)
        layout.add_widget(delete_button)

    


       
        return layout
    
    

    def show_button(self):

        mydb=sql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="mydatabase"
        )
        cursor=mydb.cursor()
        cursor.execute("SELECT id,name FROM user ORDER BY s_number")
        results=cursor.fetchall()
        cursor.close()
        mydb.close()
        popup_content = GridLayout(cols=1, spacing=1, size_hint_y=None)
        popup_content.bind(minimum_height=popup_content.setter('height'))
        for row in results:
            button = Button(text=str(row), size_hint_y=None, height=40)
            button.bind(on_press=lambda instance, id=row[0]: self.button_act(id))
            popup_content.add_widget(button)
        scroll_view = ScrollView(size_hint=(None, None), size=(300,180))
        scroll_view.add_widget(popup_content)
        popup = Popup(title="Stored Data", content=scroll_view, size_hint=(None, None), size=(400, 250))
        popup.open()

    def button_act(self, id):
        print(f"Searching for ID: {id}")
        filename = r"C:\New folder\data.txt"
    
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                try:
                    all_data = json.load(file)
                except json.JSONDecodeError:
                    all_data = []
        else:
            all_data = []

        print(f"Loaded data: {all_data}")

        found = False
        for entry in all_data:
            if str(entry['IDno']).strip().lower() == str(id).strip().lower():
                print(f"Found entry: {entry}")
                self.id_input.text = entry['IDno']
                self.name_input.text = entry['Name'] 
                
                self.age_input.text = entry['Age']
                self.mobilenumber_input.text = entry['Mobile Number']
                self.mail_input.text = entry['Mail ID']
                found = True
                break

        if not found:
            message = f"No entry found for ID: {id}"
            popup = Popup(title="Error", content=Label(text=message), size_hint=(None, None), size=(400, 200))
            popup.open()


        if not found:
            message = f"No entry found for ID: {id}"
            popup = Popup(title="Error", content=Label(text=message), size_hint=(None, None), size=(400, 200))
            popup.open()

        
        


    
    
    
    def register(self,instance):
        id=self.id_input.text
        name=self.name_input.text
        age=self.age_input.text
        mobilenumber=self.mobilenumber_input.text
        mail=self.mail_input.text
         

        if id.strip() =='' or name.strip() == '' or age.strip() == '' or mobilenumber.strip ==  '' or mail.strip() =='':
            message="Please fill the feilds"

        elif not age.isdigit():
            message = "Please enter correct age"

        elif not mobilenumber.isdigit() or len(mobilenumber) != 10:
            message = "Please enter a valid 10-digit mobile number"

        elif not'@' in mail:
            message = "Please enter a valid mail id "


        else:
            sql_cnnection(id,name,age,mobilenumber,mail)

            filename = r"C:\New folder\data.txt"
            data = {
                'IDno':id,
                'Name': name,
                'Age': age,
                'Mobile Number': mobilenumber,
                'Mail ID': mail
            }

            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    try:
                        all_data = json.load(file)
                    except json.JSONDecodeError:
                        all_data = []
            else:
                all_data = []
            all_data.append(data)

            with open(filename, 'w') as file:
                json.dump(all_data, file, indent=5)
            message="Registration Successfull!\n\n Thank You For Your Respose"  
      
        
        popup=Popup(title="Registration Status",content=Label(text=message),size_hint=(None,None),size=(400,200))
        popup.open()    
    def update_entry(self, instance,):
        id = self.id_input.text.strip()
        name = self.name_input.text
        age = self.age_input.text
        mobilenumber = self.mobilenumber_input.text
        mail = self.mail_input.text
        sql_update(id,name,age,mobilenumber,mail)
        



        filename = r"C:\New folder\data.txt"
        if id.strip() =='' or name.strip() == '' or age.strip() == '' or mobilenumber.strip ==  '' or mail.strip() =='':
            message="Please fill the feilds"

        elif not age.isdigit():
            message = "Please enter correct age"

        elif not mobilenumber.isdigit() or len(mobilenumber) != 10:
            message = "Please enter a valid 10-digit mobile number"

        elif not'@' in mail:
            message = "Please enter a valid mail id "

        else:
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    try:
                        all_data = json.load(file)
                    except json.JSONDecodeError:
                        all_data = []
            else:
                all_data = []



            for entry in all_data:
                if entry['IDno'] == id:
                    
                    
                    entry['Name'] = name
                    entry['Age'] = age
                    entry['Mobile Number'] = mobilenumber
                    entry['Mail ID'] = mail
                    break

            if entry['IDno'] == id:
                with open(filename, 'w') as file:
                    json.dump(all_data, file, indent=5)
                message = f"Entry for {id} updated successfully!"
            else:
                message = f"No entry found for {id}."

        popup = Popup(title="Update Status", content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()


    
    
    def delete(self, instance):
        id = self.id_input.text.strip()
       # name = self.name_input.text
        #age = self.age_input.text
        #mobilenumber = self.mobilenumber_input.text
        #mail = self.mail_input.text
        
        sql_delete(id,)



        filename = r"C:\New folder\data.txt"

        if not id:
            message = "Please enter the id to delete."
        else:
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    try:
                        all_data = json.load(file)
                    except json.JSONDecodeError:
                        all_data = []
            else:
                all_data = []

            updated_data = [entry for entry in all_data if entry['IDno'] != id]

            if len(updated_data) < len(all_data):
                with open(filename, 'w') as file:
                    json.dump(updated_data, file, indent=5)
                message = f"Entry for {id} deleted successfully!"
            else:
                message = f"No entry found for {id}."

        popup = Popup(title="Delete Status", content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()





if __name__== '__main__':
    RegistrationForm().run()