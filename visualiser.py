import pygame, sys, math
pygame.init()

### Colours ###
colours = {
    "BG" : (33, 33, 33),
    "Dots" : (240, 235, 238),
    "Line" : (156, 160, 163),
    "Grid" : (66, 66, 66),
    "Width" : (80, 80, 255),
    "Height" : (240, 80, 80),
    "Hypotenuse" : (80, 240, 80),
    "Angle" : (180, 40, 180)
    }

### Functions ###
def drawGrid(screen, screenDimens, step=20):
    # Horizontal lines
    for row in range(0, screenDimens[1] + step, step):
        pygame.draw.line(screen, colours["Grid"], (0, row), (screenDimens[0], row))
        
    # Vertical lines
    for col in range(0, screenDimens[0] + step, step):
        pygame.draw.line(screen, colours["Grid"], (col, 0), (col, screenDimens[1]))

def createTextRect(text, size, type, pos, colour):
    # Surface creation
    font = pygame.font.SysFont('freesansbold.ttf', size)
    img = font.render(text, True, colour)
    rect = img.get_rect()

    # Positioning - info & labels
    if type == 'topleft':
        rect.topleft = pos[0] + 1, pos[1] + 1
    elif type == 'hypright':
        rect.bottomleft = pos[0] + 3, pos[1]
    elif type == 'hypleft':
        rect.topright = pos[0] - 3, pos[1]
    elif type == 'bottomcentre':
        rect.centerx, rect.top = pos[0], pos[1] + 1
    elif type == 'topcentre':
        rect.centerx, rect.bottom = pos[0], pos[1] - 1
    elif type == 'centreright':
        rect.right, rect.centery = pos[0] - 2, pos[1]
    elif type == 'centreleft':
        rect.left, rect.centery = pos[0] + 2, pos[1]
    
    return img, rect

def drawDots(screen, centre, pos, colour, radius=5.0):
    pygame.draw.circle(screen, colour, centre, radius)
    pygame.draw.circle(screen, colour, pos, radius)
    pygame.draw.circle(screen, colour, (pos[0], centre[1]), radius)

def getTrigInfo(centre, pos):
    # Calculate width, height, hypotenuse length, and angle (degrees & radians)
    width = pos[0] - centre[0]
    height = pos[1] - centre[1]
    hyp = math.sqrt(width**2 + height**2)

    try:
        # Calculate angles
        radians = math.atan(width / height)
        deg = (radians / (2 * math.pi)) * 360
        
        # Quadrant handling
        if (width > 0 and height > 0) or (width < 0 and height < 0):
            angle = 90 - deg
        else:
            angle = 90 + deg
    except ZeroDivisionError:
        angle = 0
        radians = 0
        
    return width, height, hyp, angle, radians

def drawTriangle(screen, centre, pos, width=2):
    # Get info about the triangle
    w, h, _, _, radians = getTrigInfo(centre, pos)

    # Handle label placement & arc angle setup
    fontSize = 25
    rad = (abs(w) + abs(h)) / 6
    sqLength = min([abs(w), abs(h)]) / 6

    # Right
    if w > 0:
        # Lower
        if h > 0:
            # Text objects
            wText, wRect = createTextRect("Width", fontSize, 'topcentre', (centre[0] + w // 2, centre[1]), colours["Width"])
            hText, hRect = createTextRect("Height",  fontSize, 'centreleft', (centre[0] + w, centre[1] + h // 2), colours["Height"])
            hypText, hypRect = createTextRect("Hypotenuse",  fontSize, 'hypleft', (centre[0] + w // 2, centre[1] + h // 2), colours["Hypotenuse"])
            
            # Angles
            startAngle = 2*math.pi - (math.pi/2 - radians)
            endAngle = 0
            pygame.draw.arc(screen, colours["Angle"], (centre[0] - rad/2, centre[1] - rad/2, rad, rad), startAngle, endAngle, width)
            
            # Right-angle square
            pygame.draw.line(screen, colours["Line"], (pos[0] - sqLength, centre[1]), (pos[0] - sqLength, centre[1] + sqLength), width)
            pygame.draw.line(screen, colours["Line"], (pos[0] - sqLength, centre[1] + sqLength), (pos[0], centre[1] + sqLength), width)
    
        # Upper
        else:
            # Text objects
            wText, wRect = createTextRect("Width",  fontSize, 'bottomcentre', (centre[0] + w // 2, centre[1]), colours["Width"])
            hText, hRect = createTextRect("Height",  fontSize, 'centreleft', (centre[0] + w, centre[1] + h // 2), colours["Height"])
            hypText, hypRect = createTextRect("Hypotenuse",  fontSize, 'hypleft', (centre[0] + w // 2, centre[1] + h // 2 - 20), colours["Hypotenuse"])
            
            # Angles
            startAngle = 0
            endAngle = math.pi - (math.pi/2 - radians)
            pygame.draw.arc(screen, colours["Angle"], (centre[0] - rad/2, centre[1] - rad/2, rad, rad), startAngle, endAngle, width)
            
            # Right-angle square
            pygame.draw.line(screen, colours["Line"], (pos[0] - sqLength, centre[1] - sqLength), (pos[0] - sqLength, centre[1]), width)
            pygame.draw.line(screen, colours["Line"], (pos[0] - sqLength, centre[1] - sqLength), (pos[0], centre[1] - sqLength), width)
    
    # Left
    else:
        # Lower
        if h > 0:
            # Text objects
            wText, wRect = createTextRect("Width",  fontSize, 'topcentre', (centre[0] + w // 2, centre[1]), colours["Width"])
            hText, hRect = createTextRect("Height",  fontSize, 'centreright', (centre[0] + w, centre[1] + h // 2), colours["Height"])
            hypText, hypRect = createTextRect("Hypotenuse",  fontSize, 'hypright', (centre[0] + w // 2, centre[1] + h // 2 + 20), colours["Hypotenuse"])
            
            # Angles
            startAngle = math.pi
            endAngle = 2*math.pi - (math.pi/2 - radians)
            pygame.draw.arc(screen, colours["Angle"], (centre[0] - rad/2, centre[1] - rad/2, rad, rad), startAngle, endAngle, width)
            
            # Right-angle square
            pygame.draw.line(screen, colours["Line"], (pos[0] + sqLength, centre[1] + sqLength), (pos[0] + sqLength, centre[1]), width)
            pygame.draw.line(screen, colours["Line"], (pos[0], centre[1] + sqLength), (pos[0] + sqLength, centre[1] + sqLength), width)
        
        # Upper
        else:
            # Text objects
            wText, wRect = createTextRect("Width",  fontSize, 'bottomcentre', (centre[0] + w // 2, centre[1]), colours["Width"])
            hText, hRect = createTextRect("Height",  fontSize, 'centreright', (centre[0] + w, centre[1] + h // 2), colours["Height"])
            hypText, hypRect = createTextRect("Hypotenuse",  fontSize, 'hypright', (centre[0] + w // 2, centre[1] + h // 2), colours["Hypotenuse"])
            
            # Angles
            startAngle = math.pi - (math.pi/2 - radians)
            endAngle = math.pi
            pygame.draw.arc(screen, colours["Angle"], (centre[0] - rad/2, centre[1] - rad/2, rad, rad), startAngle, endAngle, width)
            
            # Right-angle square
            pygame.draw.line(screen, colours["Line"], (pos[0] + sqLength, centre[1] - sqLength), (pos[0], centre[1] - sqLength), width)
            pygame.draw.line(screen, colours["Line"], (pos[0] + sqLength, centre[1] - sqLength), (pos[0] + sqLength, centre[1]), width)

    # Draw to screen
    pygame.draw.line(screen, colours["Width"], centre, (pos[0], centre[1]), width)
    screen.blit(wText, wRect)
    pygame.draw.line(screen, colours["Height"], (pos[0], centre[1]), (pos[0], pos[1]), width)
    screen.blit(hText, hRect)
    pygame.draw.line(screen, colours["Hypotenuse"], centre, (pos), width)
    screen.blit(hypText, hypRect)

### Main program ###
def main():
    # Setup
    screenW = screenH = 800
    halfW, halfH = screenW / 2, screenH / 2
    centre = pos = halfW, halfH
    ySpace, size = 10, 30
    screen = pygame.display.set_mode((screenW, screenH))
    pygame.display.set_caption('Right-Angle Triangle Visualiser')
    clock = pygame.time.Clock()
    
    # Main loop
    while 1:
        clock.tick(30)
        screen.fill(colours["BG"])

        # Event handling
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pass
                
        pos = pygame.mouse.get_pos()
        width, height, hyp, angle, _ = getTrigInfo(centre, pos)
        widthText, widthRect = createTextRect(f"Width: {abs(int(width))}", size, 'topleft', (5, 5), colours["Width"])
        heightText, heightRect = createTextRect(f"Height: {abs(int(height))}", size, 'topleft', (5, widthRect.bottom + ySpace), colours["Height"])
        hypText, hypRect = createTextRect(f"Hypotenuse length: {abs(hyp):.1f}", size, 'topleft', (5, heightRect.bottom + ySpace), colours["Hypotenuse"])
        degText, degRect = createTextRect(f"Angle: {angle:.1f}", size, 'topleft', (5, hypRect.bottom + ySpace), colours["Angle"])
        
        # Grid
        drawGrid(screen, (screenW, screenH))
        
        try:
            # Draw whole triangle
            drawTriangle(screen, centre, pos)
            
            # Dots
            drawDots(screen, centre, pos, colours["Dots"])
            
            # Text in left corner
            screen.blit(widthText, widthRect)
            screen.blit(heightText, heightRect)
            screen.blit(hypText, hypRect)
            screen.blit(degText, degRect)
        except:
            pass

        pygame.display.update()

if __name__ == '__main__':
    main()
