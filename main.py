import pygame
import asyncio
import os
from statue import Statue

import map
import enemys
import essentials as es

pygame.init()
screen = pygame.display.set_mode((900, 700), pygame.RESIZABLE)
pygame.display.set_caption("Butterbrot")
clock = pygame.time.Clock()

from player import Player
faces = dict()
for path in os.listdir(str(es.BASE_DIR / "images")):
    faces[path.removesuffix(".png")] = pygame.image.load( str(es.BASE_DIR / "images" / path)).convert_alpha()
player = Player(screen, pygame.Vector2(0, 0),"Normal", faces)

map.init()
map.load_map("level1")
level = 1
l1music = es.load_music("oberweltidk")
l1playing = False
enemys.init()

levelFile = open(es.BASE_DIR / "level1.txt")
data = levelFile.readlines()
tileNames = ["grass_middle_tile", "wall"]
statues = [
    Statue(screen, pygame.Vector2(3 * 256, 2 * 256), faces, "Invisibility"),
    Statue(screen, pygame.Vector2(4 * 256, 0 * 256), faces, "Super Speed")
]
statueSize = faces["Statue_Invisibility"].get_size()
for y in range(len(data)):
    line = data[y].strip().split(" ")
    for x in range(len(line)):
        map.maps["level1"][0].append(map.tile(tileNames[int(line[x])], x * 256, y * 256, 32*8, 32*8, 1))
levelFile.close()

running = True
enemys.spawn(screen, (500, 100), 100, 5, 2, "enemy0")
async def main():
    global running,screen,player
    gameOver = False
    while running:
        if level == 1 and not l1playing:
            l1music.play(-1)
            
        elif level != 1 and l1playing:
            l1music.stop()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            
        keys = pygame.key.get_pressed()
        if gameOver:
            continue
        cameraMove = player.move(keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d]) 
        map.cam.x -= cameraMove[0]
        map.cam.y += cameraMove[1]

        if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
            print("Escape key pressed")

        if level == 1:
            if map.check_exit(player.pos):
                print("Exit erreicht! Level abgeschlossen!")

        screen.fill("blue")
        map.draw()
        player.draw()
        for statue in statues:
            statue.drawPos = (statue.pos[0] + screen.get_width() // 2 + map.cam.x - statueSize[0] // 2, statue.pos[1] + screen.get_height() // 2 + map.cam.y - statueSize[1] // 2)
            statue.draw()
            if statue.checkCollision((player.pos[0] + map.cam.x + screen.get_width() // 2 - 170, player.pos[1] + map.cam.y + screen.get_height() // 2 - faces["Face0_1000_1"].get_height() // 2), (340, faces["".join([str(x) for x in player.faceImage])].get_height())):
                if statue.canSwap:
                    statue.swap(player.swap(statue.face))
                    statue.canSwap = False
            else:
                statue.canSwap = True
        for enemy in enemys.enemys.values():
            enemy.update()
            enemy.draw()
            collision = enemy.checkCollision(player.pos, 500)
            if collision:
                enemy.current = list("enemy0_attack")
                enemy.draw()
                gameOver = True
                es.game_over()

        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
