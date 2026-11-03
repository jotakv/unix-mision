"""Misión 5 · Automatízalo. Pruébalo con:  bash comprobar.sh python"""
import os
import subprocess
import re


def ejecutar(comando, env=None):
    """Ejecuta un comando de terminal y devuelve (salida, codigo_de_salida)."""
    print(f"ejecuto: {comando}")
    resultado = subprocess.run(
        ["bash", "-c", comando], capture_output=True, text=True,   # siempre bash, también en Windows
        env=env if env is not None else os.environ.copy(),
    )
    salida = (resultado.stdout + resultado.stderr).strip()
    if salida:
        print("   " + salida.replace("\n", "\n   ")[:400])
    return salida, resultado.returncode


def resolver():
    fragmentos = []

    # Fragmento 1: find + cat (carpeta oculta en proyecto/datos)
    
    # Fragmento 1: localizar el archivo mediante find
    salida, codigo = ejecutar("find . -name fragmento1.txt")

    if codigo != 0 or not salida:
        raise RuntimeError("No se encontró fragmento1.txt")

    ruta = salida.splitlines()[0]

    # Leer el contenido del archivo encontrado
    contenido, codigo = ejecutar(f'cat "{ruta}"')

    if codigo != 0:
        raise RuntimeError("No se pudo leer el fragmento 1")

    # Extraer el valor situado después de FRAGMENTO 1:
    coincidencia = re.search(
        r"FRAGMENTO 1:\s*([A-Z0-9]+)",
        contenido
    )

    if not coincidencia:
        raise RuntimeError("No se encontró el valor del fragmento 1")

    fragmento1 = coincidencia.group(1)
    fragmentos.append(fragmento1)

    print(f"Fragmento 1 recuperado: {fragmento1}")


    # Fragmento 2: grep en proyecto/logs/app.log
    
    # Fragmento 2: localizar el valor mediante grep
    salida, codigo = ejecutar(
        "grep -o 'fragmento2=[A-Z0-9]*' proyecto/logs/app.log"
    )

    if codigo != 0 or not salida:
        raise RuntimeError("No se encontró el fragmento 2")

    fragmento2 = salida.split("=", 1)[1].strip()
    fragmentos.append(fragmento2)

    print(f"Fragmento 2 recuperado: {fragmento2}")


    # Fragmento 3: mkdir + mv en proyecto/descargas, luego ejecutar('bash ../comprobar.sh orden')
    
    # Fragmento 3: organizar archivos automáticamente

    # Crear carpetas de destino
    salida, codigo = ejecutar(
        "mkdir -p proyecto/descargas/imagenes "
        "proyecto/descargas/documentos "
        "proyecto/descargas/datos"
    )

    if codigo != 0:
        raise RuntimeError("No se pudieron crear las carpetas")

    print("Carpetas de destino preparadas")


    # Clasificar archivos según su extensión
    categorias = {
        "imagenes": ["*.jpg", "*.png"],
        "documentos": ["*.pdf", "*.txt"],
        "datos": ["*.csv", "*.json"],
    }

    for carpeta, patrones in categorias.items():
        for patron in patrones:
            comando = (
                f"cd proyecto/descargas && "
                f"if compgen -G '{patron}' > /dev/null; then "
                f"mv {patron} {carpeta}/; "
                f"fi"
            )

            salida, codigo = ejecutar(comando)

            if codigo != 0:
                raise RuntimeError(
                    f"Error al mover archivos {patron} a {carpeta}"
                )

        print(f"Categoría {carpeta} organizada")


    # Comprobar la organización y recuperar el fragmento 3
    salida, codigo = ejecutar("bash ../comprobar.sh orden")

    if codigo != 0 or "Descargas ordenada" not in salida:
        raise RuntimeError(
            f"La organización no ha sido validada: {salida}"
        )

    coincidencia = re.search(
        r"FRAGMENTO 3:\s*([A-Z0-9]+)",
        salida
    )

    if not coincidencia:
        raise RuntimeError(
            "No se encontró el fragmento 3 en la respuesta"
        )

    fragmento3 = coincidencia.group(1)
    fragmentos.append(fragmento3)

    print(f"Fragmento 3 recuperado: {fragmento3}")


    # Fragmento 4: chmod +x y ejecutar('cd proyecto && ./herramientas/revelar.sh', env={**os.environ, "AGENTE": "robot"})
    # TODO

    clave = "-".join(fragmentos)
    print(f"\nCLAVE: {clave}")
    return clave


if __name__ == "__main__":
    if not os.path.isdir("proyecto"):
        print("Ejecútame desde la carpeta mision/ :  cd mision && python3 ../entrega/resolver.py   (o python)")
        raise SystemExit(1)
    resolver()
