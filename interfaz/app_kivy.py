import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

from codigo.main import crear_recordatorio, cargar_recordatorios, eliminar_recordatorio


class Pantalla(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        # Inputs
        self.titulo = TextInput(hint_text="Titulo")
        self.add_widget(self.titulo)

        self.descripcion = TextInput(hint_text="Descripcion")
        self.add_widget(self.descripcion)

        self.fecha = TextInput(hint_text="Fecha (YYYY-MM-DD)")
        self.add_widget(self.fecha)

        self.hora = TextInput(hint_text="Hora (HH:MM)")
        self.add_widget(self.hora)

        # Botón guardar
        boton = Button(text="Guardar recordatorio")
        boton.bind(on_press=self.guardar)
        self.add_widget(boton)

        # Lista de recordatorios
        self.lista = Label(text="")
        self.add_widget(self.lista)

        # Input para eliminar
        self.indice_eliminar = TextInput(hint_text="Número a eliminar")
        self.add_widget(self.indice_eliminar)

        # Botón eliminar
        boton_eliminar = Button(text="Eliminar recordatorio")
        boton_eliminar.bind(on_press=self.eliminar)
        self.add_widget(boton_eliminar)

        # Mostrar al iniciar
        self.mostrar_recordatorios()

    def mostrar_recordatorios(self):
        recordatorios = cargar_recordatorios()

        texto = ""

        for i, r in enumerate(recordatorios):
            texto += f"{i+1}. {r['titulo']} - {r['fecha']} {r['hora']}\n"

        self.lista.text = texto

    def guardar(self, obj):

        crear_recordatorio(
            self.titulo.text,
            self.descripcion.text,
            self.fecha.text,
            self.hora.text
        )

        print("Recordatorio guardado")

        # Limpiar campos
        self.titulo.text = ""
        self.descripcion.text = ""
        self.fecha.text = ""
        self.hora.text = ""

        self.mostrar_recordatorios()

    def eliminar(self, obj):
        try:
            indice = int(self.indice_eliminar.text) - 1
            eliminar_recordatorio(indice)

            print("Recordatorio eliminado")

            self.indice_eliminar.text = ""

            self.mostrar_recordatorios()

        except:
            print("Índice inválido")


class MiRecordatorioApp(App):

    def build(self):
        return Pantalla()


MiRecordatorioApp().run()