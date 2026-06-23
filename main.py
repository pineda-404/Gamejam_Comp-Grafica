import pygame

from settings import ALTO, ANCHO, FPS, NEGRO, TITULO


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption(TITULO)
    clock = pygame.time.Clock()

    corriendo = True
    while corriendo:
        dt = clock.tick(FPS) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        pantalla.fill(NEGRO)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
