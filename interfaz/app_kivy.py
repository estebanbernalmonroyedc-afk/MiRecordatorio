import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle

from codigo.main import crear_recordatorio, cargar_recordatorios, eliminar_recordatorio


class Pantalla(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=15, spacing=12, **kwargs)

        # ===== FONDO =====
        with self.canvas.before:
            Color(0.94, 0.95, 0.97, 1)  # gris suave moderno
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # ===== TITULO =====
        titulo_app = Label(
            text="MiRecordatorio",
            font_size=26,
            bold=True,
            size_hint=(1, 0.1),
            color=(0.1, 0.1, 0.1, 1)
        )
        self.add_widget(titulo_app)

        # ===== FORMULARIO =====
        form = BoxLayout(orientation="vertical", spacing=8, size_hint=(1, 0.45))

        self.titulo = TextInput(
            hint_text="Título",
            multiline=False,
            background_color=(1,1,1,1),
            foreground_color=(0,0,0,1)
        )
        form.add_widget(self.titulo)

        self.descripcion = TextInput(
            hint_text="Descripción",
            multiline=False,
            background_color=(1,1,1,1),
            foreground_color=(0,0,0,1)
        )
        form.add_widget(self.descripcion)

        self.fecha = TextInput(
            hint_text="Fecha (YYYY-MM-DD)",
            multiline=False,
            background_color=(1,1,1,1),
            foreground_color=(0,0,0,1)
        )
        form.add_widget(self.fecha)

        self.hora = TextInput(
            hint_text="Hora (HH:MM)",
            multiline=False,
            background_color=(1,1,1,1),
            foreground_color=(0,0,0,1)
        )
        form.add_widget(self.hora)

        boton = Button(
            text="Guardar",
            size_hint=(1, 0.3),
            background_color=(0.2, 0.5, 1, 1)
        )
        boton.bind(on_press=self.guardar)
        form.add_widget(boton)

        self.add_widget(form)

        # ===== LISTA =====
        subtitulo = Label(
            size_hint=(1, 0.08),
            color=(0.2, 0.2, 0.2, 1)
        )
        self.add_widget(subtitulo)

        scroll = ScrollView(size_hint=(1, 0.25))

        self.lista = Label(
            size_hint_y=None,
            markup=True,
            color=(0, 0, 0, 1)
        )
        self.lista.bind(texture_size=self.lista.setter('size'))

        scroll.add_widget(self.lista)
        self.add_widget(scroll)

        # ===== ELIMINAR =====
        eliminar_box = BoxLayout(size_hint=(1, 0.15), spacing=8)

        self.indice_eliminar = TextInput(
            hint_text="Número a eliminar",
            multiline=False,
            background_color=(1,1,1,1),
            foreground_color=(0,0,0,1)
        )
        eliminar_box.add_widget(self.indice_eliminar)

        boton_eliminar = Button(
            text="Eliminar",
            background_color=(1, 0.3, 0.3, 1)
        )
        boton_eliminar.bind(on_press=self.eliminar)
        eliminar_box.add_widget(boton_eliminar)

        self.add_widget(eliminar_box)

        # Mostrar datos
        self.mostrar_recordatorios()

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def mostrar_recordatorios(self):
        recordatorios = cargar_recordatorios()

        texto = "[b]Recordatorios:[/b]\n\n"

        for i, r in enumerate(recordatorios):
            texto += f"[b]{i+1}.[/b] {r['titulo']}\n"
            texto += f"{r['fecha']} {r['hora']}\n\n"

        self.lista.text = texto

    def guardar(self, obj):

        crear_recordatorio(
            self.titulo.text,
            self.descripcion.text,
            self.fecha.text,
            self.hora.text
        )

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

            self.indice_eliminar.text = ""

            self.mostrar_recordatorios()

        except:
            print("Índice inválido")


class MiRecordatorioApp(App):

    def build(self):
        return Pantalla()


MiRecordatorioApp().run()