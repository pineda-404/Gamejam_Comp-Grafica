import pygame
from settings import AMARILLO, ANCHO, ALTO, BLANCO, NARANJA, NEGRO, TIEMPO_LIMITE


class ScreenNivelSuperado:
    """Pantalla de transición entre niveles.

    Se muestra cuando el jugador alcanza la meta de dinero.
    Pulsar ESPACIO o clic reinicia el timer y sube al siguiente nivel.
    """

    def __init__(self, gm) -> None:
        self.gm = gm
        self.fuente_titulo = pygame.font.SysFont("Arial", 54, bold=True)
        self.fuente_info   = pygame.font.SysFont("Arial", 26)
        self.fuente_sub    = pygame.font.SysFont("Arial", 22)
        self._t = 0.0   # tiempo en esta pantalla (para animación pulsante)

    def manejar_eventos(self, eventos) -> None:
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                self._continuar()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                self._continuar()

    def _continuar(self) -> None:
        self._t = 0.0
        self.gm.estado = "juego"

    def actualizar(self, dt: float) -> None:
        self._t += dt

    def dibujar(self, pantalla: pygame.Surface) -> None:
        pantalla.fill((20, 15, 10))

        # Fondo degradado simulado
        for i in range(ALTO):
            alpha = int(40 * (1 - i / ALTO))
            pygame.draw.line(pantalla, (alpha, int(alpha * 0.6), 0), (0, i), (ANCHO, i))

        # Título pulsante
        escala_pulso = 1.0 + 0.04 * abs(pygame.math.Vector2(1, 0).rotate(self._t * 180).x)
        titulo_txt = f"¡NIVEL {self.gm.nivel - 1} SUPERADO!"
        titulo = self.fuente_titulo.render(titulo_txt, True, AMARILLO)
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 190)))

        # Info del nivel siguiente
        from settings import NIVEL_METAS, NIVEL_META_TECHO
        meta_siguiente = NIVEL_METAS.get(self.gm.nivel, NIVEL_META_TECHO)
        info = self.fuente_info.render(
            f"Próximo objetivo: ${meta_siguiente} en {TIEMPO_LIMITE}s — Nivel {self.gm.nivel}",
            True, BLANCO
        )
        pantalla.blit(info, info.get_rect(center=(ANCHO // 2, 280)))

        # Descripción de dificultad
        from settings import CORTE_LONGITUD_POR_NIVEL, MAIZ_DESCARGA_POR_NIVEL
        n = self.gm.nivel
        clave_c = min(n, max(CORTE_LONGITUD_POR_NIVEL.keys()))
        clave_m = min(n, max(MAIZ_DESCARGA_POR_NIVEL.keys()))
        dif_txt = (f"Corte: {CORTE_LONGITUD_POR_NIVEL[clave_c]} letras  •  "
                   f"Maíz: descarga ×{MAIZ_DESCARGA_POR_NIVEL[clave_m]}/s")
        dif = self.fuente_sub.render(dif_txt, True, NARANJA)
        pantalla.blit(dif, dif.get_rect(center=(ANCHO // 2, 330)))

        # Instrucción pulsante
        if int(self._t * 2) % 2 == 0:
            instruccion = self.fuente_sub.render("Presiona ESPACIO o clic para continuar", True, BLANCO)
            pantalla.blit(instruccion, instruccion.get_rect(center=(ANCHO // 2, 410)))
