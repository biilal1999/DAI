import random


def pintarSVG (formas, colores):
    forma = random.choice(formas)
    color = random.choice(colores)
    print(forma)
    print(color)
    
    cadena = '<svg width=200 height=200>'

    
    if forma == 'circle':
        cx = random.randint(50, 170)
        cy = random.randint(50, 170)
        r = random.randint(30, 100)

        cadena += '<circle cx=' + str(cx) + ' cy=' + str(cy) + ' r=' + str(r) + ' fill=' + color + ' /></svg>'

    
    elif forma == 'ellipse':
        cx = random.randint(50, 170)
        cy = random.randint(50, 170)
        rx = random.randint(30, 100)
        ry = random.randint(30, 100)

        cadena += '<ellipse cx=' + str(cx) + ' cy=' + str(cy) + ' rx=' + str(rx) + ' ry=' + str(ry) + ' fill=' + color + ' /></svg>'


    elif forma == 'line':
        x1 = random.randint(0, 10)
        y1 = random.randint(0, 10)
        x2 = random.randint(130, 230)
        y2 = random.randint(130, 230)
        strowi = random.randint(0, 5)

        cadena += '<line x1=' + str(x1) + ' y1=' + str(y1) + ' x2=' + str(x2) + ' y2=' + str(y2) + ' stroke=' + color + ' stroke-width=' + str(strowi) + ' /></svg>'


    return cadena
