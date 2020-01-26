	# 1 - Import 
import pygame
from pygame.locals import *
import math
from random import randint
	# 2 - Inisialisasi Game
pygame.init()
width, height = 1000, 580
screen = pygame.display.set_mode((width, height))
	# Key 
keys = {
    "top": False, 
    "bottom": False,
}
running = True
Pesawatpos = [140, 240] # Posisi Pesawat
	# Kalo menang
exitcode = 0
EXIT_CODE_GAME_OVER = 0
EXIT_CODE_WIN = 1
score = 0 
health_point = 194 # health poin Planet
countdown_timer = 60000 # Waktu main
Pelurunya = [] # Peluru
enemy_timer = 100 # waktu kemunculan
enemies = [[width, 100]] # Koordinat musuh
	# 3 - Aset Game
	# Images
Pesawat = pygame.image.load("resources/images/p2.png")
Bintang = pygame.image.load("resources/images/back.jpg")
Planet = pygame.image.load("resources/images/planet33.jpg")
Peluru = pygame.image.load("resources/images/back.jpg")
Musuh = pygame.image.load("resources/images/back.jpg")
healthbar = pygame.image.load("resources/images/back.jpg")
health = pygame.image.load("resources/images/back.jpg")
gameover = pygame.image.load("resources/images/back.jpg")
youwin = pygame.image.load("resources/images/back.jpg")
	# Efek Suara

while(running):
        # Clear screen
    screen.fill(0)
        # Player Game
    	# buat Bintang
    for x in range(int(width/Bintang.get_width()+1)):
        for y in range(int(height/Bintang.get_height()+1)):
            screen.blit(Bintang, (x*100, y*100))
		# Menampilkan Planet dalam koordinat
    screen.blit(Planet, (3, 40))
    screen.blit(Planet, (3, 145))
    screen.blit(Planet, (3, 250))
    screen.blit(Planet, (3, 355))
	    # gerakan Pesawat tertuju pada mouse
    mouse_position = pygame.mouse.get_pos()
    angle = math.atan2(mouse_position[1] - (Pesawatpos[1]), mouse_position[0] - (Pesawatpos[0]))
    Pesawat_rotation = pygame.transform.rotate(Pesawat, 360 - angle * 57.29)
    new_Pesawatpos = (Pesawatpos[0] - Pesawat_rotation.get_rect().width / 2, Pesawatpos[1] - Pesawat_rotation.get_rect().height / 2)
    screen.blit(Pesawat_rotation, new_Pesawatpos)
	    # Pelurunya
    for bullet in Pelurunya:
        Peluru_index = 0
        velx=math.cos(bullet[0])*10
        vely=math.sin(bullet[0])*10
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1] < -64 or bullet[1] > width or bullet[2] < -64 or bullet[2] > height:
            Pelurunya.pop(Peluru_index)
        Peluru_index += 1
        	# Menampilkan Peluru
        for projectile in Pelurunya:
            new_Peluru = pygame.transform.rotate(Peluru, 360-projectile[0]*57.29)
            screen.blit(new_Peluru, (projectile[1], projectile[2]))

    # Buat Musuh
    # Waktu saat musuh akan muncul
    enemy_timer -= 1
    if enemy_timer == 0:
        # Buat musuh baru
        enemies.append([width, randint(25, height-32)])
        # reset enemy timer to random time
        enemy_timer = randint(1, 100)

    index = 0
    for enemy in enemies:
        	# Musuh bergerak dengan kecepatan 1.5 pixel ke kiri
        enemy[0] -= 1.5
        	# hapus musuh saat mencapai batas layar sebelah kiri
        if enemy[0] < -64:
            enemies.pop(index)
			# Benturan antara musuh dengan planet
        enemy_rect = pygame.Rect(Musuh.get_rect())
        enemy_rect.top = enemy[1] # ambil titik y (tinggi)
        enemy_rect.left = enemy[0] # ambil titik x (lebar)
        # benturan musuh dengan planet
        if enemy_rect.left < 64:
            enemies.pop(index)
            health_point -= randint(5,20)
            Tertembak.play()
            print("Awas! Musuh datang!")
        	# Benturan musuh dengan pelurunya
        index_Peluru = 0
        for bullet in Pelurunya:
            bullet_rect = pygame.Rect(Peluru.get_rect())
            bullet_rect.left = bullet[1]
            bullet_rect.top = bullet[2]
            	# benturan peluru dengan musuh
            if enemy_rect.colliderect(bullet_rect):
                score += 1
                enemies.pop(index)
                Pelurunya.pop(index_Peluru)
                MusuhMenyerang.play()
                print("Wuahahaha! Mati kau!!")
                print("Score: {}".format(score))
            index_Peluru += 1
        index += 1
	    # Menampilkan musuh
    for enemy in enemies:
        screen.blit(Musuh, enemy)
	
	    # Menampilkan health bar
    screen.blit(healthbar, (5,5))
    for hp in range(health_point):
        screen.blit(health, (hp+8, 8))
	    # Menampilkan timer
    font = pygame.font.Font(None, 24)
    minutes = int((countdown_timer-pygame.time.get_ticks())/60000) # 60000 itu sama dengan 60 detik
    seconds = int((countdown_timer-pygame.time.get_ticks())/1000%60)
    time_text = "{:02}:{:02}".format(minutes, seconds)
    clock = font.render(time_text, True, (255,255,255))
    textRect = clock.get_rect()
    textRect.topright = [635, 5]
    screen.blit(clock, textRect)    
    	# memperbarui screen
    pygame.display.flip()
	    # Perulangan
    for event in pygame.event.get():
        # tombol exit di klik
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
            # Menembak
        if event.type == pygame.MOUSEBUTTONDOWN:
            Pelurunya.append([angle, new_Pesawatpos[0]+32, new_Pesawatpos[1]+32])
            SuaraPeluru.play()
            # tombol untuk menggerakkan pesawat
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys["top"] = True
            elif event.key == K_s:
                keys["bottom"] = True
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys["top"] = False
            elif event.key == K_s:
                keys["bottom"] = False
    	# Akhir Perulangan
    	# Gerakan pesawat
    if keys["top"]:
        Pesawatpos[1] -= 5 # kurangi nilai y
    elif keys["bottom"]:
        Pesawatpos[1] += 5 # tambah nilai y
        # Menang atau kalah
    if pygame.time.get_ticks() > countdown_timer:
        running = False
        exitcode = EXIT_CODE_WIN
    if health_point <= 0:
        running = False
        exitcode = EXIT_CODE_GAME_OVER
# - End of Game Loop

	# 5 - Tampilan menang dan kalah
if exitcode == EXIT_CODE_GAME_OVER:
    screen.blit(gameover, (0, 0))
else:
    screen.blit(youwin, (0, 0))
	# Tampilkan score
text = font.render("Score: {}".format(score), True, (255, 255, 255))
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery + 24
screen.blit(text, textRect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()