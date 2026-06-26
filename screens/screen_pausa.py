"""Overlay de pausa — se activa con ESC durante \"juego\" o \"minijuego\"."""
import pygame

from settings import ALTO, ANCHO, BLANCO, NARANJA, NEGRO


_VERDE = (60, 200, 80)
_ROJO_BTN = (200, 60, 60)
_GRIS = (160, 160, 160)
_BTN_ALTO = 48
_BTN_ANCHO = 240


class _Boton:
    def __init__(self, texto: str, cy: int, color_base):
        self.texto = texto
        self.rect = pygame.Rect(0, 0, _BTN_ANCHO, _BTN_ALTO)
        self.rect.center = (ANCHO // 2, cy)
        self.color_base = color_base
        self._fuente = pygame.font.SysFont("Arial", 22, bold=True)
        self._hover = False

    def dibujar(self, pantalla: pygame.Surface) -> None:
        color = tuple(min(255, c + 40) for c in self.color_base) if self._hover else self.color_base
        pygame.draw.rect(pantalla, color, self.rect, border_radius=10)
        pygame.draw.rect(pantalla, BLANCO, self.rect, width=2, border_radius=10)
        label = self._fuente.render(self.texto, True, BLANCO)
        pantalla.blit(label, label.get_rect(center=self.rect.center))

    def actualizar_hover(self, pos) -> None:
        self._hover = self.rect.collidepoint(pos)

    def fue_presionado(self, eventos) -> bool:
        for ev in eventos:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self.rect.collidepoint(ev.pos):
                    return True
        return False


class ScreenPausa:
    """
    Overlay semitransparente de pausa.
    No es una pantalla completa independiente; se renderiza ENCIMA de la
    pantalla de juego que la invocó (ScreenJuego llama a su dibujar primero,
    luego ScreenPausa dibuja el overlay).
    """

    def __init__(self, gm):
        self.gm = gm
        self.fuente_titulo = pygame.font.SysFont("Arial", 42, bold=True)
        self._btn_continuar = _Boton("▶  Continuar", 330, (50, 130, 210))
        self._btn_salir = _Boton("✕  Salir al menú", 395, _ROJO_BTN)
        self._botones = [self._btn_continuar, self._btn_salir]

    # ------------------------------------------------------------------
    def manejar_eventos(self, eventos) -> None:
        pos = pygame.mouse.get_pos()
        for btn in self._botones:
            btn.actualizar_hover(pos)

        # ESC es manejado exclusivamente en main.py como toggle para evitar
        # que el mismo evento pause Y reanude en el mismo frame.
        if self._btn_continuar.fue_presionado(eventos):
            self.gm.reanudar()
        elif self._btn_salir.fue_presionado(eventos):
            self.gm.salir_al_menu()

    def actualizar(self, dt) -> None:
        pass  # El tiempo no avanza mientras está pausado

    def dibujar(self, pantalla: pygame.Surface) -> None:
        # Oscurecer toda la pantalla con un overlay
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        pantalla.blit(overlay, (0, 0))

        # Panel central
        panel_rect = pygame.Rect(0, 0, 320, 220)
        panel_rect.center = (ANCHO // 2, 365)
        panel_surf = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        panel_surf.fill((20, 20, 30, 200))
        pygame.draw.rect(panel_surf, NARANJA, panel_surf.get_rect(), width=2, border_radius=14)
        pantalla.blit(panel_surf, panel_rect.topleft)

        # Título "PAUSA"
        titulo = self.fuente_titulo.render("⏸  PAUSA", True, NARANJA)
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 248)))

        # Línea separadora
        pygame.draw.line(pantalla, NARANJA, (ANCHO // 2 - 120, 272), (ANCHO // 2 + 120, 272), 1)

        # Botones
        for btn in self._botones:
            btn.dibujar(pantalla)
