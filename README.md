# Pipelines CI/CD con GitHub Actions

Infraestructuras Paralelas y Distribuidas
Escuela de Ingeniería de Sistemas y Computación, Universidad del Valle
Carlos Andrés Delgado Saavedra

Lo que cada parte necesita de las bibliotecas y herramientas está en
[DOCUMENTACION.md](DOCUMENTACION.md), con ejemplos que corren y los enlaces
a la documentación oficial.

Un pipeline de integración continua ejecuta las pruebas cada vez que alguien
sube código, sin que nadie se acuerde de correrlas. Este ejercicio pide
implementar unas funciones pendientes y montar el pipeline que las verifica.

## Estructura del proyecto

```
.
├── src/
│   └── main.py              Calculadora (completa) y ConvertidorTemperatura (pendiente)
├── tests/
│   ├── test_main.py         pruebas de Calculadora, ya pasan
│   └── test_converter.py    pruebas de ConvertidorTemperatura, fallan hasta implementarlas
├── requirements.txt
└── .github/workflows/
    ├── pruebas.yml          verificación del ejercicio
    └── ci.yml               el que hay que escribir
```

## Ejecutar en la máquina propia

```bash
pip install -r requirements.txt
python src/main.py
python -m pytest tests/ -v
```

## Tarea 1: implementar `ConvertidorTemperatura`

En `src/main.py` los cuatro métodos de la clase levantan `NotImplementedError`:

| Método | Fórmula |
|---|---|
| `celsius_to_fahrenheit(celsius)` | F = C × 9/5 + 32 |
| `fahrenheit_to_celsius(fahrenheit)` | C = (F − 32) × 5/9 |
| `celsius_to_kelvin(celsius)` | K = C + 273.15 |
| `kelvin_to_celsius(kelvin)` | C = K − 273.15 |

Antes de subir nada:

```bash
python -m pytest tests/test_converter.py -v
```

## Tarea 2: escribir `.github/workflows/ci.yml`

El archivo se crea en la máquina y se sube con `git push`; Actions lo detecta
al encontrarlo en esa carpeta.

```bash
mkdir -p .github/workflows
git add .github/workflows/ci.yml
git commit -m "Agrega el pipeline de integración continua"
git push
```

El pipeline debe dispararse en cada `push`, correr sobre `ubuntu-latest`,
configurar Python 3.11, instalar las dependencias y ejecutar las pruebas.
Este esqueleto sirve de punto de partida:

```yaml
name: CI Pipeline
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Instalar dependencias
        run: pip install -r requirements.txt
      - name: Ejecutar pruebas
        run: python -m pytest tests/ -v
```

Se puede adaptar. Lo que importa es que exista, que tenga `jobs:` y `steps:`,
y que las pruebas queden en verde.

## Qué se revisa

- Pasan las pruebas de `Calculadora`.
- Pasan las pruebas de `ConvertidorTemperatura`.
- Existe `.github/workflows/ci.yml`.
- El workflow tiene `jobs:` y `steps:`.

## Qué mirar del pipeline

El disparador `on: [push]` es lo que convierte el repositorio en algo que se
prueba solo. `runs-on: ubuntu-latest` levanta una máquina limpia cada vez, así
que si algo funciona en el equipo propio y falla aquí, lo que falta es una
dependencia declarada. Y las acciones que se reutilizan, como
`actions/checkout` o `actions/setup-python`, evitan escribir a mano lo que ya
está resuelto.

## Integridad académica

Se puede consultar el material de clase, la documentación de GitHub Actions y
recursos en línea. Si se usa un asistente automático, hay que declararlo en el
commit indicando qué se generó con él y qué se implementó a mano. Copiar la
solución de otro estudiante, o compartir la propia, no es una opción.
