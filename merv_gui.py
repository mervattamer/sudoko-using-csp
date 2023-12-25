import pygame 
import sys 
import GUI
import suduko_main
import random_fn
import insert_board_gui
pygame.init() 
res = (600,300) 
screen = pygame.display.set_mode(res) 

# white color 
color = (255,255,255) 

# light shade of the button 
color_light = (170,170,170) 

# dark shade of the button 
color_dark = (100,100,100) 

# stores the width/ height of the 
# screen into a variable 
width = screen.get_width() 
height = screen.get_height() 

# defining a font 
smallfont = pygame.font.SysFont('Arial',25) 
text_Random = smallfont.render('Random' , True , color) 
text_input = smallfont.render('Input Board' , True , color) 
text_play = smallfont.render('User Play' , True , color) 
background_image = pygame.image.load('bc_2.jpeg')

while True: 
	
	for ev in pygame.event.get(): 
		
		if ev.type == pygame.QUIT: 
			pygame.quit() 
			
		#checks if a mouse is clicked
		if ev.type == pygame.MOUSEBUTTONDOWN: 
			
			#if the mouse is clicked on random
			if width/2 -100 <= mouse[0] <= width/2 +100 and height/2 <= mouse[1] <= height/2+40: 
				suduko_main.main_gui(random_fn.random_inp()) #replace with random fn
			if width/2 -100 <= mouse[0] <= width/2 -100 +200 and height/2 + 50<= mouse[1] <= height/2+90: 
				insert_board_gui.main() #replace with input board fn
			if width/2 -100 <= mouse[0] <= width/2 -100 +200 and height/2 + 100<= mouse[1] <= height/2+140:
				GUI.main() 
				#pygame.quit() #replace with input board fn
				
	# fills the screen with a color _
	#screen.fill((120,100,170)) 
	
	screen.blit(background_image, (0, 0))
	
	# stores the (x,y) coordinates into 
	# the variable as a tuple 
	mouse = pygame.mouse.get_pos() 
	

##button 1
	# if mouse is hovered on a button it 
	# changes to lighter shade 
	if width/2 -100 <= mouse[0] <= width/2 -100 +200 and height/2 <= mouse[1] <= height/2+40: 
		pygame.draw.rect(screen,color_light,[width/2 - 100,height/2,200,40]) 
	else: 
		pygame.draw.rect(screen,color_dark,[width/2 - 100 ,height/2,200,40]) 
	
	# superimposing the text onto our button 
	screen.blit(text_Random , (width/2 -50 ,height/2)) 
	
##button 2
	if width/2 -100 <= mouse[0] <= width/2 -100 +200 and height/2 + 50<= mouse[1] <= height/2+90: 
		pygame.draw.rect(screen,color_light,[width/2 - 100,height/2 +50,200,40]) 
	else: 
		pygame.draw.rect(screen,color_dark,[width/2 - 100 ,height/2 +50,200,40]) 
	
	# superimposing the text onto our button 
	screen.blit(text_input , (width/2 -50 ,height/2 +50 )) 
	
##button 3
	if width/2 -100 <= mouse[0] <= width/2 -100 +200 and height/2 + 100<= mouse[1] <= height/2+140: 
		pygame.draw.rect(screen,color_light,[width/2 - 100,height/2 +100,200,40]) 
	else: 
		pygame.draw.rect(screen,color_dark,[width/2 - 100 ,height/2 +100,200,40]) 
	
	# superimposing the text onto our button 
	screen.blit(text_play , (width/2 -50 ,height/2 +100 )) 
	
    
	
	# updates the frames of the game 
	pygame.display.update() 
