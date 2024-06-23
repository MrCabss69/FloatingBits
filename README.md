
# FloatingBits

## Descripción

La biblioteca `FloatingBits` ofrece una implementación robusta para la manipulación y operación de números en formatos de punto fijo y coma flotante. Provee soporte para operaciones básicas en números representados en binario con complemento a uno, complemento a dos, y el estándar IEEE754, permitiendo realizar cálculos precisos y controlados con representaciones de punto fijo y flotante.

## Características

- **Soporte para formatos de coma fija y coma flotante**: Permite la representación y operaciones en números negativos utilizando formatos como el complemento a uno, complemento a dos, y el estándar IEEE754.
- **Operaciones Binarias en diferentes formatos**: Incluye suma, resta, y conversión de binario a decimal y viceversa.
- **Representación en decimal, binario, y hexadecimal; conversiones simplificadas**

## Instalación

Este proyecto no está empaquetado para distribución, por lo que se recomienda clonar directamente desde el repositorio de código fuente:

```bash
git clone https://your-repository-url.git
```

## Uso

### Creación de Instancias de Números

Para trabajar con números en formatos de punto fijo o flotante, primero debe crear una instancia de la clase correspondiente. Aquí están los pasos básicos:

```python
from floatingbits.fixed_point import Pure, C1, C2

# Crear un número en formato C1
number = C1(bits_left=3, bits_right=2, number_representation='01010')

# Obtener el valor decimal del número
print(number.get_value())

# Sumar dos números
other_number = C1(bits_left=3, bits_right=2, number_representation='00101')
result, overflow = number.add_(number, other_number)
print("Resultado: ", result, "Overflow: ", overflow)
```

### Pruebas

Para ejecutar las pruebas unitarias:

```bash
python -m unittest discover -v
```