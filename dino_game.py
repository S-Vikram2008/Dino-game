#----- Importing necessary modules
import pyray as pr
import random

#----- Initialising some useful variables---------
velocity=0
screen_height=750
screen_width=750
ground=screen_height//2
can_jump=True  # This is used to get control that the dino can jump from ground and two consecutive jumps one in ground and another in air is not possible 
gravity=0.6
score=0
dino_x=20
dino_y=ground

#----- CREATING A LIST TO STORE OBSTACLES DIMENSIONS ----------
obstacles=[{'x':720,'size':random.choice([10,20]),'passed':False}]

#------- INITIALISING A WINDOW WITH WIDTH=screen_width AND HEIGHT=screen_height and title "DINO GAME "------------
pr.init_window(screen_width,screen_height,"Dino Game")

#------ SETTING A TARGET FRAMES PER SECOND TO MAKE SURE THE GAME LOOP EXECUTES 50 TIMES PER SECOND ----------- 
pr.set_target_fps(50)


#-------- LOADING ALL IMAGES AND RESIZING IT AND CONVERTING INTO A TEXTURE -----------
dino_img = pr.load_image("DinoRun1.png")
pr.image_resize(dino_img, 50, 50)
dino = pr.load_texture_from_image(dino_img)

small_obstacle_img = pr.load_image("SmallCactus1.png")
pr.image_resize(small_obstacle_img, 50, 50)
small_obstacle = pr.load_texture_from_image(small_obstacle_img)

big_obstacle_img = pr.load_image("LargeCactus1.png")
pr.image_resize(big_obstacle_img, 50, 50)
big_obstacle = pr.load_texture_from_image(big_obstacle_img)

# --------- FINALLY FREEING ALL THE RESOURCES USING UNLOAD_IMAGE() ------
pr.unload_image(dino_img)
pr.unload_image(small_obstacle_img)
pr.unload_image(big_obstacle_img)


#------ FUNCTION WHICH GETS EXECUTED WHEN DINO CRASHES WITH THE OBSTACLE -----------
def game_over(score):
    
    while (not pr.window_should_close()):
        if pr.is_key_pressed(pr.KEY_R):
           return
        pr.begin_drawing()
        pr.clear_background(pr.WHITE)
        pr.draw_text("Game over ...",280,305,30,pr.BLACK)
        pr.draw_text("Score : {}".format(score),300,335,25,pr.BLACK)
        pr.draw_text("PRESS R TO RESTART ",280,650,25,pr.BLACK)
        pr.draw_text("PRESS ESC TO QUIT ",280,700,25,pr.BLACK)

        pr.end_drawing()

    
        
# --------- MAIN GAME FUNCTION --------------       
def game():
    global velocity,dino_y,dino_x
    score=0
    can_jump = True
    
    obstacles = [
        {
        'x':720,
        'size':random.choice([10,20]),
        'passed':False
        }
        ]
    
    while (not pr.window_should_close()):

        # If Space Key is pressed and if dino is in ground then it is allowed to jump.
        if pr.is_key_pressed(pr.KEY_SPACE) and can_jump:
            velocity=-12
            can_jump=False
            
        velocity+=gravity
        dino_y+=velocity

        # WHILE RETURNING BACK TO GROUND IF DINO'S 'y' coordinates becomes larger than ground we make the dino's y coordinates equal to groun 
        if dino_y>=ground:
            dino_y=ground
            velocity=0
            can_jump=True
            
        pr.begin_drawing()
        pr.clear_background(pr.WHITE)

        # Drawing a line to indicate it as ground where the dino runs .
        pr.draw_line(0,ground+50,750,ground+50,pr.BLACK)
        pr.draw_texture(dino,dino_x,int(dino_y),pr.WHITE)

        for i in obstacles:
            if i['size']==10:
                pr.draw_texture(small_obstacle,i['x'],ground,pr.WHITE)
            else:
                pr.draw_texture(big_obstacle,i['x'],ground,pr.WHITE)

            i['x']-=10

        # If the obstacle's x coordinate is less than -10 , it means the obstacle has already left the window screen and not yet visible to the user .Hence we remove them from obstacle's list 
        for i in obstacles[:]:
            if i['x']<-10:
                obstacles.remove(i)
        # When the last obstacle has moved sufficiently left, create another obstacle so the game continues smoothly.
        if obstacles[-1]['x']<200:
            obstacles.append({'x':720,'size':random.choice([10,20]),'passed':False})
            
        # Creating a dino rectangle to simulate collision with obstacle's rectangle 
        dino_rec = pr.Rectangle(dino_x, dino_y, 50, 50)

        # For calculating score , if obstacle has passed the dino's (dino_x,dino_y) we increment the score by 1and change that obstacle 's passed value as True
        for obstacle in obstacles:
            if not obstacle['passed']and obstacle['x']<dino_x:
                score+=1
                obstacle['passed']=True

        # Checking for collision with dino_rec and obstacle_rec. If they both collides , we call game_over(score) function .      
        for obstacle in obstacles:
            obstacle_rec = pr.Rectangle(obstacle['x'], ground, 50, 50)
            if pr.check_collision_recs(dino_rec,obstacle_rec):
                game_over(score)
                return score
        # Finally on each frame we draw text Score to show the score achieved by the user .
        pr.draw_text("Score : {}".format(score),30,680,24,pr.BLACK)
        
        pr.end_drawing()
        
    return score


while not pr.window_should_close():
    score = game()
    game_over(score)

# Finally when the game loop is over , we unload all textures to free up memory 
pr.unload_texture(dino)
pr.unload_texture(small_obstacle)
pr.unload_texture(big_obstacle)

#---- Closing the window -------------
pr.close_window()
        
