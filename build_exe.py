"""
Script para crear el ejecutable del Generador de Informes de Reparos
Ejecutar este script para generar el .exe
"""

import os
import sys
import subprocess

def install_pyinstaller():
    """Instala PyInstaller si no está instalado"""
    print("🔧 Verificando PyInstaller...")
    try:
        import PyInstaller
        print("✅ PyInstaller ya está instalado")
    except ImportError:
        print("📦 Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller instalado correctamente")

def create_spec_file():
    """Crea el archivo .spec personalizado para PyInstaller"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['report_maker.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['requests', 'docx', 'tkinter', 'PIL'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GeneradorInformesReparos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No mostrar consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Aquí puedes añadir un icono .ico si tienes uno
)
"""
    
    with open('report_maker.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Archivo .spec creado")

def build_executable():
    """Compila el ejecutable usando PyInstaller"""
    print("\n🔨 Construyendo ejecutable...")
    print("⏳ Esto puede tardar unos minutos...\n")
    
    try:
        # Usar el archivo .spec
        subprocess.check_call(['pyinstaller', '--clean', 'report_maker.spec'])
        
        print("\n" + "="*60)
        print("🎉 ¡EJECUTABLE CREADO EXITOSAMENTE!")
        print("="*60)
        print("\n📁 Ubicación del ejecutable:")
        print(f"   {os.path.abspath('dist/GeneradorInformesReparos.exe')}")
        print("\n📋 Instrucciones:")
        print("   1. Ve a la carpeta 'dist'")
        print("   2. Encontrarás 'GeneradorInformesReparos.exe'")
        print("   3. Puedes copiar este archivo a cualquier PC con Windows")
        print("   4. No necesita instalación ni dependencias")
        print("\n💡 Nota: El archivo pesa entre 30-50 MB porque incluye")
        print("   Python y todas las librerías necesarias.")
        print("="*60 + "\n")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error al crear el ejecutable: {e}")
        sys.exit(1)

def main():
    """Función principal"""
    print("="*60)
    print("🚀 GENERADOR DE EJECUTABLE - Informes de Reparos")
    print("="*60 + "\n")
    
    # Verificar que existe el archivo fuente
    if not os.path.exists('report_maker.py'):
        print("❌ ERROR: No se encuentra 'report_maker.py'")
        print("   Asegúrate de ejecutar este script en la misma carpeta")
        print("   donde está 'report_maker.py'")
        sys.exit(1)
    
    # Paso 1: Instalar PyInstaller
    install_pyinstaller()
    
    # Paso 2: Crear archivo .spec
    create_spec_file()
    
    # Paso 3: Construir ejecutable
    build_executable()

if __name__ == "__main__":
    main()