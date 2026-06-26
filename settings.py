# Pantalla
ANCHO = 800
ALTO = 600
FPS = 60
TITULO = "La Vida da Vueltas: Pollería del Revés"
HUD_ALTO = 70  # franja superior reservada para timer y dinero

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 50, 50)
AMARILLO = (255, 200, 0)
NARANJA = (230, 120, 30)

# Gameplay
TIEMPO_LIMITE = 60
META_DINERO = 60
PRECIO_MINIMO_COBRO = 10
PENALIZACION_FALLO = 10

# Precios de pedidos
PRECIO_CUARTO = 20
PRECIO_MEDIO = 35
PRECIO_ENTERO = 70
PRECIO_MAIZ = 15

# Minijuego Horno
HORNO_VELOCIDAD_INICIAL = 3
HORNO_VENTANA_MS = 150
HORNO_PORCENTAJE_EXITO = 0.6

# Minijuego Corte — dificultad por nivel (longitud secuencia, tiempo límite)
CORTE_TIEMPO_LIMITE = 5        # nivel 1 por defecto
CORTE_LONGITUD_SECUENCIA = 5   # nivel 1 por defecto
CORTE_LONGITUD_POR_NIVEL = {1: 5, 2: 5, 3: 6, 4: 7}   # letras en la secuencia
CORTE_TIEMPO_POR_NIVEL   = {1: 5.0, 2: 4.5, 3: 4.5, 4: 4.0}  # segundos límite

# Minijuego Maíz — dificultad por nivel (velocidad descarga, tiempo límite)
MAIZ_TIEMPO_LIMITE = 4         # nivel 1 por defecto
MAIZ_DESCARGA_POR_NIVEL = {1: 15, 2: 18, 3: 21, 4: 24}  # puntos/s que baja la barra sola
MAIZ_TIEMPO_POR_NIVEL   = {1: 4.0, 2: 3.5, 3: 3.5, 4: 3.0}  # segundos límite

# Sistema de niveles — meta de dinero
NIVEL_METAS = {1: 60, 2: 80, 3: 100, 4: 115, 5: 125}
NIVEL_META_TECHO = 130  # nivel 6+

# Economía de tiempo por nivel (nivel 1 = sin penalizaciones ni bonuses)
TIEMPO_PENALIZACION_POR_NIVEL = {1: 0, 2: 2, 3: 3, 4: 4}   # s restados por fallo
TIEMPO_BONUS_EXITO_POR_NIVEL  = {1: 0, 2: 1, 3: 2, 4: 2}   # s sumados por éxito en minijuego
TIEMPO_BONUS_PEDIDO_POR_NIVEL = {1: 0, 2: 3, 3: 4, 4: 5}   # bonus al completar pedido sin fallos

# Animaciones (Día 3)
ANIM_CLIENTE_DURACION = 2.0   # segundos
ANIM_HORNO_DURACION = 2.5     # segundos
ANIM_RESULTADO_DURACION = 2.0 # segundos

# Rutas de assets (relativas a la raíz del proyecto / main.py)
RUTA_FONDO_RESTAURANTE = "assets/images/fondo_restaurante.png"
RUTA_FONDO_COCINA = "assets/images/fondo_cocina.png"
RUTA_POLLO_COCINERO = "assets/images/pollo_cocinero.png"
RUTA_CLIENTE_FELIZ = "assets/images/cliente_feliz.png"
RUTA_CLIENTE_ENOJADO = "assets/images/cliente_enojado.png"
RUTA_HUMANO_HORNO = "assets/images/humano_horno.png"
RUTA_HORNO_GIRATORIO = "assets/images/horno_giratorio.png"
RUTA_MAIZ = "assets/images/maiz.png"
RUTA_ZONA_IMPACTO = "assets/images/ui/zona_impacto.png"
RUTA_BARRA_PROGRESO = "assets/images/ui/barra_progreso.png"
RUTA_FLECHA_IZQUIERDA = "assets/images/flecha_izquierda.png"
RUTA_FLECHA_ABAJO = "assets/images/flecha_abajo.png"
RUTA_FLECHA_ARRIBA = "assets/images/flecha_arriba.png"
RUTA_FLECHA_DERECHA = "assets/images/flecha_derecha.png"