from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from codigo.main import crear_recordatorio

class Pantalla(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.titulo=TextInput(hint_text="Titulo")
        self.add_widget(self.titulo)

        self.descripcion=TextInput(hint_text="Descripcion")
        self.add_widget(self.descripcion)

        self.fecha=TextInput(hint_text="Fecha (YYYY-MM-DD)")
        self.add_widget(self.fecha)

        self.hora=TextInput(hint_text="Hora (HH:MM)")
        self.add_widget(self.hora)

        boton=Button(text="Guardar recordatorio")
        boton.bind(on_press=self.guardar)

        self.add_widget(boton)

    def guardar(self,obj):

        crear_recordatorio(
            self.titulo.text,
            self.descripcion.text,
            self.fecha.text,
            self.hora.text
        )

        print("Recordatorio guardado")

class MiRecordatorioApp(App):

    def build(self):
        return Pantalla()

MiRecordatorioApp().run()