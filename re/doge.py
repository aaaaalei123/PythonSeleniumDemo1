from turtle import *

#setup
screensize(500,500)
pensize(5)
seth(0)
speed(10)
color('black')
fillcolor('green')

#face
pd()
fd(25)
circle(100,90)
circle(120,90)
fd(10)
circle(120,90)
circle(100,90)
fd(25)
pu()

#eyes
goto(10,100)
pd()
fd(50)
circle(15,180)
fd(50)
circle(15,180)
pu()

goto(60,100)
begin_fill()
circle(17)
end_fill()

goto(-100,100)
pd()
fd(50)
circle(15,180)
fd(50)
circle(15,180)
pu()

goto(-50,100)
begin_fill()
circle(17)
end_fill()

#mouth
goto(-60,50)
pd()
seth(340)
circle(30,100)
seth(180)
fd(20)
seth(280)
circle(30,120)
pu()

#ears
goto(60,212)
pd()
seth(60)
circle(-80,50)
circle(-5,90)
circle(-150,35)
pu()

goto(-60,212)
pd()
seth(110)
circle(80,40)
seth(270)
fd(69)
pu()

#heart
goto(0,-100)
size=90
pd()
seth(150)
fd(size)
circle(-337, 45)
circle(-129, 165)
left(120)
circle(-129, 165)
circle(-337, 45)
fd(size)
pu()

#Words
goto(-260,80)
write("I Love THU!\n\n", align="right", font=("MS UI Gothic",20,"bold"))
goto(-220,-100)
write("EESAST the best!\n\n", align="right", font=("华文隶书",20,"bold"))
goto(460,-110)
write("Coding makes me happy!\n\n", align="right", font=("楷体", 16, "bold"))
goto(460,110)
write("Give me an npy!\n\n", align="right", font=("Tempus Sans ITC", 16, "bold"))

#goodbye
hideturtle()
done()