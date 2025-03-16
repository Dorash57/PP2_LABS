import pygame
pygame.mixer.init()
pygame.init()
running=True
wh = (600 , 600 )
screen=pygame.display.set_mode(wh)
dorash1=pygame.transform.scale(pygame.image.load(r"C:\Users\doras\OneDrive\Рабочий стол\PP2_LABARATORIKA\LABS\LAB7\Photos\dorash1.png"),wh)
dorash2=pygame.transform.scale(pygame.image.load(r"C:\Users\doras\OneDrive\Рабочий стол\PP2_LABARATORIKA\LABS\LAB7\Photos\dorash2.png"),wh)
dorash3=pygame.transform.scale(pygame.image.load(r"C:\Users\doras\OneDrive\Рабочий стол\PP2_LABARATORIKA\LABS\LAB7\Photos\dorash4.png"),wh)
arrP=[dorash1,dorash2,dorash3]
arrM=[
r"C:\Users\doras\OneDrive\Рабочий стол\PP2_LABARATORIKA\LABS\LAB7\songs\MiyaGi - Самурай.mp3",
r"C:\Users\doras\OneDrive\Рабочий стол\PP2_LABARATORIKA\LABS\LAB7\songs\MiyaGi & Эндшпиль - Fire Man.mp3",
r"C:\Users\doras\OneDrive\Рабочий стол\PP2_LABARATORIKA\LABS\LAB7\songs\MiyaGi ft. Эндшпиль - Малиновый рассвет.mp3"
]
index=0
pygame.mixer.music.load(arrM[index])
pygame.mixer.music.play()
paused=False
while running:
    screen.blit(arrP[index], (0, 0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            pygame.quit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_d:
                index=(index+1)%3
                pygame.mixer.music.load(arrM[index])
                pygame.mixer.music.play()
            if event.key == pygame.K_a:
                index = (index - 1) % 3
                pygame.mixer.music.load(arrM[index])
                pygame.mixer.music.play()
            if event.key == pygame.K_SPACE:
                if paused:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
                paused = not paused