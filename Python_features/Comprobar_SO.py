
import platform

# Este script detecta el sistema operativo en el que se está ejecutando y genera un archivo de script adaptado al sistema operativo detectado.

#Detectar el sistema operativo local y generar un script.

#No requiere entrada, usa el sistema local.

#Archivo de script adaptado al sistema operativo.

#No utiliza comandos externos.

#Compatible con Windows, Linux y MacOS.

#Sin riesgos relacionados con la seguridad.



def get_os_type():
    os_name = platform.system()  # Utiliza la biblioteca platform para identificar el sistema operativo.

#Devuelve el nombre del sistema operativo (Linux, Windows, MacOS) o Unknown OS si no es reconocido.

    if os_name == 'Linux':
        return "Linux"
    elif os_name == 'Windows':
        return "Windows"
    elif os_name == 'Darwin':
        return "MacOS"
    else:
        return "Unknown OS"

# Genera el contenido de un script dependiendo del sistema operativo detectado.

def create_script():
    os_type = get_os_type()

    if os_type == "Linux":
        script = "#!/usr/bin/env python3\n"  # Shebang para Linux
        script += "print('Este script corre en Linux')\n"
    elif os_type == "Windows":
        script = "print('Este script corre en Windows')\n"
    elif os_type == "MacOS":
        script = "#!/usr/bin/env python3\n"  # También aplicamos shebang en MacOS
        script += "print('Este script corre en MacOS')\n"
    else:
        script = "print('Sistema operativo no identificado')\n"

    return script


# Guarda el script en un archivo cuyo nombre y extensión dependen del sistema operativo.
#Utiliza:
#.sh para Linux y MacOS.
#.bat para Windows.
#.txt para sistemas no reconocidos.


def save_script(script_content):
    os_type = get_os_type()

    # Guardar el script con el nombre adecuado dependiendo del OS
    if os_type == "Linux" or os_type == "MacOS":
        file_name = "script.sh"
    elif os_type == "Windows":
        file_name = "script.bat"
    else:
        file_name = "script.txt"

    with open(file_name, "w") as file:
        file.write(script_content)
    print(f"Script guardado como {file_name}")

# Función principal que será llamada desde otros programas
def create_and_save_script():
    script_content = create_script()
    save_script(script_content)

# __main__ eliminado para que se pueda importar sin ejecutar


