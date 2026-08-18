"""
Ejercicio 4 - Infraestructuras Paralelas y Distribuidas
Proyecto Python de ejemplo para construir un pipeline CI/CD.
"""


class Calculadora:
    """
    Operaciones aritméticas básicas.
    Esta clase ya está implementada — sirve como referencia del proyecto.
    """

    def suma(self, a, b):
        return a + b

    def resta(self, a, b):
        return a - b

    def multiplicacion(self, a, b):
        return a * b

    def division(self, a, b):
        if b == 0:
            raise ZeroDivisionError("No se puede dividir entre cero")
        return a / b


class ConvertidorTemperatura:
    """
    Conversor de temperaturas entre escalas Celsius, Fahrenheit y Kelvin.

    TODO: Implementa cada método según las fórmulas indicadas en los comentarios.
          Los métodos actualmente lanzan NotImplementedError y harán fallar las pruebas.
    """

    def celsius_to_fahrenheit(self, celsius):
        # TODO: Implementar
        # Fórmula: F = C × 9/5 + 32
        raise NotImplementedError("Implementar celsius_to_fahrenheit")

    def fahrenheit_to_celsius(self, fahrenheit):
        # TODO: Implementar
        # Fórmula: C = (F − 32) × 5/9
        raise NotImplementedError("Implementar fahrenheit_to_celsius")

    def celsius_to_kelvin(self, celsius):
        # TODO: Implementar
        # Fórmula: K = C + 273.15
        raise NotImplementedError("Implementar celsius_to_kelvin")

    def kelvin_to_celsius(self, kelvin):
        # TODO: Implementar
        # Fórmula: C = K − 273.15
        # Precondición: kelvin >= 0
        raise NotImplementedError("Implementar kelvin_to_celsius")


if __name__ == "__main__":
    calc = Calculadora()
    print("=== Calculadora ===")
    print("Suma:", calc.suma(5, 3))
    print("Resta:", calc.resta(5, 3))
    print("Multiplicación:", calc.multiplicacion(5, 3))
    print("División:", calc.division(5, 3))

    print("\n=== Convertidor de Temperatura ===")
    conv = ConvertidorTemperatura()
    print("0°C =", conv.celsius_to_fahrenheit(0), "°F")
    print("100°C =", conv.celsius_to_fahrenheit(100), "°F")
    print("0°C =", conv.celsius_to_kelvin(0), "K")
