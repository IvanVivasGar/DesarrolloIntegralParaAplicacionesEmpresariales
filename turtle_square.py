import turtle

windows = turtle.Screen()
tortuga = turtle.Turtle()
tortuga.speed(10)
tortuga.color("orange")
tortuga.left(180) #Girar el cursor para que vea hacia arriba

#Funcion para dibujar un cuadrado
def dibujar_cuadrado():
    for i in range(4):
        tortuga.forward(100)
        tortuga.right(90)

#Funcion para dibujar un pentagono
def dibujar_pentagono():
    for i in range(5):
        tortuga.forward(100)
        tortuga.right(72)

#Funcion para dibujar un triangulo
def dibujar_triangulo():
    for i in range(3):
        tortuga.forward(100)
        tortuga.right(120)

dibujar_cuadrado()
dibujar_pentagono()
dibujar_triangulo()

#Codigo para levantar el lapiz
tortuga.penup()
tortuga.forward(250)
tortuga.pendown()

#Funcion For para cambiar el angulo del cuadrado
for i in range(3):
    tortuga.right(22.5)
    dibujar_cuadrado()

windows.mainloop()