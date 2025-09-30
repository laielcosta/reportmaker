"""
Conversor Universal de Python a Ejecutable (.exe)
Convierte cualquier script Python a .exe de forma interactiva
"""

import os
import sys
import subprocess
import glob

def clear_screen():
    """Limpia la pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Muestra el header"""
    print("="*70)
    print("🚀 CONVERSOR UNIVERSAL DE PYTHON A EJECUTABLE (.EXE)")
    print("="*70 + "\n")

def install_pyinstaller():
    """Instala PyInstaller si no está instalado"""
    print("🔧 Verificando PyInstaller...")
    try:
        import PyInstaller
        print("✅ PyInstaller ya está instalado\n")
        return True
    except ImportError:
        print("📦 PyInstaller no está instalado.")
        respuesta = input("¿Deseas instalarlo ahora? (s/n): ").lower()
        if respuesta == 's':
            print("\n⏳ Instalando PyInstaller...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
                print("✅ PyInstaller instalado correctamente\n")
                return True
            except:
                print("❌ Error al instalar PyInstaller")
                return False
        return False

def list_python_files():
    """Lista todos los archivos .py en el directorio"""
    py_files = [f for f in glob.glob("*.py") if f != os.path.basename(__file__)]
    return py_files

def select_file():
    """Permite seleccionar el archivo a convertir"""
    files = list_python_files()
    
    if not files:
        print("❌ No se encontraron archivos .py en este directorio")
        return None
    
    print("📄 Archivos Python disponibles:")
    print("-" * 70)
    for i, file in enumerate(files, 1):
        size = os.path.getsize(file) / 1024  # KB
        print(f"  {i}. {file} ({size:.1f} KB)")
    print("-" * 70)
    
    while True:
        try:
            opcion = input("\n🔢 Selecciona el número del archivo (0 para salir): ")
            if opcion == '0':
                return None
            
            idx = int(opcion) - 1
            if 0 <= idx < len(files):
                return files[idx]
            else:
                print("❌ Número inválido. Intenta de nuevo.")
        except ValueError:
            print("❌ Por favor ingresa un número válido.")

def get_exe_name(default_name):
    """Obtiene el nombre para el ejecutable"""
    print(f"\n📝 Nombre del ejecutable")
    print(f"   Por defecto: {default_name}")
    nombre = input("   Ingresa un nombre personalizado (Enter para usar el predeterminado): ").strip()
    
    if not nombre:
        return default_name
    
    # Quitar extensión si la agregaron
    if nombre.endswith('.exe'):
        nombre = nombre[:-4]
    
    return nombre

def get_icon():
    """Busca archivos .ico en el directorio"""
    icons = glob.glob("*.ico")
    
    if not icons:
        return None
    
    print(f"\n🎨 Se encontraron {len(icons)} icono(s) .ico:")
    for i, icon in enumerate(icons, 1):
        print(f"  {i}. {icon}")
    
    respuesta = input("\n¿Deseas usar un icono? (s/n): ").lower()
    if respuesta != 's':
        return None
    
    while True:
        try:
            opcion = input("Selecciona el número del icono (0 para ninguno): ")
            if opcion == '0':
                return None
            
            idx = int(opcion) - 1
            if 0 <= idx < len(icons):
                return icons[idx]
            else:
                print("❌ Número inválido.")
        except ValueError:
            print("❌ Por favor ingresa un número válido.")

def get_build_options():
    """Obtiene las opciones de compilación"""
    print("\n⚙️ OPCIONES DE COMPILACIÓN")
    print("-" * 70)
    
    # Tipo de ejecutable
    print("\n1️⃣ Tipo de ejecutable:")
    print("   1. Un solo archivo (--onefile) - Más fácil de distribuir [Recomendado]")
    print("   2. Carpeta con archivos (--onedir) - Inicia más rápido")
    
    while True:
        opcion = input("\n   Selecciona (1 o 2): ")
        if opcion in ['1', '2']:
            onefile = (opcion == '1')
            break
        print("   ❌ Opción inválida")
    
    # Mostrar consola
    print("\n2️⃣ Ventana de consola:")
    print("   1. Sin consola (--windowed) - Solo interfaz gráfica [Recomendado para GUI]")
    print("   2. Con consola (--console) - Muestra ventana negra [Útil para debug]")
    
    while True:
        opcion = input("\n   Selecciona (1 o 2): ")
        if opcion in ['1', '2']:
            windowed = (opcion == '1')
            break
        print("   ❌ Opción inválida")
    
    # Comprimir con UPX
    print("\n3️⃣ Comprimir ejecutable con UPX:")
    print("   Reduce el tamaño del archivo (puede ser detectado por algunos antivirus)")
    upx = input("\n   ¿Usar UPX? (s/n): ").lower() == 's'
    
    return {
        'onefile': onefile,
        'windowed': windowed,
        'upx': upx
    }

def build_executable(script_file, exe_name, icon_file, options):
    """Compila el ejecutable con las opciones especificadas"""
    print("\n" + "="*70)
    print("🔨 CONSTRUYENDO EJECUTABLE")
    print("="*70)
    
    # Construir comando
    cmd = ['pyinstaller', '--clean']
    
    if options['onefile']:
        cmd.append('--onefile')
    else:
        cmd.append('--onedir')
    
    if options['windowed']:
        cmd.append('--windowed')
    else:
        cmd.append('--console')
    
    if options['upx']:
        cmd.append('--upx-dir=upx')
    else:
        cmd.append('--noupx')
    
    cmd.append(f'--name={exe_name}')
    
    if icon_file:
        cmd.append(f'--icon={icon_file}')
    
    cmd.append(script_file)
    
    # Mostrar comando
    print(f"\n📋 Comando a ejecutar:")
    print(f"   {' '.join(cmd)}\n")
    print("⏳ Esto puede tardar unos minutos...\n")
    print("-" * 70)
    
    try:
        # Ejecutar PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=False, text=True)
        
        print("-" * 70)
        print("\n" + "="*70)
        print("🎉 ¡EJECUTABLE CREADO EXITOSAMENTE!")
        print("="*70)
        
        # Ubicación del ejecutable
        if options['onefile']:
            exe_path = os.path.abspath(f"dist/{exe_name}.exe")
            print(f"\n📁 Ubicación: {exe_path}")
            print(f"📊 Tamaño: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
        else:
            dir_path = os.path.abspath(f"dist/{exe_name}/")
            print(f"\n📁 Ubicación: {dir_path}")
            print(f"   Ejecutable: {exe_name}.exe")
        
        print("\n✅ El ejecutable está listo para usar")
        print("💡 Puedes distribuirlo sin necesidad de Python instalado")
        print("="*70 + "\n")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print("\n" + "="*70)
        print("❌ ERROR AL CREAR EL EJECUTABLE")
        print("="*70)
        print(f"\n{str(e)}\n")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}\n")
        return False

def cleanup():
    """Pregunta si desea limpiar archivos temporales"""
    print("\n🧹 LIMPIEZA DE ARCHIVOS TEMPORALES")
    respuesta = input("¿Deseas eliminar las carpetas build/ y __pycache__? (s/n): ").lower()
    
    if respuesta == 's':
        try:
            import shutil
            if os.path.exists('build'):
                shutil.rmtree('build')
                print("✅ Carpeta 'build/' eliminada")
            
            if os.path.exists('__pycache__'):
                shutil.rmtree('__pycache__')
                print("✅ Carpeta '__pycache__/' eliminada")
            
            # Eliminar archivos .spec
            for spec in glob.glob("*.spec"):
                os.remove(spec)
                print(f"✅ Archivo '{spec}' eliminado")
                
        except Exception as e:
            print(f"⚠️ Error al limpiar: {str(e)}")

def main():
    """Función principal"""
    clear_screen()
    print_header()
    
    # Paso 1: Verificar/Instalar PyInstaller
    if not install_pyinstaller():
        print("\n❌ No se puede continuar sin PyInstaller")
        input("\nPresiona Enter para salir...")
        return
    
    # Paso 2: Seleccionar archivo
    print("PASO 1: Seleccionar archivo Python")
    print("="*70)
    script_file = select_file()
    
    if not script_file:
        print("\n👋 Operación cancelada")
        return
    
    print(f"\n✅ Archivo seleccionado: {script_file}\n")
    
    # Paso 3: Nombre del ejecutable
    print("="*70)
    print("PASO 2: Configurar nombre del ejecutable")
    print("="*70)
    default_name = os.path.splitext(script_file)[0]
    exe_name = get_exe_name(default_name)
    print(f"✅ Nombre del ejecutable: {exe_name}.exe\n")
    
    # Paso 4: Icono (opcional)
    print("="*70)
    print("PASO 3: Seleccionar icono (opcional)")
    print("="*70)
    icon_file = get_icon()
    if icon_file:
        print(f"✅ Icono seleccionado: {icon_file}\n")
    else:
        print("ℹ️ No se usará icono personalizado\n")
    
    # Paso 5: Opciones de compilación
    print("="*70)
    print("PASO 4: Configurar opciones de compilación")
    print("="*70)
    options = get_build_options()
    
    # Confirmación
    print("\n" + "="*70)
    print("📋 RESUMEN DE CONFIGURACIÓN")
    print("="*70)
    print(f"  📄 Archivo fuente: {script_file}")
    print(f"  📦 Nombre ejecutable: {exe_name}.exe")
    print(f"  🎨 Icono: {icon_file if icon_file else 'Sin icono'}")
    print(f"  📑 Tipo: {'Un solo archivo' if options['onefile'] else 'Carpeta'}")
    print(f"  🖥️ Consola: {'Oculta' if options['windowed'] else 'Visible'}")
    print(f"  🗜️ UPX: {'Activado' if options['upx'] else 'Desactivado'}")
    print("="*70)
    
    respuesta = input("\n¿Proceder con la compilación? (s/n): ").lower()
    if respuesta != 's':
        print("\n👋 Operación cancelada")
        return
    
    # Paso 6: Compilar
    success = build_executable(script_file, exe_name, icon_file, options)
    
    if success:
        # Paso 7: Limpieza (opcional)
        cleanup()
        
        print("\n" + "="*70)
        print("✨ PROCESO COMPLETADO")
        print("="*70)
        print("\n🎯 Próximos pasos:")
        print("   1. Prueba el ejecutable en tu PC")
        print("   2. Compártelo con otros usuarios")
        print("   3. No necesitan Python instalado para ejecutarlo")
        print("\n" + "="*70)
    
    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        input("\nPresiona Enter para salir...")