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
from kivy.uix.popup import Popup

from codigo.main import crear_recordatorio, cargar_recordatorios, eliminar_recordatorio


class Pantalla(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=15, spacing=12, **kwargs)

        # ===== FONDO =====
        with self.canvas.before:
            Color(0.94, 0.95, 0.97, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # ===== MENSAJE VISUAL =====
        self.mensaje = Label(text="", size_hint=(1, 0.08))
        self.add_widget(self.mensaje)

        # ===== TITULO =====
        self.add_widget(Label(
            text="MiRecordatorio",
            font_size=26,
            bold=True,
            size_hint=(1, 0.1)
        ))

        # ===== FORMULARIO =====
        form = BoxLayout(orientation="vertical", spacing=8, size_hint=(1, 0.45))

        self.titulo = TextInput(hint_text="Título", multiline=False)
        form.add_widget(self.titulo)

        self.descripcion = TextInput(hint_text="Descripción", multiline=False)
        form.add_widget(self.descripcion)

        # NUEVOS FORMATOS
        self.fecha = TextInput(hint_text="Fecha (DD/MM/YYYY)", multiline=False)
        form.add_widget(self.fecha)

        self.hora = TextInput(hint_text="Hora (Ej: 3:30 pm)", multiline=False)
        form.add_widget(self.hora)

        boton = Button(text="Guardar", size_hint=(1, 0.3), background_color=(0.2, 0.5, 1, 1))
        boton.bind(on_press=self.guardar)
        form.add_widget(boton)

        self.add_widget(form)

        # ===== LISTA =====
        scroll = ScrollView(size_hint=(1, 0.25))

        self.lista = Label(size_hint_y=None, markup=True)
        self.lista.bind(texture_size=self.lista.setter('size'))

        scroll.add_widget(self.lista)
        self.add_widget(scroll)

        # ===== ELIMINAR =====
        eliminar_box = BoxLayout(size_hint=(1, 0.15), spacing=8)

        self.indice_eliminar = TextInput(hint_text="Número a eliminar", multiline=False)
        eliminar_box.add_widget(self.indice_eliminar)

        boton_eliminar = Button(text="Eliminar", background_color=(1, 0.3, 0.3, 1))
        boton_eliminar.bind(on_press=self.confirmar_eliminacion)
        eliminar_box.add_widget(boton_eliminar)

        self.add_widget(eliminar_box)

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

    # ===== MOSTRAR LISTA =====
    def mostrar_recordatorios(self):
        recordatorios = cargar_recordatorios()

        texto = "[b]Recordatorios:[/b]\n\n"

        for i, r in enumerate(recordatorios):
            texto += f"[b]{i+1}.[/b] {r['titulo']}\n"

            if r['descripcion']:
                texto += f"[color=555555] {r['descripcion']}[/color]\n"

            texto += f" {r['fecha']} {r['hora']}\n\n"

        self.lista.text = texto

    # ===== GUARDAR (MEJORADO) =====
    def guardar(self, obj):
        titulo = self.titulo.text.strip()
        descripcion = self.descripcion.text.strip()
        fecha_input = self.fecha.text.strip()
        hora_input = self.hora.text.strip().lower()

        import datetime

        if not titulo or not descripcion or not fecha_input or not hora_input:
            self.mostrar_mensaje("Todos los campos son obligatorios", "error")
            return

        # ===== FECHA DD/MM/YYYY → YYYY-MM-DD =====
        try:
            fecha_obj = datetime.datetime.strptime(fecha_input, "%d/%m/%Y")
            fecha = fecha_obj.strftime("%Y-%m-%d")
        except:
            self.mostrar_mensaje("Fecha inválida", "error")
            return

        # ===== HORA 3:30 pm → 15:30 =====
        try:
            hora_input = hora_input.replace(".", "")

            if "am" in hora_input or "pm" in hora_input:
                hora_obj = datetime.datetime.strptime(hora_input, "%I:%M %p")
            else:
                hora_obj = datetime.datetime.strptime(hora_input, "%H:%M")

            hora = hora_obj.strftime("%H:%M")
        except:
            self.mostrar_mensaje("Formato de hora inválida", "error")
            return

        crear_recordatorio(titulo, descripcion, fecha, hora)

        self.titulo.text = ""
        self.descripcion.text = ""
        self.fecha.text = ""
        self.hora.text = ""

        self.mostrar_recordatorios()
        self.mostrar_mensaje("Recordatorio guardado")

    # ===== CONFIRMAR ELIMINACIÓN =====
    def confirmar_eliminacion(self, obj):
        try:
            indice = int(self.indice_eliminar.text) - 1
        except:
            self.mostrar_mensaje("Índice inválido", "error")
            return

        contenido = BoxLayout(orientation="vertical", spacing=10)
        contenido.add_widget(Label(text="¿Seguro que quieres eliminar este recordatorio?"))

        botones = BoxLayout(spacing=10)

        btn_si = Button(text="Sí", background_color=(1, 0.3, 0.3, 1))
        btn_no = Button(text="No")

        botones.add_widget(btn_si)
        botones.add_widget(btn_no)

        contenido.add_widget(botones)

        popup = Popup(title="Confirmar eliminación", content=contenido, size_hint=(0.8, 0.4))

        btn_si.bind(on_press=lambda x: self.eliminar_confirmado(indice, popup))
        btn_no.bind(on_press=popup.dismiss)

        popup.open()

    def eliminar_confirmado(self, indice, popup):
        eliminar_recordatorio(indice)
        popup.dismiss()

        self.indice_eliminar.text = ""
        self.mostrar_recordatorios()
        self.mostrar_mensaje("Recordatorio eliminado", "eliminar")


class MiRecordatorioApp(App):
    def build(self):
        return Pantalla()


MiRecordatorioApp().run()