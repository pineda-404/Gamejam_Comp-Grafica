from entities.pedido import Pedido
from settings import (
    NIVEL_META_TECHO,
    NIVEL_METAS,
    PRECIO_MINIMO_COBRO,
    TIEMPO_LIMITE,
    TIEMPO_BONUS_EXITO_POR_NIVEL,
    TIEMPO_BONUS_PEDIDO_POR_NIVEL,
    TIEMPO_PENALIZACION_POR_NIVEL,
)

PEDIDOS_EN_COLA = 3


class GameManager:
    def __init__(self):
        self.nivel = 1
        self.dinero_acumulado = 0
        self.tiempo_restante = TIEMPO_LIMITE
        self.pedidos_disponibles: list[Pedido] = []
        self.pedido_activo: Pedido | None = None
        self.estado = "inicio"
        self.minijuego_actual = None
        self.indice_minijuego = 0
        self.fase_pedido: str | None = None  # anim_cliente | anim_horno | anim_resultado
        self._ultimo_pedido_exitoso: bool | None = None
        self._fallos_pedido_actual = 0  # para bonus de pedido perfectos
        self._pedido_cancelado = False  # True solo cuando precio cae a 0 (no entregado)
        self._llenar_cola_pedidos()

    # ------------------------------------------------------------------ #
    # Pausa                                                              #
    # ------------------------------------------------------------------ #

    def pausar(self) -> None:
        """Congela el juego guardando el estado actual."""
        if self.estado in ("juego", "minijuego"):
            self._estado_previo = self.estado
            self.estado = "pausa"
    
    def reanudar(self) -> None:
        """Reanuda desde donde se pausó."""
        if self.estado == "pausa" and self._estado_previo:
            self.estado = self._estado_previo
            self._estado_previo = None
    
    def reiniciar_nivel(self) -> None:
        """
        Reinicia el nivel actual manteniendo el nivel,
        pero reiniciando tiempo, dinero y pedidos.
        """
        self.dinero_acumulado = 0
        self.tiempo_restante = TIEMPO_LIMITE

        self.pedidos_disponibles.clear()
        self.pedido_activo = None

        self.minijuego_actual = None
        self.indice_minijuego = 0

        self.fase_pedido = None
        self._ultimo_pedido_exitoso = None
        self._fallos_pedido_actual = 0
        self._pedido_cancelado = False
        self._estado_previo = None

        self.estado = "juego"

        self._llenar_cola_pedidos()


    def salir_al_menu(self) -> None:
        """Regresa al menú principal."""
        self.reiniciar()

    # ------------------------------------------------------------------ #
    # Helpers de dificultad                                                #
    # ------------------------------------------------------------------ #

    def get_meta_dinero(self) -> int:
        """Meta de dinero del nivel actual."""
        return NIVEL_METAS.get(self.nivel, NIVEL_META_TECHO)

    def _get_tabla(self, tabla: dict) -> int | float:
        """Lee una tabla por nivel con saturación en la clave máxima."""
        clave = min(self.nivel, max(tabla.keys()))
        return tabla[clave]

    def _penalizacion_tiempo(self) -> float:
        return self._get_tabla(TIEMPO_PENALIZACION_POR_NIVEL)

    def _bonus_tiempo_exito(self) -> float:
        return self._get_tabla(TIEMPO_BONUS_EXITO_POR_NIVEL)

    def _bonus_tiempo_pedido(self) -> float:
        return self._get_tabla(TIEMPO_BONUS_PEDIDO_POR_NIVEL)

    # ------------------------------------------------------------------ #
    # Ciclo de vida                                                        #
    # ------------------------------------------------------------------ #

    def reiniciar(self) -> None:
        self.nivel = 1
        self.dinero_acumulado = 0
        self.tiempo_restante = TIEMPO_LIMITE
        self.pedidos_disponibles.clear()
        self.pedido_activo = None
        self.estado = "inicio"
        self.minijuego_actual = None
        self.indice_minijuego = 0
        self.fase_pedido = None
        self._ultimo_pedido_exitoso = None
        self._fallos_pedido_actual = 0
        self._pedido_cancelado = False
        self._llenar_cola_pedidos()

    def iniciar_partida(self) -> None:
        self.reiniciar()
        self.estado = "juego"

    def _subir_nivel(self) -> None:
        """Sube el nivel conservando el tiempo restante y reiniciando dinero."""
        self.nivel += 1
        self.dinero_acumulado = 0
        self.tiempo_restante = TIEMPO_LIMITE  # se reinicia el cronómetro
        self.pedido_activo = None
        self.minijuego_actual = None
        self.indice_minijuego = 0
        self.fase_pedido = None
        self._fallos_pedido_actual = 0
        self.pedidos_disponibles.clear()
        self._llenar_cola_pedidos()
        self.estado = "nivel_superado"

    # ------------------------------------------------------------------ #
    # Timer                                                                #
    # ------------------------------------------------------------------ #

    def actualizar_timer(self, dt: float) -> None:
        if self.estado not in ("juego", "minijuego"):
            return

        self.tiempo_restante -= dt

        # Verificar meta de dinero (subir nivel) antes de que el timer llegue a 0
        if self.dinero_acumulado >= self.get_meta_dinero() and self.estado in ("juego",):
            self._subir_nivel()
            return

        if self.tiempo_restante <= 0:
            self.tiempo_restante = 0
            self.estado = "victoria" if self.dinero_acumulado >= self.get_meta_dinero() else "derrota"

    # ------------------------------------------------------------------ #
    # Pedidos                                                              #
    # ------------------------------------------------------------------ #

    def seleccionar_pedido(self, pedido: Pedido) -> bool:
        if self.estado != "juego" or self.pedido_activo is not None:
            return False
        if pedido not in self.pedidos_disponibles:
            return False

        self.pedidos_disponibles.remove(pedido)
        self.pedido_activo = pedido
        self.indice_minijuego = 0
        self.minijuego_actual = None
        self.fase_pedido = "anim_cliente"
        self._fallos_pedido_actual = 0
        self._pedido_cancelado = False
        # Permanece en estado "juego" hasta terminar animaciones
        return True

    def avanzar_fase_pedido(self) -> None:
        """Transición anim_cliente → anim_horno (si aplica) → minijuego."""
        if self.pedido_activo is None:
            self.fase_pedido = None
            return

        if self.fase_pedido == "anim_cliente":
            if self.get_minijuego_actual_id() == "horno":
                self.fase_pedido = "anim_horno"
            else:
                self.fase_pedido = None
                self.estado = "minijuego"
            return

        if self.fase_pedido == "anim_horno":
            self.fase_pedido = None
            self.estado = "minijuego"
            return

    def registrar_resultado_minijuego(self, exito: bool) -> None:
        if self.pedido_activo is None:
            return

        if exito:
            # Bonus de tiempo por éxito en minijuego (nivel 2+)
            bonus = self._bonus_tiempo_exito()
            if bonus > 0:
                self.tiempo_restante = min(self.tiempo_restante + bonus, TIEMPO_LIMITE)
        else:
            self._fallos_pedido_actual += 1
            self.pedido_activo.aplicar_penalizacion()
            # Penalización de tiempo por fallo (nivel 2+)
            penalizacion = self._penalizacion_tiempo()
            if penalizacion > 0:
                self.tiempo_restante = max(0.0, self.tiempo_restante - penalizacion)
            if self.pedido_activo.cancelado:
                self._cancelar_pedido_activo()
                return

        self.indice_minijuego += 1
        if self.indice_minijuego >= len(self.pedido_activo.minijuegos):
            self.cobrar_pedido()

    def cobrar_pedido(self) -> None:
        if self.pedido_activo is None:
            return

        if self.pedido_activo.precio_actual > PRECIO_MINIMO_COBRO:
            self.dinero_acumulado += self.pedido_activo.precio_actual

        # El pedido se entregó, pero el cliente solo queda feliz si no hubo errores.
        # Con fallos pagará menos y saldrá molesto.
        pedido_perfecto = self._fallos_pedido_actual == 0

        # Bonus de tiempo por pedido perfecto (sin fallos, nivel 2+)
        if pedido_perfecto:
            bonus_pedido = self._bonus_tiempo_pedido()
            if bonus_pedido > 0:
                self.tiempo_restante = min(self.tiempo_restante + bonus_pedido, TIEMPO_LIMITE)

        # exito=True  → cliente feliz (cara satisfecha)
        # exito=False → cliente enojado (cara molesta, aunque pagó algo)
        self._mostrar_resultado_pedido(exito=pedido_perfecto)

    def generar_nuevo_pedido(self) -> None:
        self.pedidos_disponibles.append(Pedido.generar_aleatorio())

    def get_minijuego_actual_id(self) -> str | None:
        if self.pedido_activo is None:
            return None
        if self.indice_minijuego >= len(self.pedido_activo.minijuegos):
            return None
        return self.pedido_activo.minijuegos[self.indice_minijuego]

    def _cancelar_pedido_activo(self) -> None:
        self._pedido_cancelado = True
        self._mostrar_resultado_pedido(exito=False)

    def _mostrar_resultado_pedido(self, exito: bool) -> None:
        self._ultimo_pedido_exitoso = exito
        self.pedido_activo = None
        self.indice_minijuego = 0
        self.minijuego_actual = None
        self.estado = "juego"
        self.fase_pedido = "anim_resultado"

    def finalizar_resultado_pedido(self) -> None:
        cancelado = self._pedido_cancelado
        self.fase_pedido = None
        self._ultimo_pedido_exitoso = None
        self._pedido_cancelado = False
        if cancelado:
            # El pedido se perdió: rellenar cola completa (el cliente se fue sin pagar)
            self._llenar_cola_pedidos()
        else:
            # El pedido fue entregado (perfecto o con fallos): generar solo 1 pedido nuevo
            self.generar_nuevo_pedido()

    def _llenar_cola_pedidos(self) -> None:
        while len(self.pedidos_disponibles) < PEDIDOS_EN_COLA:
            self.generar_nuevo_pedido()
