#!/usr/bin/env python3
"""
Setup and Validation Script for HTTP Ingestion & KPI Processing Pipeline

Este script verifica que:
1. Todas las bibliotecas requeridas estén instaladas
2. Los directorios de entrada/salida existen o se pueden crear
3. El proyecto está listo para ejecutar
"""

import sys
import subprocess
from pathlib import Path

# ==================== CONFIGURACIÓN ====================
REQUIRED_MODULES = {
    "requests": "requests>=2.31.0",
    "faker": "faker>=20.0.0",
    "bs4": "beautifulsoup4>=4.12.0",
    "lxml": "lxml>=4.9.0",
    "pandas": "pandas>=2.0.0",
    "numpy": "numpy>=1.24.0",
    "matplotlib": "matplotlib>=3.7.0",
}

REQUIRED_DIRS = [
    "01_ingestion_http/out",
    "02_simulation_logs/out",
    "03_kpi_processing/out",
    "04_etl_pentaho/db",
    "04_etl_pentaho/logs",
    "05_reporting/out",
]

REQUIRED_FILES = [
    "01_ingestion_http/run_all.py",
    "02_simulation_logs/generar_datos.py",
    "03_kpi_processing/calcular_kpis.py",
    "05_reporting/generar_reporte.py",
]

# ==================== FUNCIONES ====================
def print_header(text):
    """Imprime encabezado destacado."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_check(text, status="✓"):
    """Imprime una línea de verificación."""
    color = "\033[92m" if status == "✓" else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{status}{reset} {text}")

def check_python_version():
    """Verifica que la versión de Python sea >= 3.8"""
    print_header("1. Verificando versión de Python")
    v = sys.version_info
    if v.major >= 3 and v.minor >= 8:
        print_check(f"Python {v.major}.{v.minor}.{v.micro} OK", "✓")
        return True
    else:
        print_check(f"Python {v.major}.{v.minor} - Se requiere >= 3.8", "✗")
        return False

def check_imports():
    """Verifica que todas las bibliotecas requeridas estén instaladas."""
    print_header("2. Verificando bibliotecas requeridas")
    missing = []
    
    for import_name, package_name in REQUIRED_MODULES.items():
        try:
            __import__(import_name)
            print_check(f"{package_name} instalado", "✓")
        except ImportError:
            print_check(f"{package_name} NO instalado", "✗")
            missing.append(package_name)
    
    if missing:
        print("\n⚠️  Paquetes faltantes. Ejecuta:")
        print(f"   pip install {' '.join(missing)}")
        return False
    return True

def check_directories():
    """Verifica y crea los directorios requeridos."""
    print_header("3. Verificando directorios")
    for dir_path in REQUIRED_DIRS:
        p = Path(dir_path)
        if p.exists():
            print_check(f"{dir_path} existe", "✓")
        else:
            try:
                p.mkdir(parents=True, exist_ok=True)
                print_check(f"{dir_path} creado", "✓")
            except Exception as e:
                print_check(f"{dir_path} ERROR: {e}", "✗")
                return False
    return True

def check_files():
    """Verifica que los archivos principales existen."""
    print_header("4. Verificando archivos principales")
    all_exist = True
    for file_path in REQUIRED_FILES:
        p = Path(file_path)
        if p.exists():
            print_check(f"{file_path} existe", "✓")
        else:
            print_check(f"{file_path} NO ENCONTRADO", "✗")
            all_exist = False
    return all_exist

def check_requirements_file():
    """Verifica que requirements.txt existe."""
    print_header("5. Verificando requirements.txt")
    if Path("requirements.txt").exists():
        print_check("requirements.txt existe", "✓")
        return True
    else:
        print_check("requirements.txt NO ENCONTRADO", "✗")
        return False

def summary(results):
    """Imprime resumen final."""
    print_header("RESUMEN DE VALIDACIÓN")
    all_ok = all(results.values())
    
    for check, status in results.items():
        status_text = "PASS" if status else "FAIL"
        print_check(check, "✓" if status else "✗")
    
    if all_ok:
        print("\n✓ El proyecto está listo para ejecutar.")
        print("\nEjemplos de ejecución:")
        print("  1. Generar datos simulados:")
        print("     python 02_simulation_logs/generar_datos.py --n_registros 500 --seed 42")
        print("  2. Calcular KPIs:")
        print("     python 03_kpi_processing/calcular_kpis.py --input 02_simulation_logs/out/http_logs.jsonl --output 03_kpi_processing/out/kpi_por_endpoint_dia.csv")
        print("  3. Generar reporte:")
        print("     python 05_reporting/generar_reporte.py --input 03_kpi_processing/out/kpi_por_endpoint_dia.csv --output 05_reporting/out/report/kpi_diario.html")
    else:
        print("\n✗ Hay problemas que resolver. Ver arriba.")
        sys.exit(1)

def main():
    """Función principal."""
    print("\n" + "=" * 60)
    print("  HTTP INGESTION & KPI PROCESSING - Setup & Validation")
    print("=" * 60)
    
    results = {
        "Python version": check_python_version(),
        "Required packages": check_imports(),
        "Directory structure": check_directories(),
        "Main files": check_files(),
        "requirements.txt": check_requirements_file(),
    }
    
    summary(results)

if __name__ == "__main__":
    main()
