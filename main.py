from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.clock import Clock
import math
import colorsys

class HeartWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num_lines = 200          # nombre de traits
        self.scale = 20
        self.current_index = 0
        self.points_cache = []        # stocke les coordonnées des points de la courbe

        # Pré‑calcule tous les points du cœur
        for i in range(self.num_lines + 1):
            t = i * 2 * math.pi / self.num_lines
            x = 16 * (math.sin(t) ** 3)
            y = (13 * math.cos(t)
                 - 5 * math.cos(2*t)
                 - 2 * math.cos(3*t)
                 - math.cos(4*t))
            self.points_cache.append((x, y))

        # Centre de l’écran (sera mis à jour quand la taille est connue)
        self.center_x = 0
        self.center_y = 0

        # Lance l’animation (appel toutes les 0.02 secondes)
        Clock.schedule_interval(self.add_line, 0.02)

    def on_size(self, *args):
        # Récupère le centre du widget une fois la fenêtre créée
        self.center_x = self.width / 2
        self.center_y = self.height / 2

    def add_line(self, dt):
        if self.current_index >= len(self.points_cache):
            return False  # arrête l'horloge quand tout est tracé

        x, y = self.points_cache[self.current_index]

        # Conversion en coordonnées écran (le centre est au milieu)
        start_x = self.center_x
        start_y = self.center_y
        end_x = self.center_x + x * self.scale
        end_y = self.center_y + y * self.scale

        # Couleur arc‑en‑ciel basée sur l'index
        t = self.current_index * 2 * math.pi / self.num_lines
        hue = t / (2 * math.pi)
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        # Kivy attend des composantes entre 0 et 1
        color = (r, g, b)

        with self.canvas:
            Color(*color)
            Line(points=[start_x, start_y, end_x, end_y], width=2)

        self.current_index += 1

class HeartApp(App):
    def build(self):
        return HeartWidget()

if __name__ == '__main__':
    HeartApp().run()