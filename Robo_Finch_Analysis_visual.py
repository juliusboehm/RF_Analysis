from shapely.geometry import Polygon, Point, LineString                 #Erstellung der verschiedenen geometrischen Körper
from shapely.plotting import plot_line, plot_points, plot_polygon       #Darstellung der Körper zum Testen 
import matplotlib.pyplot as plt                                         # "
import math                                                             #Berechnung von Wurzeln/Sinus etc.

#----------------------------------------------------------------------
#ONLY PROBLEM: The Code will not Work, if the Coordinates of Head and Beak are identical
#Die Warscheinlichkeit dafür ist wegen der hohen Anzahl an Nachkommastellen aber so klein, das das vorerst 
#in Kauf genommen wird
#----------------------------------------------------------------------

def get_lin_func_from_points(A, B):#Funktion die Steigung und y-Achsen-Abschnitt einer lin. Funktion aus zwei Punten berechnet
    dy = B.y - A.y
    dx = B.x - A.x

    loc_m = dy/dx
    loc_b = A.y - (loc_m * A.x)

    return(loc_m, loc_b)    #loc_m = Steigung, loc_b = y-Achsen-Abschnitt

def get_lin_func_from_point_steigung(A, m): #Funktion die Steigung und y-A-A ausgibt, aber aus Punkt und Steigung berechnet
    loc_b = A.y - (m * A.x)

    return(m, loc_b)

def get_point_triangle(d, x1, m, b):        #Funktion die den Startpunkt zur Erstellung des Dreiecks erstellt, von dem aus die Eckpunkte berechnet werden (liegt genau in der Mitte)
    xpos = x1 + (math.sqrt((d**2)/(1+(m**2))))
    xneg = x1 - (math.sqrt((d**2)/(1+(m**2))))

    ypos = (m * xpos) + b
    yneg = (m * xneg) + b

    return(xpos, ypos, xneg, yneg)

#-------------------------------------------------------------------------------------------------------

#-------Points-------------------
Head = Point(801.22705078125,428.33880615234375)               #Test Punkte
Beak = Point(825.8939208984375,452.4085083007813)
RF = Point(200,200)

#------Distance_toter_Winkel-----
T = 1000                          #Entfernung, in dem das Dreieck gebildet wird

HB = LineString([(Head.x, Head.y), (Beak.x, Beak.y)])       #Verbindung zwischen Head und Beak

#--------------------------------------------------------------------------------------------------------

if Head.x == Beak.x:      # Außnahme 1: Paralell zur y-Achse
    x_par_d = (math.sqrt((T**2)/(1+(0**2))))
    d_from_start = (T/math.sin(math.radians(60)))/2
    tr_up_start = Point(Head.x, (Head.y + T))
    tr_dwn_start = Point(Head.x, (Head.y - T))

    if Head.y > Beak.y:
        corner1 = Point((tr_up_start.x + d_from_start), (Head.y + x_par_d))
        corner2 = Point((tr_up_start.x - d_from_start), (Head.y + x_par_d))
    
    if Head.y < Beak.y:
        corner1 = Point((tr_dwn_start.x + d_from_start), (Head.y - x_par_d))
        corner2 = Point((tr_dwn_start.x - d_from_start), (Head.y - x_par_d))

    triangle = Polygon([(Head.x, Head.y), (corner1.x, corner1.y), (corner2.x, corner2.y)])

elif Head.y == Beak.y:      # Ausnahme 2: Parallel zur x-Achse      # überhaupt nötig???
    y_par_d = (math.sqrt((T**2)/(1+(0**2))))
    d_from_start = (T/math.sin(math.radians(60)))/2
    tr_left_start = Point((Head.x - T), Head.y)
    tr_right_start = Point((Head.x + T), Head.y)

    if Head.x > Beak.x:
        corner1 = Point((Head.x + y_par_d), (tr_left_start.y + d_from_start))
        corner2 = Point((Head.x + y_par_d), (tr_left_start.y - d_from_start))
    
    if Head.x < Beak.x:
        corner1 = Point((Head.x - y_par_d), (tr_right_start.y + d_from_start))
        corner2 = Point((Head.x - y_par_d), (tr_right_start.y - d_from_start))

    triangle = Polygon([(Head.x, Head.y), (corner1.x, corner1.y), (corner2.x, corner2.y)])

else:
    #----------Bird--------------
    m_HB = get_lin_func_from_points(Head,Beak)[0]
    b_HB = get_lin_func_from_points(Head,Beak)[1]

    #----------Triangle-Points---------
    tr_pos = Point(get_point_triangle(T,Head.x,m_HB,b_HB)[0], get_point_triangle(T,Head.x,m_HB,b_HB)[1])
    tr_neg = Point(get_point_triangle(T,Head.x,m_HB,b_HB)[2], get_point_triangle(T,Head.x,m_HB,b_HB)[3])

    #---------Senkrechte---------------------------
    senk_d = (T/math.sin(math.radians(60)))/2
    senk_m = ((1/(m_HB)*-1))

    #----------or,ur,lo,lu--------------------------
    if Head.x > Beak.x:
        senk_x1 = tr_pos.x
        senk_b = get_lin_func_from_point_steigung(tr_pos, senk_m)[1]

    elif Head.x < Beak.x:
        senk_x1 = tr_neg.x
        senk_b = get_lin_func_from_point_steigung(tr_neg, senk_m)[1]
    #------------------------------------------------

    corners = get_point_triangle(senk_d, senk_x1, senk_m, senk_b)

    corner1 = Point(corners[0], corners[1])
    corner2 = Point(corners[2], corners[3])

    triangle = Polygon([(Head.x, Head.y), (corner1.x, corner1.y), (corner2.x, corner2.y)])

###################################################
plot_polygon(triangle, color="y")
plot_line(HB)
plot_points(RF)

print(triangle.contains(RF))

plt.show()

###################################################