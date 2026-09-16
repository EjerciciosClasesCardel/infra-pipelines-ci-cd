# Documentación de apoyo: pipelines CI/CD con GitHub Actions

Aquí está lo que hace falta para resolver el ejercicio: qué hace cada herramienta, un ejemplo que corre tal cual y los enlaces a la documentación oficial. Hay una sección por cada tarea del README, en el mismo orden y con el mismo nombre. Los ejemplos resuelven un problema vecino, no el del ejercicio: se leen, se entienden y se escribe lo propio. Los enlaces van al final de cada sección.

## Parte 1: implementar `ConvertidorTemperatura`

### Lo que se usa

- `def celsius_to_fahrenheit(self, celsius):` y los otros tres métodos de `src/main.py`. Cada uno recibe un número y devuelve otro. Hoy el cuerpo es `raise NotImplementedError(...)`; esa línea se reemplaza por el cálculo y un `return`. En Python 3 el operador `/` siempre da un flotante: `9 / 5` es `1.8`.
- `unittest.TestCase` es la clase base de las pruebas en `tests/`. `setUp(self)` corre antes de cada prueba y ahí se crea el objeto que se va a probar. `assertEqual(a, b)` compara con `==`; `assertRaises(Excepcion, funcion, *args)` verifica que la llamada lance esa excepción.
- `assertAlmostEqual(primero, segundo, places=7)` redondea la diferencia a `places` decimales y la compara con cero. Es la comparación que usan las pruebas del convertidor, porque dos flotantes que deberían ser iguales rara vez lo son bit a bit. Con `places=1` basta con que coincida el primer decimal.
- `pytest` recorre la carpeta que se le indica y recoge, sin que nadie los registre, los archivos `test_*.py` o `*_test.py`, las clases que heredan de `unittest.TestCase` y los métodos cuyo nombre empieza por `test`. Un método llamado `verificar_algo` no se ejecuta.
- `python -m pytest tests/ -v` ejecuta las pruebas. `python -m` pone el directorio actual en `sys.path`, y por eso `from src.main import ...` resuelve desde `tests/`. Opciones que sirven aquí: `-v` imprime una línea por prueba con PASSED o FAILED; `-q` resume en una línea; `-k EXPR` corre solo las pruebas cuyo nombre contiene `EXPR` (admite `and`, `or`, `not`); `-x` se detiene en el primer fallo; `--tb=short` acorta el rastro de cada fallo (`line` lo deja en una línea, `no` lo quita). Una sola prueba se corre con su identificador completo: `python -m pytest tests/test_converter.py::TestConvertidorTemperatura::test_celsius_to_kelvin_zero`.
- `python3 -m venv venv` crea un entorno virtual en la carpeta `venv/`; `source venv/bin/activate` lo activa. Así `pip` instala en el proyecto y no en el sistema. El `.gitignore` del repositorio ya excluye `venv/` y `.venv`.
- `pip install -r requirements.txt` instala lo que lista el archivo, un paquete por línea, con versión opcional (`pytest`, `pytest==9.1.1`, `pytest>=8`). Es el mismo comando que ejecuta el pipeline, así que lo que no esté ahí no existe en el runner.

### Ejemplo

Un conversor de longitudes con un método pendiente, la misma situación con que arranca el ejercicio. Tres archivos:

```
ejemplo/
├── requirements.txt         pytest
├── src/
│   ├── __init__.py          vacío
│   └── longitud.py
└── tests/
    ├── __init__.py          vacío
    └── test_longitud.py
```

`src/longitud.py`:

```python
"""Conversor de longitudes entre metros, pies, kilómetros y millas."""


class ConvertidorLongitud:

    def metros_a_pies(self, metros):
        # 1 m = 3,28084 pies
        return metros * 3.28084

    def pies_a_metros(self, pies):
        return pies / 3.28084

    def km_a_millas(self, km):
        # 1 milla = 1,609344 km
        return km / 1.609344

    def millas_a_km(self, millas):
        # Pendiente: la prueba tiene que fallar hasta escribirlo
        raise NotImplementedError("Implementar millas_a_km")


if __name__ == "__main__":
    conv = ConvertidorLongitud()
    print("100 m =", conv.metros_a_pies(100), "pies")
    print("42,195 km =", conv.km_a_millas(42.195), "millas")
```

`tests/test_longitud.py`:

```python
import unittest

from src.longitud import ConvertidorLongitud


class TestConvertidorLongitud(unittest.TestCase):

    def setUp(self):
        self.conv = ConvertidorLongitud()

    def test_metros_a_pies(self):
        self.assertAlmostEqual(self.conv.metros_a_pies(1), 3.28084)
        self.assertAlmostEqual(self.conv.metros_a_pies(0), 0.0)

    def test_pies_a_metros(self):
        # places=3: basta con que coincidan tres decimales
        self.assertAlmostEqual(self.conv.pies_a_metros(3.28084), 1.0, places=3)

    def test_km_a_millas(self):
        self.assertAlmostEqual(self.conv.km_a_millas(1.609344), 1.0)

    def test_millas_a_km(self):
        self.assertAlmostEqual(self.conv.millas_a_km(1), 1.609344)
        self.assertAlmostEqual(self.conv.millas_a_km(26.2188), 42.195, places=2)
```

Se prepara el entorno y se corren las pruebas con el método todavía pendiente:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/ -v --tb=short
```

```
collected 4 items

tests/test_longitud.py::TestConvertidorLongitud::test_km_a_millas PASSED [ 25%]
tests/test_longitud.py::TestConvertidorLongitud::test_metros_a_pies PASSED [ 50%]
tests/test_longitud.py::TestConvertidorLongitud::test_millas_a_km FAILED [ 75%]
tests/test_longitud.py::TestConvertidorLongitud::test_pies_a_metros PASSED [100%]

=================================== FAILURES ===================================
___________________ TestConvertidorLongitud.test_millas_a_km ___________________
tests/test_longitud.py:23: in test_millas_a_km
    self.assertAlmostEqual(self.conv.millas_a_km(1), 1.609344)
src/longitud.py:19: in millas_a_km
    raise NotImplementedError("Implementar millas_a_km")
E   NotImplementedError: Implementar millas_a_km
=========================== short test summary info ============================
FAILED tests/test_longitud.py::TestConvertidorLongitud::test_millas_a_km - No...
========================= 1 failed, 3 passed in 0.02s ==========================
```

El rastro dice en qué línea de la prueba falló y en qué línea del código se lanzó la excepción. Se escribe el método, dos líneas en lugar del `raise`:

```python
    def millas_a_km(self, millas):
        return millas * 1.609344
```

Y se vuelve a correr, esta vez solo las pruebas que tienen `millas` en el nombre:

```bash
python -m pytest tests/ -k millas -v
```

```
collected 4 items / 2 deselected / 2 selected

tests/test_longitud.py::TestConvertidorLongitud::test_km_a_millas PASSED [ 50%]
tests/test_longitud.py::TestConvertidorLongitud::test_millas_a_km PASSED [100%]

======================= 2 passed, 2 deselected in 0.01s ========================
```

La corrida completa, `python -m pytest tests/ -v`, termina en `4 passed in 0.01s`, y el script suelto también funciona:

```bash
python src/longitud.py
```

```
100 m = 328.084 pies
42,195 km = 26.218757456454306 millas
```

Con `-x` la corrida se detiene en el primer fallo y el resumen termina en `stopping after 1 failures`; sirve cuando se está arreglando un método a la vez.

### Lo que suele fallar

- `ModuleNotFoundError: No module named 'src'`. Aparece cuando falta `tests/__init__.py`, que el repositorio trae vacío y que en un proyecto montado desde cero suele olvidarse: sin ese archivo, `pytest tests/` a secas y `python -m pytest` desde dentro de `tests/` solo ponen `tests/` en `sys.path`, y `src` no se encuentra. Con el archivo en su sitio, pytest sube hasta la raíz del proyecto y la añade él mismo. El comando del README, `python -m pytest tests/` desde la raíz, funciona en los dos casos porque `python -m` añade el directorio actual.
- `/usr/bin/python3: No module named pytest`. El entorno virtual no está activado o `pip` instaló en otro intérprete. Con el venv activo, `which python` apunta a `venv/bin/python`; si no, `source venv/bin/activate`.
- `AssertionError: 3 != 3.28084 within 7 places (0.28084 difference)`. El cálculo usó división entera (`//`) o redondeó antes de devolver. Las fórmulas del README se escriben con `/` y se devuelve el valor tal cual sale.
- `ValueError` en `test_kelvin_to_celsius_absolute_zero`. La precondición del método es `kelvin >= 0`, y la prueba llama con `0`. Si se decide validar la entrada, el cero es válido; lo que se rechaza es lo negativo.
- Una prueba que no aparece en la corrida. Un método llamado `check_millas_a_km` en vez de `test_millas_a_km` no se recoge y el conteo baja sin ningún aviso; un archivo `pruebas_longitud.py` tampoco se recoge. El nombre del archivo empieza por `test_` y el de cada método también.

### Enlaces

- [Cómo invocar pytest](https://docs.pytest.org/en/stable/how-to/usage.html): las opciones de línea de comandos, entre ellas `-k`, `-x`, `--tb` y cómo correr una sola prueba por su identificador.
- [Convenciones de descubrimiento de pruebas](https://docs.pytest.org/en/stable/explanation/goodpractices.html): qué archivos, clases y funciones recoge pytest y cómo organizar `src/` y `tests/`.
- [pytest con pruebas de unittest](https://docs.pytest.org/en/stable/how-to/unittest.html): cómo corre pytest las clases `unittest.TestCase` que tiene este repositorio.
- [Módulo unittest](https://docs.python.org/3/library/unittest.html): `TestCase`, `setUp` y la lista completa de `assert*`, con la definición exacta de `assertAlmostEqual`.
- [Aritmética de punto flotante](https://docs.python.org/3/tutorial/floatingpoint.html): por qué `0.1 + 0.2 != 0.3` y por qué las pruebas comparan con tolerancia.
- [Entornos virtuales con venv](https://docs.python.org/3/library/venv.html) y [formato de requirements.txt](https://pip.pypa.io/en/stable/reference/requirements-file-format/): crear y activar un entorno, y la sintaxis de cada línea del archivo con sus especificadores de versión.

## Parte 2: escribir `.github/workflows/ci.yml`

### Lo que se usa

- Un workflow es un archivo YAML dentro de `.github/workflows/`. GitHub lo lee en cada evento del repositorio y decide si lo ejecuta. La indentación son espacios, nunca tabulaciones, y dos espacios por nivel es la costumbre.
- `name:` es el nombre con que el workflow aparece en la pestaña Actions. Si falta, se usa la ruta del archivo.
- `on:` declara los eventos que lo disparan. `on: [push]` corre en cada push a cualquier rama. La forma larga filtra: `push: branches: [main]` solo corre en esa rama; `pull_request:` corre cuando se abre o actualiza un pull request; `workflow_dispatch:` agrega un botón *Run workflow* en la pestaña Actions para lanzarlo a mano.
- `jobs:` es el mapa de trabajos. Cada uno tiene un identificador (`test`, `pruebas`, el que se quiera), corre en su propia máquina limpia y, salvo que se diga otra cosa, todos arrancan en paralelo.
- `runs-on: ubuntu-latest` pide una máquina virtual Ubuntu de GitHub. Trae Python, Node, Docker y git preinstalados, pero no trae el proyecto ni sus dependencias.
- `steps:` es la lista ordenada de pasos del job. Cada paso es `uses: dueño/accion@version`, que ejecuta una acción publicada, o `run: comando`, que ejecuta comandos de shell. `name:` le pone etiqueta al paso en el log. Un `run` de varias líneas se escribe con `run: |` y una línea por comando; si un comando devuelve distinto de cero, el paso falla y el job con él.
- `with:` pasa parámetros a la acción del `uses`. `env:` define variables de entorno; puesto al nivel del workflow vale para todos los jobs, al nivel de un job para sus pasos, y en un paso solo para ese. Dentro de `run` se leen como `$NOMBRE`.
- `needs: otro_job` hace que un job espere a que otro termine bien. Sin `needs` los jobs corren a la vez.
- `strategy: matrix:` repite el job una vez por cada combinación de valores. Con `python-version: ["3.11", "3.12"]` salen dos jobs, y el valor actual se lee con `${{ matrix.python-version }}`.
- `if:` en un paso o en un job lo condiciona a una expresión; `${{ }}` es la sintaxis de expresiones y dentro se accede a contextos como `matrix`, `github`, `env` o `runner`.
- `actions/checkout@v4` clona el repositorio en la máquina del job, en el commit que disparó el evento. Sin él, la máquina está vacía y `requirements.txt` no existe.
- `actions/setup-python@v5` instala la versión de Python que se pide en `with: python-version:` y la deja como `python` y `pip` en el `PATH`. Con `cache: pip` guarda lo que pip descargó, indexado por el contenido de `requirements.txt`, y lo restaura en la corrida siguiente. La versión va entre comillas.
- `$GITHUB_STEP_SUMMARY` es un archivo al que un paso puede escribir Markdown; lo que escriba sale en la página de resumen del run, debajo del grafo de jobs.
- La pestaña Actions del repositorio lista los runs, uno por evento, con el commit que lo disparó y un ícono de estado. Al entrar a un run se ven sus jobs a la izquierda y, al abrir uno, cada paso con su log desplegable; el paso que falló aparece en rojo y expandido. Desde la terminal, `gh run list` muestra los últimos runs, `gh run view <id>` el detalle por pasos, `gh run view <id> --log-failed` solo el log de lo que falló y `gh run watch` sigue en vivo el run en curso.
- El badge es una imagen que GitHub genera con el estado del último run de un workflow. La URL es `https://github.com/<usuario>/<repositorio>/actions/workflows/<archivo>.yml/badge.svg`, y en el README se pone como imagen enlazada a la página del workflow.
- `act` ejecuta un workflow en la máquina propia, dentro de Docker, con la misma sintaxis y las mismas acciones. Sirve para probar el YAML antes de hacer push; `act -l` lista los jobs y `act push` simula un push.

### Ejemplo

Un pipeline para el conversor de longitudes de la Parte 1, con dos versiones de Python, un paso condicionado y un segundo job que espera al primero. El archivo va en `.github/workflows/pruebas-longitud.yml`:

```yaml
name: Pruebas de longitud

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

env:
  PYTHONDONTWRITEBYTECODE: "1"

jobs:
  pruebas:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip

      - name: Instalar dependencias
        run: pip install -r requirements.txt

      - name: Ejecutar pruebas
        run: python -m pytest tests/ -v --tb=short

      - name: Probar el script
        if: matrix.python-version == '3.12'
        run: python src/longitud.py

  resumen:
    needs: pruebas
    runs-on: ubuntu-latest
    steps:
      - name: Escribir el resumen del run
        run: echo "Las pruebas pasaron en las dos versiones de Python." >> "$GITHUB_STEP_SUMMARY"
```

Antes de subirlo se corre en la máquina propia con `act`, que necesita Docker activo. Primero se comprueba que el YAML se lee y qué jobs salen:

```bash
act -l
```

```
Stage  Job ID   Job name  Workflow name        Workflow file         Events
0      pruebas  pruebas   Pruebas de longitud  pruebas-longitud.yml  push,pull_request,workflow_dispatch
1      resumen  resumen   Pruebas de longitud  pruebas-longitud.yml  push,pull_request,workflow_dispatch
```

El *stage* 1 de `resumen` es el efecto de `needs`. Luego se simula el push:

```bash
act push -P ubuntu-latest=catthehacker/ubuntu:act-latest
```

```
[Pruebas de longitud/pruebas-1]  Start image=catthehacker/ubuntu:act-latest
[Pruebas de longitud/pruebas-2]  Start image=catthehacker/ubuntu:act-latest
[Pruebas de longitud/pruebas-2]  Run Main actions/checkout@v4
[Pruebas de longitud/pruebas-2]  Success - Main actions/checkout@v4
[Pruebas de longitud/pruebas-2]  Run Main actions/setup-python@v5
[Pruebas de longitud/pruebas-2]  | Successfully set up CPython (3.12.14)
[Pruebas de longitud/pruebas-1]  | Successfully set up CPython (3.11.16)
[Pruebas de longitud/pruebas-1]  Run Main Instalar dependencias
[Pruebas de longitud/pruebas-1]  Run Main Ejecutar pruebas
[Pruebas de longitud/pruebas-1]  | ============================== 4 passed in 0.01s ===============================
[Pruebas de longitud/pruebas-1]  Success - Main Ejecutar pruebas
[Pruebas de longitud/pruebas-2]  | ============================== 4 passed in 0.01s ===============================
[Pruebas de longitud/pruebas-2]  Success - Main Ejecutar pruebas
[Pruebas de longitud/pruebas-1]  | Cache saved with the key: setup-python-Linux-x64-24.04-Ubuntu-python-3.11.16-pip-...
[Pruebas de longitud/pruebas-2]  Run Main Probar el script
[Pruebas de longitud/pruebas-2]  | 100 m = 328.084 pies
[Pruebas de longitud/pruebas-2]  Success - Main Probar el script
[Pruebas de longitud/pruebas-1]  Job succeeded
[Pruebas de longitud/pruebas-2]  Job succeeded
[Pruebas de longitud/resumen  ]  Start image=catthehacker/ubuntu:act-latest
[Pruebas de longitud/resumen  ]  Run Main Escribir el resumen del run
[Pruebas de longitud/resumen  ]  Summary - Las pruebas pasaron en las dos versiones de Python.
[Pruebas de longitud/resumen  ]  Job succeeded
```

Ahí se ve cada pieza en acción. La matriz produjo `pruebas-1` con Python 3.11.16 y `pruebas-2` con 3.12.14, y los dos corrieron a la vez. El paso `Probar el script` solo salió en `pruebas-2`, donde el `if` se cumple. `resumen` arrancó cuando los dos terminaron, y `cache: pip` guardó la caché al cerrar cada job. En la segunda corrida el mismo paso imprime `Cache restored from key: setup-python-linux-x64-24.04-ubuntu-python-3.11.16-pip-...`. La corrida completa tarda cerca de un minuto en un portátil corriente; en GitHub un job así tarda entre 10 y 20 segundos.

Una vez en GitHub, el run se revisa desde la pestaña Actions o desde la terminal. Así se ve un run del repositorio base del ejercicio, donde el convertidor todavía lanza `NotImplementedError`:

```bash
gh run list --limit 2
gh run view 34006760794
```

```
completed  failure  readme: quita la rubrica de puntos           Pruebas  main  push  34006760794  11s
completed  failure  Enunciado y flujo de pruebas del ejercicio   Pruebas  main  push  32190788329  11s

X main Pruebas · 34006760794
Triggered via push about 10 days ago

JOBS
X pruebas in 7s (ID 101415278516)
  ✓ Set up job
  ✓ Run actions/checkout@v4
  ✓ Run actions/setup-python@v5
  ✓ Instalar dependencias
  ✓ Pruebas de Calculadora
  X Pruebas de ConvertidorTemperatura
  - El pipeline propio existe y tiene jobs y steps
  - Post Run actions/setup-python@v5
  ✓ Post Run actions/checkout@v4
  ✓ Complete job

To see what failed, try: gh run view 34006760794 --log-failed
```

El guion en los pasos siguientes al que falló indica que no corrieron: el job se detiene en el primer paso rojo. Ese es el estado del que parte el ejercicio; con las dos tareas hechas, los diez pasos salen en verde.

El badge del workflow `Pruebas` del repositorio base se escribe así en un README, con `<usuario>` reemplazado por el dueño del fork:

```markdown
[![Pruebas](https://github.com/<usuario>/infra-pipelines-ci-cd/actions/workflows/pruebas.yml/badge.svg)](https://github.com/<usuario>/infra-pipelines-ci-cd/actions/workflows/pruebas.yml)
```

La imagen se actualiza sola con cada run del workflow, y el mismo patrón sirve para `ci.yml`. El del repositorio base se puede abrir directamente: [badge de Pruebas](https://github.com/EjerciciosClasesCardel/infra-pipelines-ci-cd/actions/workflows/pruebas.yml/badge.svg).

### Lo que suele fallar

- Nada aparece en la pestaña Actions después del push. Tres causas, en orden de frecuencia: el fork trae los workflows desactivados y hay que entrar a Actions y pulsar el botón que los habilita; el archivo quedó en `.github/workflow/` (sin la `s`) o fuera de `.github/`; o `on: push: branches: [main]` no coincide con la rama a la que se hizo push. Con `act -l` en la máquina propia, una carpeta mal nombrada devuelve la tabla de jobs vacía.
- La pestaña Actions marca el workflow con *Invalid workflow file* y la línea del problema. Es indentación: un guion corrido un espacio, o una tabulación. `act -l` lo reporta antes de subirlo: `yaml: line 6: did not find expected '-' indicator` y `yaml: line 5: found a tab character that violates indentation`.
- El paso `El pipeline propio existe y tiene jobs y steps` de `pruebas.yml` dice `Falta .github/workflows/ci.yml`, o las pruebas del convertidor siguen en `NotImplementedError` en el runner cuando en la máquina ya pasan. El archivo no se subió: `git status` lo muestra sin agregar o `git log origin/main..main` muestra commits sin push. El runner solo ve lo que está en el commit que disparó el run.
- `ModuleNotFoundError: No module named 'numpy'` (o el paquete que sea) en el runner, con las pruebas en verde en la máquina propia. El paquete está instalado en el venv local pero no en `requirements.txt`, y la máquina de GitHub arranca limpia en cada run. Lo mismo pasa con la versión de Python: un `type Grados = float` corre con el 3.14 del equipo y en el 3.11 del runner da `SyntaxError: invalid syntax`. La versión que manda es la del `python-version:` del workflow.
- `python-version: 3.10` sin comillas. YAML lee `3.10` como el número `3.1` (con PyYAML: `yaml.safe_load('python-version: 3.10')` devuelve `{'python-version': 3.1}`), y `setup-python` sale a buscar un Python 3.1 que no existe. Entre comillas, `"3.10"`, es texto y llega intacto.

### Enlaces

- [Sintaxis de los workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax): la referencia completa de `name`, `on`, `jobs`, `runs-on`, `steps`, `with`, `env`, `needs`, `strategy.matrix` e `if`.
- [Eventos que disparan workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows): `push`, `pull_request`, `workflow_dispatch` y sus filtros por rama y por ruta.
- [Expresiones](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions) y [contextos](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts): qué se puede escribir dentro de `${{ }}` y de `if:`, con los operadores, las funciones y los contextos `matrix`, `github` y `env`.
- [actions/checkout](https://github.com/actions/checkout) y [actions/setup-python](https://github.com/actions/setup-python): los parámetros de `with:` de cada acción, entre ellos `python-version` y `cache`, y qué guarda la caché de pip.
- [Ver los logs de un run](https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs), [agregar un badge de estado](https://docs.github.com/en/actions/how-tos/monitor-workflows/add-a-status-badge) y [comandos de workflow](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands): dónde se leen los runs, cómo se arma la URL del badge y cómo funciona `GITHUB_STEP_SUMMARY`.
- [gh run](https://cli.github.com/manual/gh_run) y [act](https://nektosact.com/): los runs desde la terminal (`list`, `view`, `watch`, `rerun`) y cómo simular cada evento en la máquina propia.

## Cómo compilar y ejecutar en la máquina propia

En Debian o Ubuntu hace falta Python con `venv`, `pip` y git; `gh` es opcional y `act` pide Docker:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git
sudo apt install gh                # opcional: ver runs desde la terminal
```

Con eso, el flujo del ejercicio es el del README dentro de un entorno virtual:

```bash
git clone git@github.com:<usuario>/infra-pipelines-ci-cd.git
cd infra-pipelines-ci-cd
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/ -v
```

Para `act` se instala Docker con [la guía de Docker Engine para Ubuntu](https://docs.docker.com/engine/install/ubuntu/) y luego `act` desde [su página de instalación](https://nektosact.com/installation/index.html) o como extensión de `gh` con `gh extension install nektos/gh-act`. La primera corrida descarga la imagen `catthehacker/ubuntu:act-latest`, de unos 2,3 GB; la bandera `-P ubuntu-latest=catthehacker/ubuntu:act-latest` le dice a `act` que use esa imagen para `runs-on: ubuntu-latest`, y `act` la recuerda si se guarda en `~/.actrc`.

En Windows la vía es WSL2 con Ubuntu, según [la guía de instalación de WSL](https://learn.microsoft.com/en-us/windows/wsl/install); dentro de esa Ubuntu valen los comandos anteriores tal cual. El repositorio se clona en el sistema de archivos de Linux (`~/`), no en `/mnt/c/`, porque git y pytest sobre `/mnt/c/` van lentos. Docker Desktop con el backend de WSL2 deja `docker` disponible dentro de la distribución. Si se trabaja con el Python de Windows sin WSL, el entorno se activa con `venv\Scripts\activate` y `python` reemplaza a `python3`; la [documentación de Python en Windows](https://docs.python.org/3/using/windows.html) cubre el instalador y el `py` launcher.

En macOS, `python3` viene con las herramientas de línea de comandos de Xcode o se instala con [Homebrew](https://brew.sh/) (`brew install python git gh`), y los comandos del venv y de pytest son los mismos de Linux; la [documentación de Python en macOS](https://docs.python.org/3/using/mac.html) explica las variantes. Un detalle que muerde en macOS y en Windows: el sistema de archivos no distingue mayúsculas, así que `from src.Main import` funciona ahí y falla en `ubuntu-latest`, que sí las distingue. Los nombres de archivo se escriben exactamente como están en el repositorio.
