# You can place the script of your game in this file.
init python:

    import math
    
    warnbeatrice = False
    
    class Cursor(renpy.Displayable):
        def __init__(self, img):
            super(Cursor, self).__init__()
            
            # This image should be twice the width and twice the height
            # of the screen.
            self.child = Image(img)

            # (-1, -1) is the way the event system represents
            # "outside the game window".
            self.pos = (-1, -1)

        def render(self, width, height, st, at):
            render = renpy.Render(config.screen_width, config.screen_height)
            
            if self.pos == (-1, -1):
                # If we don't know where the cursor is, render pure black.
                render.canvas().rect("#000", (0, 0, config.screen_width, config.screen_height))
                return render

            # Render the flashlight image.
            child_render = renpy.render(self.child, width, height, st, at)

            # Draw the image centered on the cursor.
            flashlight_width, flashlight_height = child_render.get_size()
            x, y = self.pos
            x -= flashlight_width / 2
            y -= flashlight_height / 2
            render.blit(child_render, (x, y))
            return render

        def event(self, ev, x, y, st):
            # Re-render if the position changed.
            if self.pos != (x, y):
                renpy.redraw(self, 0)

            # Update stored position
            self.pos = (x, y)

        def visit(self):
            return [ self.child ]
        

    class Appearing(renpy.Displayable):

        def __init__(self, child, pos, opaque_distance, transparent_distance, **kwargs):

            # Pass additional properties on to the renpy.Displayable
            # constructor.
            super(Appearing, self).__init__(**kwargs)

            # The child.
            self.child = renpy.displayable(child)

            # The distance at which the child will become fully opaque, and
            # where it will become fully transparent. The former must be less
            # than the latter.
            self.opaque_distance = opaque_distance
            self.transparent_distance = transparent_distance

            # The alpha channel of the child.
            self.alpha = 0.0

            # The width and height of us, and our child.
            self.width = 0
            self.height = 0
            
            self.pos = pos
            
            #has been looked at
            self.viewed = False

        def render(self, width, height, st, at):

            # Create a transform, that can adjust the alpha channel of the
            # child.
            t = Transform(child=self.child, alpha=self.alpha)

            # Create a render from the child.
            child_render = renpy.render(t, width, height, st, at)

            # Get the size of the child.
            self.width, self.height = child_render.get_size()

            # Create the render we will return.
            render = renpy.Render(self.width, self.height)

            # Blit (draw) the child's render to our render.
            rcenter = (0, 0)
            render.blit(child_render, rcenter)
            
            # if self.viewed :

            # Return the render.
            return render

        def event(self, ev, x, y, st):

            # Compute the distance between the center of this displayable and
            # the mouse pointer. The mouse pointer is supplied in x and y,
            # relative to the upper-left corner of the displayable.
            px,py = self.pos
            distance = math.hypot(x-px, y-py)

            # Base on the distance, figure out an alpha.
            if distance <= self.opaque_distance:
                alpha = 1.0
                self.viewed = True
            elif distance >= self.transparent_distance:
                alpha = 0.0
            else:
                alpha = 1.0 - 1.0 * (distance - self.opaque_distance) / (self.transparent_distance - self.opaque_distance)

            # If the alpha has changed, trigger a redraw event.
            if alpha != self.alpha:
                self.alpha = alpha
                renpy.redraw(self, 0)

            # Pass the event to our child.
            return self.child.event(ev, x, y, st)
            
        def getViewed(self):
            return self.viewed

    def visit(self):
        return [ self.child ]
    
    class Flashlight(renpy.Displayable):
        def __init__(self):
            super(Flashlight, self).__init__()
            
            # This image should be twice the width and twice the height
            # of the screen.
            self.child = Image("images/flashlight.png")

            # (-1, -1) is the way the event system represents
            # "outside the game window".
            self.pos = (-1, -1)

        def render(self, width, height, st, at):
            render = renpy.Render(config.screen_width, config.screen_height)
            
            if self.pos == (-1, -1):
                # If we don't know where the cursor is, render pure black.
                render.canvas().rect("#000", (0, 0, config.screen_width, config.screen_height))
                return render

            # Render the flashlight image.
            child_render = renpy.render(self.child, width, height, st, at)

            # Draw the image centered on the cursor.
            flashlight_width, flashlight_height = child_render.get_size()
            x, y = self.pos
            x -= flashlight_width / 2
            y -= flashlight_height / 2
            render.blit(child_render, (x, y))
            return render

        def event(self, ev, x, y, st):
            # Re-render if the position changed.
            if self.pos != (x, y):
                renpy.redraw(self, 0)

            # Update stored position
            self.pos = (x, y)

        def visit(self):
            return [ self.child ]
            
    class Icon (renpy.Displayable):
        def __init__(self, img, xpos, ypos):
            super(Icon, self).__init__()
            self.child = Image(img)

            # (-1, -1) is the way the event system represents
            # "outside the game window".
            self.pos = (xpos, ypos)

        def render(self, width, height, st, at):
            render = renpy.Render(config.screen_width, config.screen_height)
            
            if self.pos == (-1, -1):
                # If we don't know where the cursor is, render pure black.
                render.canvas().rect("#000", (0, 0, config.screen_width, config.screen_height))
                return render

            # Render the flashlight image.
            child_render = renpy.render(self.child, width, height, st, at)

            # Draw the image in the top right hand corner
            x, y = self.pos
            render.blit(child_render, (x, y))
            return render
            
            

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"
image bg policeLobby = "images/Policelobby_1.png"
image bg policeInterrogationRoom = "images/PoliceInterrogation_1.png"
image bg party = "images/Ballroom_l.png"
image bg policeCaptainsOffice = "images/captainsOffice.png"
image bg policeInterrogationRoomSpill = "images/SpiltTea.png"
image bg parlor = "images/Parlor_02.png"
image bg office = "images/haroldoffice.png"
image bg bedroom = "images/bedroom.png"
image bg cutscene1 = "images/alley_cutscene/Beatrice_and_Con_01.png"
image bg cutscene2 = "images/alley_cutscene/Angelica_Face_Off_02.png"
image bg cutscene3 = "images/alley_cutscene/Go_Towards_03.png"
image bg cutscene4 = "images/alley_cutscene/Fight_04.png"
image bg cutscene5 = "images/alley_cutscene/Realize_05.png"
image bg cutscene6 = "images/alley_cutscene/Leave_Beatrice_06.png"
image bg parliamentoffice = "images/OfficeP_01.png"
image bg parliamenthallway = "images/ParliamentHall_01.png"
image bg alley = "images/Alleyway_01.png"
image bg angelicacipher = "images/AngelicaCipher.png"
image bg angelicadress = "images/AngelicaDress.png"
image bg tryagain = "images/GameOver_Restart.png"
image bg youdied = "images/GameOver_Death.png"
image bg buckingham = "images/BuckinghamPalace_01.png"
image bg chapter1 = "images/Transitions/Chapter1.png"
image bg chapter2 = "images/Transitions/Chapter2.png"
image bg chapter3 = "images/Transitions/Chapter3.png"
image bg chapter4 = "images/Transitions/Chapter4.png"
image bg chapter5 = "images/Transitions/Chapter5.png"
image bg chapter6 = "images/Transitions/Chapter6.png"
image bg beatriceandshady = "images/beatriceandshady.png"


#image angelica smile ".png"
image arthur normal = "images/arthursingle.png"
#image harold normal ".png"
image policebaton = "images/baton.png"
image notedeciphered = "images/SearchItems/notedeciphered.png"
image noteundeciphered = "images/SearchItems/noteunciphered.png"

#angelica's corner image stuff
image angelica normal hidden = Null()
image angelica angry hidden = Null()

# Declare characters used by this game.
#define angelica = Character('Angelica Hall', color="#c8ffc8",
#                            window_left_padding=300,
#                            show_side_image=Image("images/angelica/Angelica_Corner_Idle.png",
#                            xalign=0.0, yalign=1.0))
define angelica = Character('Angelica Hall', color="#c8ffc8",
                            window_left_padding=300,
                            show_side_image=ShowingSwitch("angelica normal", "images/angelica/Angelica_Corner_Idle.png",
                                                          "angelica angry", "images/angelica/Angelica_Corner_Idle2.png",
                                                          None, Null(),
                            xalign=0.0, yalign=1.0))
define ar = Character('Arthur Charleston', image="arthur", window_left_padding=300,
                            show_side_image=ShowingSwitch("angelica normal", "images/angelica/Angelica_Corner_Idle.png",
                                                          "angelica angry", "images/angelica/Angelica_Corner_Idle2.png",
                                                          None, Null(),
                            xalign=0.0, yalign=1.0))
define harold = Character('Harold Fredrickson', color="#a7ffc8", window_left_padding=300,
                            show_side_image=ShowingSwitch("angelica normal", "images/angelica/Angelica_Corner_Idle.png",
                                                          "angelica angry", "images/angelica/Angelica_Corner_Idle2.png",
                                                          None, Null(),
                            xalign=0.0, yalign=1.0))
define countess = Character('Countess', color="#a7ffc8", window_left_padding=300,
                            show_side_image=ShowingSwitch("angelica normal", "images/angelica/Angelica_Corner_Idle.png",
                                                          "angelica angry", "images/angelica/Angelica_Corner_Idle2.png",
                                                          None, Null(),
                            xalign=0.0, yalign=1.0))
define beat = Character('Beatrice Fredrickson', color="#a7ffc8", window_left_padding=300,
                            show_side_image=ShowingSwitch("angelica normal", "images/angelica/Angelica_Corner_Idle.png",
                                                          "angelica angry", "images/angelica/Angelica_Corner_Idle2.png",
                                                          None, Null(),
                            xalign=0.0, yalign=1.0))
define shady = Character('Shady Man', color="#a7ffc8", window_left_padding=300,
                            show_side_image=ShowingSwitch("angelica normal", "images/angelica/Angelica_Corner_Idle.png",
                                                          "angelica angry", "images/angelica/Angelica_Corner_Idle2.png",
                                                          None, Null(),
                            xalign=0.0, yalign=1.0))
define assistant = Character('Assistant', color="#a7ffc8", window_left_padding=300,
                            show_side_image=ShowingSwitch("angelica normal", "images/angelica/Angelica_Corner_Idle.png",
                                                          "angelica angry", "images/angelica/Angelica_Corner_Idle2.png",
                                                          None, Null(),
                            xalign=0.0, yalign=1.0))
define guard = Character ('Palace Guard', color = "#a7ffc8", window_left_padding=300,
                            show_side_image=ShowingSwitch("angelica normal", "images/angelica/Angelica_Corner_Idle.png",
                                                          "angelica angry", "images/angelica/Angelica_Corner_Idle2.png",
                                                          None, Null(),
                            xalign=0.0, yalign=1.0))
define queen = Character ('HRM Queen Victoria', color = "#a7ffc8", window_left_padding=300,
                            show_side_image=ShowingSwitch("angelica normal", "images/angelica/Angelica_Corner_Idle.png",
                                                          "angelica angry", "images/angelica/Angelica_Corner_Idle2.png",
                                                          None, Null(),
                            xalign=0.0, yalign=1.0))

#stop music
#play sound "effect.ogg"

init:
    image arthur chinanimation = Animation("images/Arthur_Idle_Edit/Arthur_Idle0001_Filter.png", .08,
                                            "images/Arthur_Idle_Edit/Arthur_Idle0002_Filter.png", .08,
                                            "images/Arthur_Idle_Edit/Arthur_Idle0003_Filter.png", .08,
                                            "images/Arthur_Idle_Edit/Arthur_Idle0004_Filter.png", .08,
                                            "images/Arthur_Idle_Edit/Arthur_Idle0005_Filter.png", .08,
                                            "images/Arthur_Idle_Edit/Arthur_Idle0006_Filter.png", .08,
                                            "images/Arthur_Idle_Edit/Arthur_Idle0007_Filter.png", .08,
                                            "images/Arthur_Idle_Edit/Arthur_Idle0008_Filter.png", .08,
                                            "images/Arthur_Idle_Edit/Arthur_Idle0009_Filter.png", .08,
                                            "images/Arthur_Idle_Edit/Arthur_Idle0010_Filter.png", .08,
                                            "images/Arthur_Idle_Edit/Arthur_Idle0011_Filter.png", .08,
                                            "images/Arthur_Idle_Edit/Arthur_Idle0012_Filter.png", .08)
    image harold hanimation = Animation("images/harold/Harold1.png", .16,
                                        "images/harold/Harold2.png", .16,
                                        "images/harold/Harold3.png", .16,
                                        "images/harold/Harold4.png", .16,
                                        "images/harold/Harold5.png", .16,
                                        "images/harold/Harold6.png", .16,)
    image beat banimation = Animation("images/beatrice/Beatrice_Sad0001_Filter.png", .16,
                                          "images/beatrice/Beatrice_Sad0002_Filter.png", .16,
                                          "images/beatrice/Beatrice_Sad0003_Filter.png", .16,
                                          "images/beatrice/Beatrice_Sad0004_Filter.png", .16,
                                          "images/beatrice/Beatrice_Sad0005_Filter.png", .16,
                                          "images/beatrice/Beatrice_Sad0006_Filter.png", .16)
    image beat cryanimation = Animation("images/beatricecry/Beatrice_Cry0001_Filter.png", .16,
                                          "images/beatricecry/Beatrice_Cry0002_Filter.png", .16,
                                          "images/beatricecry/Beatrice_Cry0003_Filter.png", .16,
                                          "images/beatricecry/Beatrice_Cry0004_Filter.png", .16,
                                          "images/beatricecry/Beatrice_Cry0005_Filter.png", .16,
                                          "images/beatricecry/Beatrice_Cry0006_Filter.png", .16)
    image countess countanimation = Animation("images/Countess_Indifferent/Countess_Indifferent0001.png", .16,
                                              "images/Countess_Indifferent/Countess_Indifferent0002.png", .16,
                                              "images/Countess_Indifferent/Countess_Indifferent0003.png", .16,
                                              "images/Countess_Indifferent/Countess_Indifferent0004.png", .16,
                                              "images/Countess_Indifferent/Countess_Indifferent0005.png", .16,
                                              "images/Countess_Indifferent/Countess_Indifferent0006.png", .16,)
    image shady shadimation = Animation("images/shady/ShadyMan_Drunk10001_Filter.png", .16,
                                        "images/shady/ShadyMan_Drunk10002_Filter.png", .16,
                                        "images/shady/ShadyMan_Drunk10003_Filter.png", .16,
                                        "images/shady/ShadyMan_Drunk10004_Filter.png", .16,
                                        "images/shady/ShadyMan_Drunk10005_Filter.png", .16,
                                        "images/shady/ShadyMan_Drunk10006_Filter.png", .16,)
    image assistant asanimation = Animation ("images/assistant/Parliament_Assistant_Neutral0001.png", .16,
                                             "images/assistant/Parliament_Assistant_Neutral0002.png", .16,
                                             "images/assistant/Parliament_Assistant_Neutral0003.png", .16,
                                             "images/assistant/Parliament_Assistant_Neutral0004.png", .16,
                                             "images/assistant/Parliament_Assistant_Neutral0005.png", .16,
                                             "images/assistant/Parliament_Assistant_Neutral0006.png", .16,)
    image victoria victoranimation = Animation ("images/Queen_Concerned/Queen_Concerned0001_Filter.png", .16,
                                                "images/Queen_Concerned/Queen_Concerned0002_Filter.png", .16,
                                                "images/Queen_Concerned/Queen_Concerned0003_Filter.png", .16,
                                                "images/Queen_Concerned/Queen_Concerned0004_Filter.png", .16,
                                                "images/Queen_Concerned/Queen_Concerned0005_Filter.png", .16,
                                                "images/Queen_Concerned/Queen_Concerned0006_Filter.png", .16,)
    
    image guard guardimation = Animation ("images/Guard_Neutral/Guard_Neutral0001_Filter.png", .16,
                                        "images/Guard_Neutral/Guard_Neutral0002_Filter.png", .16,
                                        "images/Guard_Neutral/Guard_Neutral0003_Filter.png", .16,
                                        "images/Guard_Neutral/Guard_Neutral0004_Filter.png", .16,
                                        "images/Guard_Neutral/Guard_Neutral0005_Filter.png", .16,
                                        "images/Guard_Neutral/Guard_Neutral0006_Filter.png", .16,)

screen flashlight_demo:
    textbutton "continue" xpos 300 ypos 300 action Return()
    add Flashlight()
    
# The game starts here.
label start:    
    $ a = [Appearing("images/police_news.png", (960,700), 40, 100)]
    $ baton = [Appearing("images/baton2.png", (300,700), 40, 100)]
    $ glasses = [Appearing("images/SearchItems/glasses.png", (620,570), 40, 100)]
    $ blueprint = [Appearing("images/SearchItems/blueprint.png", (150,1030), 100, 500)]
    $ cipher = [Appearing("images/SearchItems/cipher.png", (1450,490), 40, 100)]
    $ cryphoto = [Appearing("images/SearchItems/cryphoto.png", (1830,400), 40, 100)]
    $ jewelrybox = [Appearing("images/SearchItems/jewelrybox.png", (1370,670), 40, 100)]
    $ letters = [Appearing("images/SearchItems/letters.png", (390,600), 40, 100)]
    $ mirror = [Appearing("images/SearchItems/mirror.png", (1050,700), 40, 100)]
    $ sword = [Appearing("images/SearchItems/sword.png", (480,340), 40, 100)]
    $ book = [Appearing("images/SearchItems/book.png", (1160,740), 40, 100)]
    $ note2 = [Appearing("images/SearchItems/note2.png", (1880,740), 40, 100)]
    $ typewriter = [Appearing("images/SearchItems/typewriter.png", (1525,540), 40, 100)]
    $ icon = [Icon("images/Notes_UI.png", 1719, 0) ]
    
    screen newspaper:
        add a[0]
        add Cursor("images/magnifyingglass_UI.png")
        #add Flashlight()
    screen bedroom:
        add mirror[0]
        add jewelrybox[0]
        add blueprint[0]
        add Cursor("images/magnifyingglass_UI.png")
    screen officedesk:
        add cipher[0]
        add letters[0]
        add glasses[0]
        add Cursor("images/magnifyingglass_UI.png")
    screen bedroomFlashlight:
        add Flashlight()
        add mirror[0]
        add jewelrybox[0]
        add blueprint[0]
        add Cursor("images/magnifyingglass_UI.png")
    screen officedeskFlashlight:
        add Flashlight()
        add cipher[0]
        add letters[0]
        add glasses[0]
        add Cursor("images/magnifyingglass_UI.png")
    screen parlor:
        add cryphoto[0]
        add book[0]
        add sword[0]
        add Cursor("images/magnifyingglass_UI.png")
    screen parlorFlashlight:
        add Flashlight()
        add cryphoto[0]
        add book[0]
        add sword[0] 
        add Cursor("images/magnifyingglass_UI.png")
    screen darkness:
        add Flashlight()
        add Cursor("images/magnifyingglass_UI.png")
    screen baton:
        add baton[0]
        add Cursor("images/magnifyingglass_UI.png")
    screen parliamentarian:
        add note2[0]
        add typewriter [0]
        add Cursor("images/magnifyingglass_UI.png")
    screen icons:
        add icon[0]
    
    # make this work
    #$ mouse_visible = False
    #call screen flashlight_demo
    
    #this is how you change angelica's corner image
    show angelica normal hidden
    show angelica angry hidden
    show angelica normal
    
    play music "sounds/Busy_Music.ogg" loop
    show bg chapter1
    
    "London, 1875.\n\n A Member of Parliament, Harold Fredrickson, has tried to kill Her Majesty Queen Victoria.
     \n\nA league of private detectives thwarted the attempt, and took the would-be killer into custody.
     \n\nYou are Angelica Hall, the first female private eye in Britain. You're bright, but underestimated by your peers. Maybe this case is the chance you need to prove yourself."
    show bg policeLobby
    with dissolve
    angelica "(Huh, everyone's in the interrogation room with the would-be assassin. It's just like them not to tell me anything. Well, if I look around I should be able to figure it out for myself.)"
    label newsbaton:
        $ mouse_visible = True
        menu:
            #change this to examine room later
            "Examine the room.":
                $ mouse_visible = False
                show screen newspaper
                show screen baton
                "You begin to examine the room. Hover over objects to view them, and click to exit investigation mode."
                hide screen newspaper
                hide screen baton
                jump newsbaton
            "Done examining":
                "(Well, I've got the jist. I'm done larking about.)"
                hide screen newspaper
                hide screen baton
                jump captainWalksIn

    label captainWalksIn:
        show arthur chinanimation at left
        with dissolve
        play sound "sounds/Door_close.ogg"
        angelica "Sir, what the bloody hell is going on?"
        ar "Miss Hall. This assassin case is our top priority. Absolute top! Nothing else to bother with!"
        angelica "You're awfully excited about an attempted murder..."
        ar "It's remarkable! Unreal! We've detained a member of Parliament for trying to murder the Queen!"
        angelica "Impressive police work, sir. I'm ready to help however I can."
        ar "Great. Tip top! I have an important assignment for you! We've got to investigate all of this man's contacts, you see? There could be a conspiracy... a whole spider web just waiting for Her Majesty to get tangled up in! And I don't like spiders. Not at all."
        angelica "Honestly, the entire force knows you don't like spiders, Commissioner. We've all heard the screams."
        ar "In any case! There's an important part of the web I need you to investigate -- the assassin's wife! Befriend her. See what she knows! She could be withholding key information. Critical stuff, my girl!"
        angelica "(The wife? He can't be serious. This isn't police work!)"
        menu:
            "Yes, sir.":
                jump prettiedUp
            "With all due respect, interrogating the wife seems like something one of the younger officers would enjoy.":
                jump centralCase
    label centralCase:
        ar "Nonsense, my dear girl! Even if you were suitable for... traditional detective work, it simply couldn't happen, my dear! You're still a rookie detective! Support team, you see! You've got to work hard and pay those dues!"
        angelica "(Ugh, pay my dues... Suitable my arse.)"
        menu: 
            "Yes, sir.":
                jump prettiedUp
            "Well, if you're going to be sending a lady out after dark, how about some actual protection, sir?":
                ar "Well-well... Very well then. Here, take my night stick -- but be sure to be careful with it! Wouldn't want to scratch that paint!"
                show policebaton
                angelica "Thank you very much, Sir. I'll use it with the utmost discretion."
                hide policebaton
                #add boolean for saying you have a weapon
                jump prettiedUp
        
    label prettiedUp:
        ar "That's what I like to hear! We'll be sending you to a society gathering tonight. Secret idenity! Good chance to get prettied up, eh?"
        menu:
            "Whatever you say, Sir.":
                jump paperwork
            "I'm not here to get prettied up!":
                jump prettiedUp2
        label prettiedUp2:
            ar "Central to the job, my dear! You can get in where no one else can! Gentlemen will spill all kinds of secrets to a pretty lady!"
            angelica "Sir, are you saying you've given up secrets to a pretty lady?."
            ar "Well I-"
            ar "Now see here! I-I have never- I've got to be going. Just keep our of trouble, Ms. Hall!"
            hide arthur chinanimation
            with dissolve
            angelica "I think I just got out of busy work. Now how shall I proceed?"
            menu:
                "Investigate the holding room":
                    jump holdingRoom
                "Investigate commissioner's office":
                    jump captainsOffDead
        label paperwork:
            ar "Yes, Yes. I have some paperwork for you to file in the meantime. Hop to it, now!"
            hide arthur
            with dissolve
            angelica "I'll file the paperwork later. Surely there's something more I can learn about the case... The commissioner never gives me the truly important information. Maybe I can look in his office. Or... is the assassin still in our holding room?)"
            menu:
                "Investigate the holding room":
                    jump holdingRoom
                "Investigate commissioner's office":
                    jump captainsOffDead
    label captainsOffDead:
        stop music
        play sound "sounds/Fast_Footsteps.ogg"
        play sound "sounds/Door_close.ogg"
        play sound "sounds/Gameover.ogg"
        show bg policeCaptainsOffice
        show arthur chinanimation
        with dissolve
        ar "Miss Hall! Are you following me? I'm afraid I'm not your governess. Get back to work, won't you?"
      
        hide arthur chinanimation
        with dissolve
        show bg tryagain
        with dissolve
        "Try again?"
        show bg policeLobby
        with dissolve
        play music "sounds/Busy_Music.ogg" loop
        show arthur chinanimation at left
        with dissolve
        jump paperwork


label holdingRoom:
    hide arthur chinanimation
    stop music
    play music "sounds/dark_strings.ogg"
    show bg policeInterrogationRoom
    angelica "Surely no one will mind if I bring a nice cuppa tea to our restrained guest. I'm simply being hospitable-- even prisoners deserve that!"
    "Voice: Who's there?"
    show harold hanimation at right
    with dissolve
    harold "Ah, you must be the secretary."
    harold "Why on earth would they send you in here?"
    angelica "I just thought I'd bring you some tea."
    angelica "We're British, after all. There is no excuse to skip afternoon tea!"
    harold "Quite right. Bring it here, girl!"
    menu:
        "First, how 'bout you tell me what I want to know?":
            harold "You think I'll blather away at some secretary? I'm not here to supply you with idle gossip, woman."
            harold "If you want to serve me tea, fine. But get on with it."
            menu:
                "But of course. Anything for a charmer like you.":
                    hide harold
                    with dissolve
                    show bg policeInterrogationRoomSpill
                    with dissolve
                    harold "BLAST! That's scalding!"
                    angelica "Oh, I am terribly sorry. How clumsy of me, how dreadful for you!"
                    show bg policeInterrogationRoom
                    with dissolve
                    show harold hanimation at right
                    with dissolve
                    angelica "Today must really not be your day!"
                    harold "Get me a towel, you fool!"
                    angelica "I'm afraid we don't have any."
                    harold "BLAST! Can't get any good help these days"
                    angelica "I know! I'm so sorry, I just started."
                    harold "It's one blunder after another!"
                    harold "Why must I always suffer for others' mistakes?"
                    angelica "That must be so hard for you..."
                    angelica "If only you were in charge. Perhaps things would go your way?"
                    harold "That's bloody right!"
                    angelica "(The Commissioner was right. He's not working alone. And he isn't the leader...)"
                    angelica "And they all threw you to the dogs"
                    angelica "What a sad spectacle"
                    harold "Spectacle! Bloody spectacles, that's all they..."
                    "Harold fell silent, looking down to the table."
                    angelica "(This man is a Member of Parliament. Why would conspirators send him to assassinate the Queen? He didn't have much chance of succeeding.)"
                    angelica "It's a distraction, isn't it?"
                    angelica "There's going to be another assasination attempt!"
                    harold "What? You ridiculous girl..."
                    angelica "And you don't even know it, do you? They were getting you out of the way."
                    angelica "Why did they want you out of Parliament?"
                    harold "I don't know what you're talking about."
                    "Angelica throws a towel at Harold."
                    angelica "Clean yourself up, you buffoon."
                    angelica "(Maybe I should check the commissioner's office for more information.)"
                    play sound "sounds/Door_Close.ogg"
                    hide harold hanimation
                    with dissolve
                    jump chiefsoffice

                "Tell me what you know or no tea!":
                    harold "You must think me a bloody fool. No tea's that tempting. Off with you!"
                    angelica "How rude!"
                    hide harold
                    with dissolve
                    show bg policeInterrogationRoomSpill
                    with dissolve
                    harold "BLAST! That's scalding! Why am I always suffering for other people's screw ups! Get out of here, I'll call one of the officers!"
                    show bg policeInterrogationRoom
                    with dissolve
                    show harold hanimation at right
                    with dissolve
                    angelica "(Aha! He's not working alone! That's enough for me.)"
                    angelica "You think hot tea is the worst that's in store for you?"
                    angelica "(Maybe I should check the commissioner's office for more information.)"
                    play sound "sounds/Door_Close.ogg"
                    hide harold hanimation
                    with dissolve
                    jump chiefsoffice
                    
        "Well, aren't you charming. Here.":
                    hide harold
                    with dissolve
                    show bg policeInterrogationRoomSpill
                    with dissolve
                    harold "BLAST! That's scalding!"
                    angelica "Oh, I am terribly sorry. How clumsy of me, how dreadful for you!"
                    show bg policeInterrogationRoom
                    with dissolve
                    show harold hanimation at right
                    with dissolve
                    angelica "Today must really not be your day!"
                    harold "Get me a towel, you fool!"
                    angelica "I'm afraid we don't have any."
                    harold "BLAST! Can't get any good help these days"
                    angelica "I know! I'm so sorry, I just started."
                    harold "It's one blunder after another!"
                    harold "Why must I always suffer for others' mistakes?"
                    angelica "That must be so hard for you..."
                    angelica "If only you were in charge. Perhaps things would go your way?"
                    harold "That's bloody right!"
                    angelica "(The Commissioner was right. He's not working alone. And he isn't the leader...)"
                    angelica "And they all threw you to the dogs."
                    angelica "What a sad spectacle."
                    harold "Spectacle! Bloody spectacles, that's all they..."
                    "Harold fell silent, looking down to the table."
                    angelica "(This man is a Member of Parliament. Why would conspirators send him to assassinate the Queen? He didn't have much chance of succeeding.)"
                    angelica "It's a distraction, isn't it?"
                    angelica "There's going to be another assasination attempt!"
                    harold "What? You ridiculous girl..."
                    angelica "And you don't even know it, do you? They were getting you out of the way."
                    angelica "Why did they want you out of Parliament?"
                    harold "I don't know what you're talking about."
                    "Angelica throws a towel at Harold."
                    angelica "Clean yourself up, you buffoon."
                    angelica "(Maybe I should check the commissioner's office for more information.)"
                    play sound "sounds/Door_Close.ogg"
                    hide harold hanimation
                    with dissolve
                    jump chiefsoffice

label chiefsoffice:
    show bg policeCaptainsOffice
    stop music
    play music "sounds/arthur_song.ogg" loop
    show arthur chinanimation at left
    with dissolve
    ar "Oho! Did you need something?"
    angelica "I was hoping you could give me more information on my assignment, sir."
    ar "Ah! Of course! Yes, it's quite exciting. I'm sending you to quite a shindig."
    ar "The Countess of Worthington is hosting her annual gala tomorrow night. You will be Miss Elizabeth Kent. Quite brilliant, yes?"
    angelica "What, a fake name?"
    ar "Quite right! No one will know your true identity!"
    angelica "Sir, they didn't know my original identity."
    angelica "In any case, how do you know the suspect's wife will be there?"
    ar "One of our agents has befriended Mrs. Fredrickson's coachman. He says she is intent on going to the party tomorrow."
    angelica "I don't know anything about her. How am I supposed to befriend her?"
    ar "I'm sure you have your ways! Feminine wiles, yes?"
    angelica "My feminine wiles usually work on *men*, sir."
    ar "Of course, my dear! But I did hear quite a rumor. From the coachman, you know! He said Mrs. Fredrickson has been down to entertain many ladies late into the night."
    angelica "I'm not sure I understand. Entertain?"
    ar "Quite scandalous, yes? Ha! Well now. Perhaps your feminine wiles will be of service after all!"
    menu:
        "Ohh. Well, I'll, uh, do my best, sir.":
            ar "That's what I like to hear! Find out what she knows!"
            angelica "(Time to go to that party!)"
            hide arthur chinanimation
            with dissolve
            jump party
                
        "Sir, this might be an innocent woman... perhaps that's going a bit far.":
            ar "Innocent! Well, perhaps of the crime! Ha! Do as you wish, my dear! Just get any information she knows!"
            angelica "(Time to go to that party!)"
            hide arthur chinanimation
            with dissolve
            jump party

label party:
    show bg chapter2
    with dissolve
    " To the party!"
    show bg angelicadress
    with dissolve
    stop music
    play music "sounds/ball_room_waltz_1_.ogg" loop
    angelica "(This is the fanciest event I've ever been to. Thankfully, I have a fancy dress to match. Let's see if I can blend in with high society long enough to find the would-be killer's wife?)"
    show bg party
    with dissolve
    angelica "(There's a woman in the corner, by herself. Everyone's ignoring her. I wonder if that's Mrs. Fredrickson?)"
    menu:
        "Maybe I'll observe her for a little while":
            show countess countanimation
            with dissolve
            countess "It's unbecoming to stare, child."
            angelica "I'm sure I don't know what you mean."
            countess "You're staring at that woman in the corner, dear. It is most improper."
            countess "You look like a hound waiting for its meal!"
            menu: 
                "I assure you that was not my intention.":
                    countess "Who cares what you intended, child? I'm the hostess of this gala, and you ought to watch what you do in my company. If you forget your manners, you might end up like the woman you're staring at, and who wants that?"
                    angelica "What, did she pick up the wrong spoon at a fancy dinner?"
                    countess "Hmph! Really! But I'm sure you're curious, child? I'll tell you why no one's speaking to her if you'll stop making a scene with your incessant staring."
                    menu:
                        "I don't particularly care to hear your idle prattle":
                            jump lifedull
                        "Please, my lady, do share your wisdom with me.":
                            countess "That's Mrs. Fredrickson hiding in the corner over there. Her husband tried to kill the queen, you know."
                            countess "And she still has the gall to come to my party. Clearly she doesn't realize she's nobody of importance anymore! Almost like you, dear!"
                            menu:
                                "You're more of a scoundrel than a lady, aren't you?":
                                    jump supermean
                                "Truly, her decisions seem ill-advised.":
                                    jump shesdumb
                "One might say those who compare ladies to dogs are most improper.":
                    jump hostesses
            label hostesses:
                countess "Hmph! You would think guests might treat their hostesses with a bit more respect!"
                angelica "So you're the Countess of Worthington?"
                countess "Hmph! Really! You've come to my party without an inkling of who I am?"
                angelica "You don't know who I am either!"
                countess "It hardly matters, does it? I'm somebody of importance... If I don't know you already, then you're clearly no one significant... I know everyone worth knowing. And if you're nobody at all, how on earth were you invited to my gala?"
                angelica "(uh oh.)"
                angelica "Isn't it your job to know who's invited to your own party?"
                countess "People like me, child, have other people to do that for us. I'm sure you don't know what that's like. You probably busy yourself with crude embroidery and entertaining your poor marriage prospects."
                angelica "You seem a little bitter."
                countess "Bitter! Hmph! How dare you! I'm worth ten of you! No, fifteen!"
                menu:
                    "I'll keep that in mind for moments when life seems too dull.":
                        jump lifedull
                
                    "Forgive my rudeness. Weren't you going to tell me something?":
                        jump tellsomething
                        
                label lifedull:
                    countess "Hmph! You petulant child! You clearly don't belong at society gatherings."
                    countess "Go talk to Mrs. Fredrickson, then-- you should find yourself quite comfortable amongst her and her ilk."
                    angelica "Perhaps I shall show Mrs. Fredrickson some better company."
                    hide countess countanimation
                    with dissolve
                    jump followbeatrice
                    
        "Shall I go and speak with her?":
            jump beatriceskip
                
        "Oh look, a drunkard in the corner!":
            show shady shadimation
            with dissolve
            angelica "(Well this should be good for a laugh)"
            angelica "And how are you tonight, good sir?"
            shady "Lovely, my fair lady! Everything is lovely! Should you care to drink with me?"
            angelica "Why, I think not. Here we are celebrating after our own Queen was only just subject to an assassination attempt. \ Don't you find it crass?"
            shady "This is why we must celebrate, my dear! \ She was not assassinated, she lives on, as must we all!"
            angelica "That is a good way to look at things. \ Poor Lady Fredrickson, I don't suppose she can see it that way!"
            shady "Oh, I think that might be exactly how she sees it!"
            angelica "What do you mean?"
            shady "The girl despised her husband, I hear! \ All those people thinking she could've had something to do with that. \ They're all daft!"
            angelica "Yes, I suppose so."
            angelica "(I guess I'm not the only one who thinks this assignment is pointless.)"
            shady "Anyone who pays attention knows that the young lady has no appreciation for... a man's company, should I say?"
            angelica "Oh, you think?"
            angelica "(Maybe this won't be such a waste...\ For me, anyway.)"
            hide shady shadimation
            with dissolve
            menu:
                "Maybe I should find out if the rumors are true?":
                    jump followbeatrice
                     
                "Perhaps I should question other guests first.":
                    show countess countanimation
                    angelica "How are you enjoying the party?"
                    countess "Certainly I am not. Ilk of all kinds are present here! That disgusting man, and that foolish child of a lady!"
                    menu:
                        "And who are you to cast such harsh judgement?":
                            jump hostesses
                        "You seem like a very wise judge of character.":
                            jump shesdumb

label tellsomething:
    countess "That's Mrs. Fredrickson hiding in the corner over there. Her husband tried to kill the queen, you know. \ And she still has the gall to come to my party."
    countess "Clearly she doesn't realize she's nobody of importance anymore! Almost like you, dear!"
    menu:
        "You're more of a scoundrel than a lady, aren't you?":
            jump supermean
        
        "Truly, her decisions seem ill-advised":
            jump shesdumb
            
    label supermean:
        countess "I didn't make the world this way, darling, that's just the way things are!"
        hide countess countanimation
        with dissolve
        angelica "What a dreadful woman! Shall I look for better company?"
        jump followbeatrice
    
    label shesdumb:
        countess "Truly! The silly thing doesn't realize her society life is over. It's quite amusing!"
        countess "Do you know what would be fun, child? You ought to go talk to her. I'd like to know what she was thinking by coming here tonight. \ But someone of my stature talking to someone like her... ha! \You would be a more appropriate match for her."
        menu:
            "You love to tell terrible tales, don't you?":
                jump supermean
            
            "I could converse with her, perhaps.":
                hide countess countanimation
                with dissolve 
                jump followbeatrice
        
label followbeatrice:
    hide countess countanimation
    with dissolve
    angelica "(It looks like Mrs. Fredrickson has gone to freshen up. Perhaps I can start up a conversation with her.)"
    show bg beatriceandshady
    with dissolve
    angelica "(Oh no, that drunken man from before has stopped her.)"
    beat "What are these?"
    shady "Just some documents, ma'am. Give my best to your husband."
    show bg party
    with dissolve
    angelica "Wait, what was that? Is it possible that she had something to do with this after all? I'll strike up a conversation..."
    show beat banimation
    with dissolve
    menu:
        "Mrs. Fredrickson, what on earth are you doing here?":
            hide beat banimation
            show beat cryanimation
            angelica "(Oh, lovely.)"
            beat "Are you here to tell me how ashamed I should be of my husband? How I should be embarassed to simply exist?"
            menu:
                "Of course not! Please stop crying...":
                    hide beat cryanimation
                    show beat banimation
                    beat "I just saw you speaking with the Countess. She is notoriously obsessed with reputation, which means she decides everyone else's reputation. \ I think she told everyone at the party to avoid me!"
                    hide beat banimation
                    show beat cryanimation
                    angelica "(Oh, don't start crying again!)"
                    menu:
                        "She did seem to be one for idle gossip and foolishness.":
                            beat "The countess is a woman of great reputation, which means she decides what everyone else's reputation is. \ Now I'm without a husband and without friends."
                            angelica "Good friends are hard to come by, and I don't think she was ever a good one."
                            beat "No, she was rotten. But I'm sure a young lady like you doesn't care to hear the musings of a lonely wife. So lonely..."
                            jump dontcry
                            
                            
                        "I won't pretend she didn't prattle like a madwoman about you.":
                            beat "I'm sure you found my misfortunes quite amusing. Almost as good as the tabloids, yes?"
                            hide beat banimation
                            show beat cryanimation
                            angelica "(Uh oh...)"
                            angelica "I didn't mean to offend, Mrs. Fredrickson! \ Your strength in these times is truly admirable."
                            hide beat cryanimation
                            show beat banimation
                            beat "Call me Beatrice, won't you? I appreciate your kindness. Few have shown it to me tonight."
                            angelica "Good friends are hard to come by, and I don't think anyone here is a good friend."
                            beat "No, they're all rotten. Except for you, it seems. \ But I'm sure a young lady like you doesn't care to hear the musings of a lonely wife. So lonely..."
                            jump dontcry
                                      
                        
                "Maybe you should learn to be a better judge of character.":
                    beat "Judge of character?! Do you think I am clairvoyant? How on earth would I have predicted that my husband would try to kill the Queen? That's insanity!"
                    angelica "I spoke out of turn, my apologies. If you could just... stop crying... please."
                    beat "Leave me be!"
                    hide beat cryanimation
                    with dissolve
                    angelica "Lovely. I've wasted my chance to talk to my target. But she's still at the party... maybe if I rush back to her house, I could investigate before she comes home? Then tonight won't be an entire waste."
                    jump beatricefail
                    return
                    
        "A lady as lovely as you shouldn't be left alone.":
            jump sorryignoring
        
label beatriceskip:
    angelica "(It looks like Mrs. Fredrickson has gone to freshen up. Perhaps I can start up a conversation with her.)"
    show bg beatriceandshady
    with dissolve
    angelica "(Oh no, that drunken man from before has stopped her.)"
    beat "What are these?"
    shady "Just some documents, ma'am. Give my best to your husband."
    show bg party
    with dissolve
    angelica "Wait, what was that? Is it possible that she had something to do with this after all? I'll strike up a conversation..."
    show beat banimation
    with dissolve
    angelica "A lady as lovely as you shouldn't be left alone."
    jump sorryignoring
  
label sorryignoring:
    beat "I appreciate your kindness. Few have shown it to me tonight. But you probably just don't know who I am..."
    angelica "I do, Mrs. Fredrickson. It just seemed a shame that everyone else here decided to judge you for someone else's crime."
    beat "Call me Beatrice, please. Everyone is rotten here. Except for you, it seems! But I'm sure a young lady like you doesn't care to hear the musings of a lonely wife. So lonely..."
    jump dontcry
    
label dontcry:
    hide beat banimation
    show beat cryanimation
    angelica "No, no! I love your musings! Why don't I keep you company?"
    hide beat cryanimation
    show beat banimation
    angelica "I think you need better companions. Perhaps I could escort you from the party?"
    beat "I know there have been rumors about my ... impropriety ... in the past. \I can assure you that true ladies are never more than friends with one another."
    beat "That said, I am not opposed to recieving ladies in my parlor. Perhaps, if you feel as unwelcome at this party as I do, you might retire with me."
    angelica "(Perhaps Beatrice's 'impropriety' isn't so long past? \ While not entirely sanctioned by my mission,  her invitation is far too... tempting an opportunity. To look into Lord Fredrickson's house, of course!"
    angelica "That seems like a lovely idea."
    hide beat banimation
    with dissolve
    jump beatricehouse
#end ballroom scene




















#start beatrice house scenes

# beatrice fail route 
label beatricefail:
    show bg chapter3
    with dissolve
    "Searching the house"
    show screen darkness
    show bg parlor
    stop music
    play music "sounds/dark_strings.ogg"
    angelica "(I've got to be quiet. Can't risk being found or I could risk the entire investigation. \ I'll have to use a lantern so as not to alert anyone of my presence."
    menu:
        "Examine Parlor":
            hide screen darkness
            jump parlorlantern
        "Examine Bedroom":
            hide screen darkness
            jump bedroomcantgetin
        "Examine Office":
            hide screen darkness
            jump officelantern
       
label parlorlantern:
    show screen parlorFlashlight
    show bg parlor
    angelica "Let's see what I can find in here."
    #search no flashlight
    #item 1, wedding photo

    menu:
        "Investigate again?":
            jump parlorlantern
        "I'm done here.":
            menu:
                "Examine Bedroom":
                    hide screen parlorFlashlight
                    jump bedroomcantgetin
                "Examine Office":
                    hide screen parlorFlashlight
                    jump officelantern
                    
label bedroomcantgetin:
    screen darkness
    show bg parlor
    angelica "The door is locked! Maybe I can pick this..."
    angelica "I can't get it open! Hopefully there's nothing important in there..."
    menu:
        "Examine Again?":
            jump bedroomcantgetin
        "Examine Parlor":
            hide screen darkness
            jump parlorlantern
        "Examine Office":
            hide screen darkness
            jump officelantern

label officelantern:
    show screen officedeskFlashlight
    show bg office
    angelica "I wonder what's hidden in here."
  
    #end investigation
    angelica "I think that's all there is here. I suppose I should go."
    menu:
        "Examine again":
            jump officelantern
        "Did I examine the parlor thoroughly?":
            hide screen officedeskFlashlight
            jump parlorlantern
        "Perhaps one last check of the bedroom.":
            hide screen officedeskFlashlight
            jump bedroomcantgetin
        "I should visit the address on that letter.":
            hide screen officedeskFlashlight
            jump parliamentarianoffice
            
  

#beatrice success route
label beatricehouse:
    show bg chapter3
    with dissolve
    "Searching the house"
    show bg parlor
    stop music
    play music "sounds/Beatrice_Sweet.ogg"
    show beat banimation
    with dissolve
    angelica "You have a truly lovely home."
    beat "Yes, I've come to like it. \ But who knows how much longer I'll be able to live here."
    hide beat banimation
    show beat cryanimation
    angelica "No no, my dear, your situation is not so bleak! \ A lovely lady like you, with all your husband's money at your disposal...\ You have the world at your fingertips now!"
    beat "Do you think so?"
    hide beat cryanimation
    show beat banimation
    beat "Yes, maybe now I can travel."
    angelica "Of course you can. See exciting things, meet new people..."
    beat "Oh, that sounds nice. \ Away from all these horrible people. But perhaps I can take one familiar face with me..."
    "Beatrice clasps Angelica's hand."
    angelica "(Perhaps this is gone too far... she's a sweet girl... \ There's no way she could have anything to do with this. \I might actually like her. \Should I be doing this?)"
    menu:
        "I have to be honest with her!":
            jump detectivework
        "The mission is more important.":
            jump angelicaandbeatrice

$ warnbeatrice = False
#tell beatrice the truth            
label detectivework:
    $ warnbeatrice = True
    show bg parlor
    angelica "This isn't right. I can't do this to you. \ I'm not who I say I am."
    beat "What do you mean?"
    angelica "I am a detective assigned to investigate you. I was to see if I could find any leads about the assassination case.  \ I am truly sorry for misleading you, but if you let me, I can help you."
    hide beat banimation
    show beat cryanimation
    angelica "(Not again! Now I've done it...)"
    beat "How can you possibly help me? You're a liar!"
    angelica "If you help me to figure out who is behind this mess, it will help clear your name! You will be vindicated in the eyes of the public."
    beat "Do you truly think so?"
    angelica "I do. Will you help me?"
    beat "I... I suppose I will help you. What can I do?"
    angelica "Who was the man you spoke with earlier tonight?"
    beat "I do not know him. \ He took me aside and wished the best for my scoundrel husband. \ Surely he's a dangerous man! What if he comes after me?"
    angelica "Don't fret, I will protect you."
    hide beat cryanimation
    show beat banimation
    beat "How can I trust you? Were your... advances... towards me just a part of your investigation?"
    menu:
        "Of course not!":
            jump angelicagenuine
        "Yes. I'm truly sorry.":
            jump angelicanongenuine

# make beatrice angry at you
label angelicanongenuine:
    beat "Then I can't trust you at all! Just get out! Take a look around if you must, but stay away from me!"
    hide beat banimation
    #door slam
    #show parlor rather than bedroom
    angelica "(Bloody hell. I've made a good mess of things. \ I didn't even ask about the papers! Well, I should still have a look around.)"
    menu:
        "Examine Again":
            jump angelicanongenuine
        "Examine Parlor":
            jump parlorangrybeatrice
        "Examine Office":
            jump officeangrybeatrice
    
    
#search routes when beatrice gets mad at you. no flashlight.
label officeangrybeatrice:
    show screen officedesk
    show bg office
    angelica "I wonder what's hidden in here."

    menu:
        "Examine again":
            jump officeangrybeatrice
        "Did I examine the parlor thoroughly?":
            hide screen officedesk
            jump parlorangrybeatrice
        "I should visit the address on that letter.":
            hide screen officedesk
            jump parliamentarianoffice

label parlorangrybeatrice:
    show bg parlor
    show screen parlor
    angelica "Let's see what I can find in here."
   
    menu:
        "Investigate again?":
            jump parlorlantern
        "I'm done here.":
            menu:
                "Examine Office":
                    hide screen parlor
                    jump officeangrybeatrice
                    
#be honest with beatrice but still seduce
label angelicagenuine:
    angelica "I'll stay with you all night if I have to."
    beat "Oh will you? \ It will get quite boring, just staying and watching over me."
    angelica "Well, I'm sure we can find other ways to pass the time."
    beat "The things you say...\ I wish I you would take responsibility for them."
    jump angelicaandbeatrice

# seduce beatrice
label angelicaandbeatrice:
    angelica "A virtous young lady entertaining a commoner? \ You seek to truly ruin yourself, my lady! I would love ot be the one who ruins you."
    beat "I'm afraid I've already been tarnished."
    angelica "The one I see before me is nothing but pristine. Let me fix that."
    #fade to black
    hide beat banimation
    with dissolve
    hide bg parlor
    with dissolve
    show bg bedroom
    with dissolve
    angelica "She should be sleeping soundly for a good few hours. Suprisingly agressive for such a teary woman...\ Now let me take a look around and see what I can find."
    menu:
        "Examine Bedroom":
            jump examinebedroom
        "Examine Parlor":
            jump examineparlor
        "Examine Office":
            jump examineoffice
            
#search post seducy stuff- flashlight in bedroom only
label examinebedroom:
    show screen bedroomFlashlight
    show bg bedroom
    #show bedroom
    angelica "Time to take a look around. I have to be careful not to wake Beatrice."
    
    angelica "I think that's everything in here."
    if blueprint[0].getViewed() :
        show screen icons
    menu:
        "Examine Again?":
            jump examinebedroom
        "Examine Parlor":
            hide screen bedroomFlashlight
            jump examineparlor
        "Examine Office":
            hide screen bedroomFlashlight
            jump examineoffice
        

label examineparlor:
    show bg parlor
    show screen parlor
    angelica "Let's see what I can find in here."

    menu:
        "Examine Again?":
            jump examineparlor
        "Examine Bedroom":
            hide screen parlor
            jump examinebedroom
        "Examine Office":
            hide screen parlor
            jump examineoffice
                
label examineoffice:
    show screen officedesk
    show bg office
    angelica "I wonder what's hidden in here."

    angelica "I think that's all there is here. I suppose I should go."
    menu:
        "Examine Again?":
            jump examineoffice
        "Did I examine the parlor thoroughly?":
            hide screen officedesk
            jump examineparlor
        "Perhaps one last check of the bedroom.":
            hide screen officedesk
            jump examinebedroom
        "I should visit the address on that letter.":
            hide screen officedesk
            jump parliamentarianoffice

#end of beatrice house 

#beginning parliamentarian office














#beginning parliamentarian office

label parliamentarianoffice:
    show bg chapter4
    with dissolve
    #show bg parliamentexterior
    stop music
    play music "sounds/Palace_Fugue.ogg"
    angelica "The palace of Westminster... I've never been inside the Parliament building before. The letter I found came from an office in here. I'll have to take a good look around... I really think I'm getting close."
    show bg parliamenthallway
    with dissolve
    angelica "Here it is! There have to be answers behind this door."
    show bg parliamentoffice
    with dissolve
    show assistant asanimation
    with dissolve
    assistant "What are you doing here?"
    angelica "Er..."
    menu:
        "There's a fire, you have to evacuate!":
            jump fire
        "I'm here to pick up some papers":
            jump papers
        "Your boss is downstairs, he said to come get you immediately!":
            jump downstairs
            
            
            
label fire:
    assistant "A fire?! Not again! We must go now!"
    #angryangelicasprite
    show bg parliamenthallway
    with dissolve
    angelica "Please, exit quietly and calmly. \ No need to start a panic."
    assistant "I can't possibly just leave you behind!"
    angelica " I still have to evacuate the rest of the building. Try to lead out as many people on your way as you can."
    assistant "A-Alright. Be careful, ma'am."
    hide assistant asanimation
    with dissolve
    angelica " Good. Now down to business."
    
    jump searchfire
    
label searchfire:
    show bg parliamentoffice
    with dissolve
    angelica "Let's see what we can find."
    show screen parliamentarian
    #screen random papers, papers, and typewriter
    angelica "I hope that's everything."
    menu: 
        "Examine again?":
            jump searchfire
        "I think I'm done examining.":
            hide screen parliamentarian
            angelica "That's everything. Let's see if this cipher can decipher the message."
            show noteundeciphered
            with dissolve
            angelica "If I transpose each letter..."
            hide noteundeciphered
            with dissolve
            show bg angelicacipher
            with dissolve
            angelica "I think I've got it!"
            show notedeciphered
            with dissolve
            #hide cipher
            angelica "Meet before dawn on Thursday the 27th... between Charlotte and Rathbone."
            angelica "That's tomorrow morning! Who is he meeting with?"   
            hide notedeciphered 
            with dissolve
            jump alley
            
        
label papers:
    assistant "What papers?"
    angelica "Sir, I'm just the secretary. How should I know which papers he was referring to?"
    assistant "Who's 'he'? Who do you work for?"
    angelica "Mr... Smith. (The odds are with me, at least)"
    assistant "Oh, I see. the one down the hall, then? Or on the fourth floor?"
    angelica "Fourth floor."
    assistant "I see. I certainly don't know what papers you're talking about. I shall check in our filing room, I won't be a moment."
    angelica "Of course. I will wait here for you."
    hide assistant asanimation
    with dissolve
    jump searchpapers

label searchpapers:
    show bg parliamentoffice
    with dissolve
    angelica "Let's see what we can find."
    show screen parliamentarian
    #screen random papers, papers, and typewriter
    angelica "I hope that's everything."
    menu: 
        "Examine again?":
            jump searchpapers
        "I think I'm done examining.":
            hide screen parliamentarian
            angelica "That's everything. Let's see if this cipher can decipher the message."
            show noteundeciphered
            with dissolve
            angelica "If I transpose each letter..."
            hide noteundeciphered
            with dissolve
            show bg angelicacipher
            with dissolve
            angelica "I think I've got it!"
            show notedeciphered
            with dissolve
            #hide cipher
            angelica "Meet before dawn on Thursday the 27th... between Charlotte and Rathbone."
            angelica "That's tomorrow morning! Who is he meeting with?"   
            hide notedeciphered 
            with dissolve
            #hide cipher with solved paper
            show bg parliamentoffice
            with dissolve
            show assistant asanimation
            with dissolve
            assistant "What on earth are you doing? These are private documents!"
            angelica "Oh, I'm terribly sorry. I seem to have gotten fidgety waiting."
            assistant "If I told Mr. Aldredge a stranger had looked through his desk, I'd be out of a job! I didn't find any papers in the back, so just get out of here and we'll pretend this never happened!"
            hide assistant asanimation
            with dissolve
            jump alley
            
            
label downstairs:
    assistant "His lordship isn't in the city right now, so I can hardly believe that."
    angelica "Oh! Well, I assure you I am--"
    assistant "A lying scoundrel?"
    #angelica sad face
    angelica "I... I am terribly sorry for trying to decieve you but--"
    assistant "I think it's best you leave."
    angelica "No, please, you don't understand!"
    assistant "Guards!"
    hide assistant asanimation
    with dissolve
    show bg tryagain
    with dissolve
    "You were arrested for breaking into Parliament."
    "Try again?"
    jump parliamentarianoffice


label alley:

#cutscene
show bg chapter5
with dissolve
"The Meeting"
show bg alley
with dissolve
stop music
play music "sounds/Alley_Sounds.ogg" loop
angelica "This is their meeting spot. Better hide before someone gets here!"

show shady shadimation at right 
with dissolve
angelica "(It's the shady man from the party... he's definitely up to skullduggery. \ Is he still drunk, or does he just look like that?)"
shady "I have confirmed the Queen's meeting with the Prime Minister tomorrow."
angelica "(Who is he talking to?)"
shady "The weapon has been planted. Tomorrow marks the dawn of a new age."

hide shady shadimation
with dissolve

stop music
queue music ["sounds/Bitter_Intro.ogg", "sounds/Just_Bitter.ogg"] loop
play music "sounds/Beatrice_Bitter.ogg" loop


show bg cutscene1
with dissolve
beat "And it will be a firey dawn indeed."
angelica "What?"
angelica "B-Beatrice? You're leading the conspiracy?"
beat "Well well, looks like you're more than just a secretary after all."
shady "Ma'am--"
beat "Hush dear, the ladies are talking now."
show bg cutscene2
with dissolve
angelica "You know, now that I think about it, it all seems very obvious."
beat "Naturally. But of course, you were blinded by your own views."
angelica "Is that so? Well--"
show bg cutscene3
with dissolve
angelica "Allow me to rectify that mistake!"
beat "My pleasure!"
show bg cutscene4
with dissolve
beat "Honestly... I would have thought of you as an ally!"
angelica "Why would I want the Queen dead? Why do you?"
beat "Oh, Angelica. You make your own way, but you will always be stifled. \ I have a riddle for you."
angelica "Never cared for riddles."
beat "One person plays the game, but ignores the rules. The other follows the rules but isn't really playing the game. Who wins? The one playing, right?"
angelica "This isn't a game, Beatrice!"
beat "Unless someone flips over the board!"
show bg cutscene5
with dissolve
beat "And I'm about to pull everything right out from under the one making all the rules!"
angelica "That's it! *clank*"
show bg cutscene6
with dissolve
angelica "I know where the bomb is! Boys, take care of her."
beat "What? You brought reinforcements?"
angelica "Beatrice, you're under arrest for conspiracy to assassinate the Queen."
angelica "Commissioner, we have a Queen to save. Come with me!"
jump buckinghampalace

label buckinghampalace:

#If you warned beatrice or broke into her house
    if blueprint[0].getViewed() == True:
        jump buckinghamnoblueprint
#if you didn't warn beatrice
    jump buckinghamblueprint
    
label buckinghamblueprint:
    show bg chapter6
    with dissolve
    "Stop the bomb!"
    show bg buckingham
    with dissolve
    show guard guardimation at right
    with dissolve
    guard "Excuse me, what is your business here?"
    #show angry angelica
    angelica "I'm with the police, this is an emergency!"
    guard "Madam--"
    show arthur chinanimation at left
    ar "I'm police commissioner Charleston. We have intelligence that there is a bomb on the premises-- another attempt on the Queen's life!"
    angelica "Let us through!"
    guard "R-right! Sound the alarms!"
    ar "We have to get everyone out! We have no idea how large this explosive might be."
    angelica "Guard! Take a look at this map. What room is on this blueprint?"
    guard "Ma'am, that's this room. This is where the Queen recieves the Prime Minister for meetings."
    hide guard guardimation
    with dissolve
    show victoria victoranimation at right
    with dissolve
    angelica "Your majesty, you are in grave danger!"
    ar "Come with me, your majesty! We're evacuating the palace!"
    angelica "I'll stay behind and see if I can disarm the bomb."
    hide victoria victoranimation
    with dissolve
    hide arthur chinanimation
    with dissolve
    angelica "If this is that wall... the bomb must be behind that painting!"
    angelica "Found it! Look at all these gears... it must be set to explode when the clock reaches a certain time. If I can take out the right gear, the clock will stop ticking."
    angelica "Got it! We're safe!"
    with dissolve
    show arthur chinanimation at left
    with dissolve
    show victoria victoranimation at right
    with dissolve
    queen "I cannot sufficiently express my gratitude for your service. I have faith that we will prevail against the evils conspiring to defeat us."
    queen "All the men here shall be knighted!"
    angelica "(sigh)"
    hide victoria victoranimation
    with dissolve
    show bg policeLobby
    with dissolve
    play music "sounds/Busy_Music.ogg" loop
    if warnbeatrice:
        ar "Absolutely remarkable! Top police work, my dear!"
        ar "We'll be charging Lord Aldredge with heading the conspiracy!"
        angelica "Sorry, who?"
        ar "The man with the mustache, my dear!"
        angelica "But he wasn't in charge-- it was Beatrice!"
        ar "Our men searched her home, and found a stack of papers burnt in the fireplace. We're afraid any evidence we might have had against her was lost in the fire. \Rather strange! It's as if she knew we were coming!"
        angelica "(Maybe I should'nt have trusted Beatrice...)"
        ar "Lord Aldredge confessed to planting the bomb! We're sure to convict him!"
        angelica "But..."
        ar "No buts! It's done with! Wrapped up! Thanks to your hard work, my dear, I'm promoting you to a full detective! Secretaries be damned!"
        angelica "Thank you sir. I'm ready for my next assignment!"
        jump betrayedbybeatricewin
    ar "Absolutely remarkable! Top police work, my dear!"
    ar "We'll be charging Lady Fredrickson with heading the conspiracy!"
    ar "It's done with! Wrapped up! Thanks to your hard work, my dear, I'm promoting you to a full detective! Secretaries be damned!"
    angelica "Thank you sir. I'm ready for my next assignment!"
    "Congratulations! You prevented the destruction of Buckingham Palace, caught the head conspirator and saved the Queen!  Excellent work, detective."
    return
    
    

label buckinghamnoblueprint:
    show bg chapter6
    with dissolve
    "Stop the bomb!"
    show bg buckingham
    with dissolve
    show guard guardimation at right
    with dissolve
    guard "Excuse me, what is your business here?"
    #show angry angelica
    angelica "I'm with the police, this is an emergency!"
    guard "Madam--"
    show arthur chinanimation at left
    ar "I'm police commissioner Charleston. We have intelligence that there is a bomb on the premises-- another attempt on the Queen's life!"
    angelica "Let us through!"
    guard "R-right! Sound the alarms!"
    ar "We have to get everyone out! We have no idea how large this explosive might be."
    menu:
        "I'll come with you to evacuate the queen!":
            hide arthur chinanimation
            with dissolve
            hide guard guardimation
            with dissolve
            jump evacuatevictoria
        "There may not be enough time! I'll try to disarm the bomb!":
            jump bombdead
          


label evacuatevictoria:
    "(Future Cutscene) Angelica helps Queen Victoria flee the palace just as a substantial portion of it is blown to smithereens."
    show bg policeLobby
    with dissolve
    play music "sounds/Busy_Music.ogg" loop
    show arthur chinanimation at left
    with dissolve
    show victoria victoranimation at right
    with dissolve
    queen "I cannot sufficiently express my gratitude for your service. Although the destruction of Buckingham Palace marks a dark day for the British Empire, I have faith that we will prevail against the evils conspiring to defeat us."
    queen "All the men here shall be knighted!"
    angelica "(sigh)"
    hide victoria victoranimation
    with dissolve
    show bg policeLobby
    with dissolve
    if warnbeatrice == True:
        ar "Absolutely remarkable! Top police work, my dear!"
        ar "We'll be charging Lord Aldredge with heading the conspiracy!"
        angelica "Sorry, who?"
        ar "The man with the mustache, my dear!"
        angelica "But he wasn't in charge-- it was Beatrice!"
        ar "Our men searched her home, and found a stack of papers burnt in the fireplace. We're afraid any evidence we might have had against her was lost in the fire. \Rather strange! It's as if she knew we were coming!"
        angelica "(Maybe I should'nt have trusted Beatrice...)"
        ar "Lord Aldredge confessed to planting the bomb! We're sure to convict him!"
        angelica "But..."
        ar "No buts! It's done with! Wrapped up! Thanks to your hard work, my dear, I'm promoting you to a full detective! Secretaries be damned!"
        angelica "Thank you sir. I'm ready for my next assignment!"
        jump betrayedbybeatrice
    ar "Absolutely remarkable! Top police work, my dear!"
    ar "We'll be charging Lady Fredrickson with heading the conspiracy!"
    ar "It's done with! Wrapped up! Thanks to your hard work, my dear, I'm promoting you to a full detective! Secretaries be damned!"
    angelica "Thank you sir. I'm ready for my next assignment!"
    "Congratulations! Maybe you didn't save the palace, but you caught the head conspirator and saved the Queen! Good work, detective."
    return

    

label bombdead:
    hide arthur chinanimation
    with dissolve
    show bg youdied
    with dissolve
    "You don't know where the bomb is. You died in explosion. If only you had found a clue about the bomb's location..."
    "Try again?"
    jump buckinghamnoblueprint


label betrayedbybeatrice:
    "Congratulations! Even if you didn't save the palace... or convict the right conspirator... you still saved the Queen! It's the thought that counts, right?"
    return

label betrayedbybeatricewin:
    "Congratulations! You may not have secured Beatrice's place behind bars, but you saved the Queen and prevented the destruction of Buckingham Palace! Good work, detective."
    return

"End of Demo"
return 
