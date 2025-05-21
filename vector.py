import math
""" clase Vector2
    Representa un vector en 2D con operaciones básicas como suma, resta, multiplicación,"""
class Vector2(object):
    """ metodo constructor de la clase Vector2.
        Inicializa las coordenadas x e y del vector y establece un umbral para comparaciones.
        Args:
            x (float, opcional): Coordenada x del vector. Por defecto es 0.
            y (float, opcional): Coordenada y del vector. Por defecto es 0.
        atributos:
            x (float): Coordenada x del vector.
            y (float): Coordenada y del vector.
            thresh (float): Umbral para comparaciones de igualdad."""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.thresh = 0.000001
    """metodo __add de la clase Vector2.
        Suma dos vectores y devuelve un nuevo vector resultante.
        Args:
            other (Vector2): Otro vector a sumar.
        Returns:
            Vector2: Nuevo vector resultante de la suma."""
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    """metodo __sub de la clase Vector2.
        Resta dos vectores y devuelve un nuevo vector resultante.
        Args:
            other (Vector2): Otro vector a restar.
        Returns:
            Vector2: Nuevo vector resultante de la resta."""
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    """metodo __neg de la clase Vector2.
        Negación del vector, devuelve un nuevo vector con las coordenadas opuestas.
        Returns:
            Vector2: Nuevo vector con las coordenadas opuestas."""
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    """metodo __mul de la clase Vector2.
        Multiplica el vector por un escalar y devuelve un nuevo vector resultante.
        Args:
            scalar (float): Escalar por el cual multiplicar el vector.
        Returns:
            Vector2: Nuevo vector resultante de la multiplicación."""
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    """ metodo _div de la clase Vector2.
        Divide el vector por un escalar y devuelve un nuevo vector resultante.
        Args:
            scalar (float): Escalar por el cual dividir el vector.
        Returns:
            Vector2: Nuevo vector resultante de la división."""
    def __div__(self, scalar):
        if scalar != 0:
            return Vector2(self.x / float(scalar), self.y / float(scalar))
        return None
    """ metodo __truediv de la clase Vector2.
        Divide el vector por un escalar y devuelve un nuevo vector resultante.
        Args:
            scalar (float): Escalar por el cual dividir el vector.
        Returns:
            Vector2: Nuevo vector resultante de la división."""
    def __truediv__(self, scalar):
        return self.__div__(scalar)
    """ metodo eq de la clase Vector2.
        Compara dos vectores y devuelve True si son iguales dentro de un umbral especificado.
        Args:
            other (Vector2): Otro vector a comparar.
        Returns:
            bool: True si los vectores son iguales dentro del umbral, False en caso contrario."""
    def __eq__(self, other):
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
        return False
    """ metodo magnitudeSquared de la clase Vector2.
        Calcula el cuadrado de la magnitud del vector.
        Returns:
            float: Cuadrado de la magnitud del vector."""
    def magnitudeSquared(self):
        return self.x**2 + self.y**2
    """ metodo magnitude de la clase Vector2.
        Calcula la magnitud del vector.
        Returns:
            float: Magnitud del vector."""
    def magnitude(self):
        return math.sqrt(self.magnitudeSquared())
    """ metodo copy de la clase Vector2.
        Crea una copia del vector y devuelve un nuevo objeto Vector2.
        Returns:
            Vector2: Nueva instancia de Vector2 con las mismas coordenadas."""
    def copy(self):
        return Vector2(self.x, self.y)
    """ metodo asTuple de la clase Vector2.
        Devuelve las coordenadas del vector como una tupla.
        Returns:
            tuple: Tupla con las coordenadas (x, y) del vector."""
    def asTuple(self):
        return self.x, self.y
    """ metodo asInt de la clase Vector2.
        Devuelve las coordenadas del vector como una tupla de enteros.
        Returns:
            tuple: Tupla con las coordenadas (x, y) del vector convertidas a enteros."""
    def asInt(self):
        return int(self.x), int(self.y)
    """ metodo __str__ de la clase Vector2.
        Devuelve una representación en cadena del vector.
        Returns:
            str: Representación en cadena del vector en formato "<x, y>"."""
    def __str__(self):
        return "<"+str(self.x)+", "+str(self.y)+">"