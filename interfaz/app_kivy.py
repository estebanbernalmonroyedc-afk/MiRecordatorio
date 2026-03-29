import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup

from codigo.main import crear_recordatorio, cargar_recordatorios, eliminar_recordatorio


class Pantalla(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)

        # ===== FONDO =====
        with self.canvas.before:
            Color(0.94, 0.95, 0.97, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # ===== MENSAJE =====
        self.mensaje = Label(text="", size_hint=(1, None), height=30)
        self.add_widget(self.mensaje)

        # ===== TITULO =====
        titulo = Label(
            text="MiRecordatorio",
            font_size=24,
            bold=True,
            size_hint=(1, None),
            height=50,
            color=(0, 0, 0, 1),
            halign="center",
            valign="middle"
        )
        titulo.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        self.add_widget(titulo)

        # ===== FORMULARIO =====
        form = BoxLayout(orientation="vertical", spacing=5, size_hint=(1, None), height=220)

        self.titulo = TextInput(hint_text="Título", multiline=False)
        form.add_widget(self.titulo)

        self.descripcion = TextInput(hint_text="Descripción", multiline=False)
        form.add_widget(self.descripcion)

        self.fecha = TextInput(hint_text="Fecha (DD/MM/YYYY)", multiline=False)
        form.add_widget(self.fecha)

        self.hora = TextInput(hint_text="Hora (Ej: 3:30 pm o 15:30)", multiline=False)
        form.add_widget(self.hora)

        boton = Button(text="Guardar", size_hint=(1, None), height=40, background_color=(0.2, 0.5, 1, 1))
        boton.bind(on_press=self.guardar)
        form.add_widget(boton)

        self.add_widget(form)

        # ===== LISTA NUEVA (CON BOTONES) =====
        scroll = ScrollView(size_hint=(1, 1))

        self.lista = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.lista.bind(minimum_height=self.lista.setter('height'))

        scroll.add_widget(self.lista)
        self.add_widget(scroll)

        self.mostrar_recordatorios()

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    # ===== MENSAJES =====
    def mostrar_mensaje(self, texto, tipo="ok"):
        if tipo == "error":
            self.mensaje.color = (1, 0, 0, 1)
        elif tipo == "eliminar":
            self.mensaje.color = (1, 0.6, 0, 1)
        else:
            self.mensaje.color = (0, 0.7, 0, 1)

        self.mensaje.text = texto

    # ===== LISTA CON TARJETAS =====
    def mostrar_recordatorios(self):
        self.lista.clear_widgets()

        recordatorios = cargar_recordatorios()

        for i, r in enumerate(recordatorios):

            # TARJETA
            card = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=80,
                padding=10,
                spacing=10
            )

            with card.canvas.before:
                Color(1, 1, 1, 1)
                card.rect = Rectangle(size=card.size, pos=card.pos)
                card.bind(size=lambda inst, val: setattr(card.rect, 'size', val))
                card.bind(pos=lambda inst, val: setattr(card.rect, 'pos', val))

            # TEXTO
            texto = Label(
                text=f"[b]{i+1}. {r['titulo']}[/b]\n{r['descripcion']}\n {r['fecha']} {r['hora']}",
                markup=True,
                size_hint_x=1,
                halign="left",
                valign="middle",
                color=(0, 0, 0, 1)
            )
            texto.bind(
                 size=lambda inst, val: setattr(inst, 'text_size', (val[0], None))
            )

            # BOTÓN ELIMINAR
            btn_eliminar = Button(
                text="eliminar",
                size_hint=(None, 1),
                width=60,
                background_color=(1, 0.3, 0.3, 1)
            )

            btn_eliminar.bind(
                on_press=lambda x, idx=i: self.confirmar_eliminacion_directa(idx)
            )

            card.add_widget(texto)
            card.add_widget(btn_eliminar)

            self.lista.add_widget(card)

    # ===== GUARDAR =====
    def guardar(self, obj):
        titulo = self.titulo.text.strip()
        descripcion = self.descripcion.text.strip()
        fecha_input = self.fecha.text.strip()
        hora_input = self.hora.text.strip().lower()

        import datetime

        if not titulo or not descripcion or not fecha_input or not hora_input:
            self.mostrar_mensaje("Todos los campos son obligatorios", "error")
            return

        try:
            fecha_obj = datetime.datetime.strptime(fecha_input, "%d/%m/%Y")
            fecha = fecha_obj.strftime("%Y-%m-%d")
        except:
            self.mostrar_mensaje("Fecha inválida", "error")
            return

        try:
            hora_input = hora_input.replace(".", "")

            if "am" in hora_input or "pm" in hora_input:
                hora_obj = datetime.datetime.strptime(hora_input, "%I:%M %p")
            else:
                hora_obj = datetime.datetime.strptime(hora_input, "%H:%M")

            hora = hora_obj.strftime("%H:%M")
        except:
            self.mostrar_mensaje("Hora inválida", "error")
            return

        crear_recordatorio(titulo, descripcion, fecha, hora)

        self.titulo.text = ""
        self.descripcion.text = ""
        self.fecha.text = ""
        self.hora.text = ""

        self.mostrar_recordatorios()
        self.mostrar_mensaje("Recordatorio guardado")

    # ===== CONFIRMAR ELIMINACIÓN DIRECTA =====
    def confirmar_eliminacion_directa(self, indice):

        contenido = BoxLayout(orientation="vertical", spacing=10)
        contenido.add_widget(Label(text="¿Eliminar este recordatorio?"))

        botones = BoxLayout(spacing=10)

        btn_si = Button(text="Sí")
        btn_no = Button(text="No")

        botones.add_widget(btn_si)
        botones.add_widget(btn_no)
        contenido.add_widget(botones)

        popup = Popup(title="Confirmación", content=contenido, size_hint=(0.8, 0.4))

        btn_si.bind(on_press=lambda x: self.eliminar_confirmado(indice, popup))
        btn_no.bind(on_press=popup.dismiss)

        popup.open()

    def eliminar_confirmado(self, indice, popup):
        eliminar_recordatorio(indice)
        popup.dismiss()

        self.mostrar_recordatorios()
        self.mostrar_mensaje("Eliminado", "eliminar")


class MiRecordatorioApp(App):
    def build(self):
        return Pantalla()


MiRecordatorioApp().run()