import pygame
import requests
import sys
import os


def show_map(ll_spn=None, map_type="map", add_params=None):
    if ll_spn:
        map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?l={map_type}"

    spn = (0.004104999999999137, 0.0020895000000002995)
    if add_params:
        map_request += "&" + add_params
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    spns = f"{spn[0]},{spn[1]}"
    # Инициализируем pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(map_file), (0, 0))
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()
    running = True
    fps = 10
    clock = pygame.time.Clock()
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP and spn[0] < 16.1:
                    spns = f"{spn[0] + 0.001},{spn[1] + 0.001}"
                    spn = spn[0] + 0.001, spn[1] + 0.001

                elif event.key == pygame.K_PAGEDOWN and spn[0] > 0.003:
                    spns = f"{spn[0] - 0.001},{spn[1] - 0.001}"
                    spn = spn[0] - 0.001, spn[1] - 0.001
        ll = "32.012103,59.45837"
        ll_spn = f"ll={ll}&spn={spns}"
        map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}"
        response = requests.get(map_request)
        map_file = "map.png"
        try:
            with open(map_file, "wb") as file:
                file.write(response.content)
        except IOError as ex:
            print("Ошибка записи временного файла:", ex)
            sys.exit(2)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()

    pygame.quit()
    # Удаляем за собой файл с изображением.
    os.remove(map_file)
