# You can place the script of your game in this file.
init python:

    import math

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
            rcenter = (300, 100)
            render.blit(child_render, rcenter)

            # Return the render.
            return render

        def event(self, ev, x, y, st):

            # Compute the distance between the center of this displayable and
            # the mouse pointer. The mouse pointer is supplied in x and y,
            # relative to the upper-left corner of the displayable.
            px,py = self.pos
            distance = math.hypot(x - (self.width / 2)-px, y - (self.height / 2)-py)

            # Base on the distance, figure out an alpha.
            if distance <= self.opaque_distance:
                alpha = 1.0
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

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"
image bg policeLobby = "images/Policelobby_1.png"
image bg policeInterogationRoom = "images/PoliceInterrogation_1.png"
image bg party = "images/Ballroom_l.png"
image bg policeCaptainsOffice = "images/captainsOffice.png"

#image angelica smile ".png"
image arthur normal = "images/arthursingle.png"
#image harold normal ".png"
image policebaton = "images/baton.png"

# Declare characters used by this game.
define angelica = Character('Angelica Hall', color="#c8ffc8",
                            window_left_padding=300,
                            show_side_image=Image("images/angelica/Angelica_Corner_Idle.png",
                            xalign=0.0, yalign=1.0))
define ar = Character('Arthur Charleston', image="arthur")
define harold = Character('Harold Fredrickson', color="#a7ffc8")
define countess = Character('Countess', color="#a7ffc8")
define beat = Character('Beatrice Fredrickson', color="#a7ffc8")

#stop music
#play sound "effect.oog"

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
    image beat banimation = Animation("images/beatrice/Beatrice_Test0001.png", .16,
                                          "images/beatrice/Beatrice_Test0002.png", .16,
                                          "images/beatrice/Beatrice_Test0003.png", .16,
                                          "images/beatrice/Beatrice_Test0004.png", .16,
                                          "images/beatrice/Beatrice_Test0005.png", .16,
                                          "images/beatrice/Beatrice_Test0006.png", .16)
    image countess countanimation = Animation("images/Countess_Indifferent/Countess_Indifferent0001.png", .16,
                                              "images/Countess_Indifferent/Countess_Indifferent0002.png", .16,
                                              "images/Countess_Indifferent/Countess_Indifferent0003.png", .16,
                                              "images/Countess_Indifferent/Countess_Indifferent0004.png", .16,
                                              "images/Countess_Indifferent/Countess_Indifferent0005.png", .16,
                                              "images/Countess_Indifferent/Countess_Indifferent0006.png", .16,)
screen newspaper:
    add Appearing("images/police_news.png", (720,300), 40, 100)
screen baton:
    add Appearing("images/baton.png", (1100,180), 40, 100)
screen flashlight_demo:
    textbutton "continue" xpos 300 ypos 300 action Return()
    add Flashlight()
    
# The game starts here.
label start:    
    #$ mouse_visible = False
    #call screen flashlight_demo
    play music "sounds/Busy_Music.ogg" loop
    show bg policeLobby
    "London, 1875.\n\n A Member of Parliament, Harold Fredrickson, has tried to kill Her Majesty Queen Victoria.
     \n\nA league of private detectives thwarted the attempt, and took the would-be killer into custody.
     \n\nYou are Angelica Hall, the first female private eye in Britain. You're bright, but underestimated by your peers. Maybe this case is the chance you need to prove yourself."
    angelica "(Huh, everyone's in the interrogation room with the would-be assassin. It's just like them not to tell me anything. Well, if I look around I should be able to figure it out for myself.)"
    label newsbaton:
        menu:
            #change this to examine room later
            "Examine the room.":
                show screen newspaper
                show screen baton
                "I see a newspaper, and a baton..."
                "I see our arrest has made the tabloids. That baton belongs to the Police Commissioner. It's basically a useless decoration -- I doubt he's patrolling the streets much anymore."
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
            angelica "I think I just got out of busy work. Now how shall I proceed?"
            menu:
                "Investigate the holding room":
                    jump holdingRoom
                "Investigate commissioner's office":
                    jump captainsOffDead
        label paperwork:
            ar "Yes, Yes. I have some paperwork for you to file in the meantime. Hop to it, now!"
            hide arthur
            angelica "I'll file the paperwork later. Surely there's something more I can learn about the case... The commissioner never gives me the truly important information. Maybe I can look in his office. Or... is the assassin still in our holding room?)"
            menu:
                "Investigate the holding room":
                    jump holdingRoom
                "Investigate commissioner's office":
                    jump captainsOffDead
    label captainsOffDead:
        stop music
        play sound "sounds/Fast_Footsteps.ogg"
        show bg policeCaptainsOffice
        show arthur chinanimation
        ar "Miss Hall! Are you following me? I'm afraid I'm not your governess. Get back to work, won't you?"
        play sound "sounds/Gameover.ogg"
        menu:
            "Try again":
                show bg policeLobby
                play music "sounds/Busy_Music.ogg" loop
                show arthur chinanimation at left
                jump paperwork
    return
    
label holdingRoom:
    hide arthur chinanimation
    stop music
    play music "sounds/dark_strings.ogg"
    show bg policeInterogationRoom
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
                    "Angelica spills hot tea on his lap."
                    harold "BLAST! That's scalding!"
                    angelica "Oh, I am terribly sorry. How clumsy of me, how dreadful for you!"
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
                    angelica "(The Chief was right. He's not working alone. And he isn't the leader...)"
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
                    "Angelica pours hot tea on him."
                    harold "BLAST! That's scalding! Why am I always suffering for other people's screw ups! Get out of here, I'll call one of the officers!"
                    angelica "(Aha! He's not working alone! That's enough for me.)"
                    angelica "You think hot tea is the worst that's in store for you?"
                    angelica "(Maybe I should check the commissioner's office for more information.)"
                    "You leave the room."
                    play sound "sounds/Door_Close.ogg"
                    hide harold hanimation
                    with dissolve
                    jump chiefsoffice
                    
        "Well, aren't you charming. Here.":
                    "Angelica spills hot tea on his lap."
                    harold "BLAST! That's scalding!"
                    angelica "Oh, I am terribly sorry. How clumsy of me, how dreadful for you!"
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
                    angelica "(The Chief was right. He's not working alone. And he isn't the leader...)"
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
                    "You leave the room."
                    play sound "sounds/Door_Close.ogg"
                    hide harold hanimation
                    with dissolve
                    jump chiefsoffice

label chiefsoffice:
    show bg policeCaptainsOffice
    stop music
    play music "sounds/Busy_Music.ogg" loop
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
    show bg party
    stop music
    play music "sounds/gameover.ogg"
    angelica "(This is the fanciest event I've ever been to. Thankfully, I have a fancy dress to match. Let's see if I can blend in with high society long enough to find the would-be killer's wife?)"
    angelica "(There's a woman in the corner, by herself. Everyone's ignoring her. I wonder if that's Mrs. Fredrickson?)"
    "A woman enters"
    "Woman: It's unbecoming to stare, my dear."
    angelica "I'm sure I don't know what you mean."
    show countess countanimation
    with dissolve
    countess "You're staring at that woman in the corner, dear. It is most unbecoming."
    countess "Quite improper."
    menu:
        "I assure you that was not my intention.":
            countess "Who cares what you intended, my dear? Our actions speak louder than words."
            countess "A girl ought to be careful not to offend her betters. You might end up like the woman you're staring at, and who wants that?"
            countess "But I'm sure you're just curious, dear?"
            countess "I'll tell you why no one's speaking to her if you'll stop making a scene with your incessant staring."
            menu:
                "I don't particularly care to hear your idle prattle.":
                    countess "Here's a lesson, little girl: lords and ladies might hold the key to your marriage prospects, so treat them well as though your life depends on it!"
                    countess "But perhaps you don't care about those things. Go talk to Mrs. Fredrickson, then-- you should find yourself quite comfortable amongst her and her ilk."
                    angelica "Perhaps I shall show her some better company."
                    hide countess countanimation
                    with dissolve
                    jump ladyFredrickson
                "Please, My Lady, do share your wisdom with me.":
                    countess "That's Mrs. Fredrickson hiding in the corner over there. The poor dear--her husband is the member of parliament who tried to kill the Queen."
                    countess "And she still has the gall to come here tonight and expect to be treated like every other parliament member's wife!"
                    countess "Perhaps she's just naive. Either way, I hope she's learned her lesson now. People like her don't mingle with people like me."
                    countess "Not anymore."
                    menu:
                        "My my, even ladies can act like scoundrels, can't they?":
                            jump worldthisway
                        "Truly, her decisions seem ill-advised.":
                            countess "Truly. The poor dear doesn't realize her society life is over. But you, little girl, you know how the world works."
                            countess "Do you know what would be quite fun, girl? You ought to go talk to her. I confess, I'd like to know what on earth she was thinking by coming here tonight. But someone of my stature talking to someone like her... it would be most unbecoming."
                            menu:
                                "You love to tell terrible tales, don't you?":
                                    jump worldthisway
                                "I could converse with her, perhaps.":
                                    hide countess countanimation
                                    with dissolve
                                    jump ladyFredrickson
                    label worldthisway:
                        countess "I didn't make the world this way, darling, that's just the way things are. I'm sure you'll learn that soon."
                        "Countess leaves."
                        hide countess countanimation
                        with dissolve
                        angelica "(What a dreadful woman! Shall I look for better company?)"
                        jump ladyFredrickson
                            
        "One might think many things are improper. Chastising strangers, for instance.":
            countess "You naive little girl! You are truly unaware of who I am? I am Lydia, Countess of Worthington, my dear.../ you ought to put it to memory."
            countess "People like me, dear, are best treated with deference. Doe-eyed little girls like you owe a great deal to ladies like me. Here's a lesson, little girl: lords and ladies might hold the key to your marriage prospects, so treat them well as though your life depends on it!"
            menu:
                "I'll keep that in mind for moments when life seems too dull. ":
                    "Go talk to Mrs. Fredrickson, then-- you should find yourself quite comfortable amongst her and her ilk."
                    angelica "Perhaps I shall show her some better company."
                    hide countess countanimation
                    jump ladyFredrickson
                    
                "Forgive my rudeness. Share your wisdom with me, my Lady.":
                    show countess countanimation
                    with dissolve
                    countess "That's Mrs. Fredrickson hiding in the corner over there. The poor dear--her husband is the member of parliament who tried to kill the Queen."
                    countess "And she still has the gall to come here tonight and expect to be treated like every other parliament member's wife!"
                    countess "Perhaps she's just naive. Either way, I hope she's learned her lesson now. People like her don't mingle with people like me."
                    countess "Not anymore."
                    menu:
                        "My my, even ladies can act like scoundrels, can't they?":
                            countess "I didn't make the world this way, darling, that's just the way things are. I'm sure you'll learn that soon."
                            hide countess countanimation
                            "Countess leaves"
                            angelica "(What a dreadful woman! Shall I look for better company?)"
                            jump ladyFredrickson
                        "Truly, her decisions seem ill-advised.":
                            countess "Truly. The poor dear doesn't realize her society life is over. But you, little girl, you know how the world works."
                            countess "Do you know what would be quite fun, girl? You ought to go talk to her. I confess, I'd like to know what on earth she was thinking by coming here tonight. But someone of my stature talking to someone like her... it would be most unbecoming."
                            menu:
                                "You love to tell terrible tales, don't you?":
                                    countess "I didn't make the world this way, darling, that's just the way things are. I'm sure you'll learn that soon."
                                    "Countess leaves"
                                    hide countess countanimation
                                    jump ladyFredrickson
                                "I could converse with her, perhaps.":
                                    hide countess countanimation
                                    jump ladyFredrickson

label ladyFredrickson:
    show beat banimation
    menu:
        "Lady Fredrickson, what on earth are you doing here?":
            
            beat "Are you here to tell me how ashamed I should be of my husband? How I should hide my face in public? How I should be embarrased to simply exist?"
            menu:
                "Of course not, I simply wished to know why you would put up with these judgmental society louses.":
                    beat "Forgive my skepticism, then, as I just saw you speaking with the Countess. I cannot imagine the woman said anything complementary about me. She is notoriously obsessed with reputation."
                    menu:
                        "She did seem to be one for idle gossip and foolishness.":
                            beat "The countess is an woman of great reputation, but I'm afraid it doesn't mean much for her moral character. I had hoped she might show a speck of kindness to me, after what I have been through. It is hard enough to lose one's husband, but perhaps it is even worse to lose one's friends."
                            angelica "Good friends are hard to come by, but they are the finest things in life."
                            jump morethanafriend
                        "I won't pretend she didn't prattle like a madwoman about you.":
                            beat "Yes, and I'm sure my misfortunes were quite amusing to you. Almost as good as the tabloids, yes? How lovely of you to show an interest in my suffering."
                            angelica "I didn't mean to offend, Lady Fredrickson!"
                            angelica "Your strength in these times is truly admirable. "
                            beat "I appreciate your kindness. Few have shown it to me tonight. It is unfortunate that our fates are so tied with those of our husbands; we put on a ring and lose our individual selves."
                            angelica "A true tragedy. It seems you have need of more loyal friends than those who've abandoned you."
                            jump morethanafriend
                    label morethanafriend:
                        beat "I could use more than a friend. I could use a new husband."
                        beat "I pray that the Queen will execute him so that I might become a widow and remarry."
                        beat "But I shouldn't say such things."
                        beat "But I'm sure a young lady like you doesn't care to hear the musings of a lonely wife."
                        angelica "On the contrary, I quite love your musings."
                        angelica "Still, a new husband, a new scoundrel. Wouldn't it be better to find companionship in a true equal?"
                        angelica "More like you and I?"
                        jump findyou
                "Maybe you should learn to be a better judge of character.":
                    beat "I had no idea what my husband intended. I accepted his hand in marriage because my parents thought it advantageous. I am not a killer simply because I was near one, no more than you are a countess because you were talking to one just a moment ago."
                    angelica "I spoke out of turn, my apologies."
                    beat "I'm a person, a person distinct from my husband. No one seems to remember that."
                    angelica "Marriage means the death of our independent lives. But perhaps now you can return to that life, and find comfort in your companions and friends."
                    beat "I see now that my old \"friends\" were not true ones. It is difficult enough to accept the loss of one's husband, but without friends..."
                    beat "I find no comfort in anyone. I find myself quite alone."
                    angelica "I've been told, in passing, I can be a great source of comfort."
            label findyou:
                beat "I know there have been rumors about my... impropriety... in the past."
                beat "I can assure you that true ladies are never more than friends with one another."
                beat "That said, I am not opposed to recieving ladies in my parlor. Perhaps, if you feel as unwelcome at this party as I do, you might retire with me."
                angelica "(Perhaps Lady Fredrickson's 'impropriety' isn't so long past?)"
                angelica "(While not entirely sanctioned by my mission, her invitation is far too... tempting an opportunity. To look into Lord Fredrickson's house, of course!)"
                angelica "Once this party becomes too much for my conscience, I'll be sure to come find you!"
        "A lady as lovely as you shouldn't be left alone.":
            beat "I appreciate your kindness. Few have shown it to me tonight. It is unfortunate that our fates are so tied with those of our husbands; we put on a ring and lose our individual selves."
            angelica "A true tragedy. It seems you have need of more loyal friends than those who've abandoned you."
            jump morethanafriend

return