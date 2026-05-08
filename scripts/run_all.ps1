$ErrorActionPreference = "Stop"

# Script de ejecución completa del proyecto.
# Sirve para que cualquier persona pueda reproducir el análisis desde cero
# después de colocar el CSV original en data/raw/.

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$Requirements = Join-Path $ProjectRoot "requirements.txt"

if (-not (Test-Path $Python)) {
    Write-Host "No se ha encontrado el entorno virtual. Creándolo..."
    python -m venv (Join-Path $ProjectRoot ".venv")
}

Write-Host "Comprobando dependencias..."
& $Python -m pip install -r $Requirements

Write-Host "Ejecutando limpieza y transformación..."
& $Python (Join-Path $ProjectRoot "src\analyze_genres.py")

Write-Host "Generando figuras del informe..."
& $Python (Join-Path $ProjectRoot "src\create_figures.py")

# Ejecutamos los notebooks y guardamos copias con sufijo _ejecutado.
# Así se conserva el notebook original y también queda una versión con salidas.
Write-Host "Ejecutando notebook 01..."
& $Python -m jupyter nbconvert --to notebook --execute (Join-Path $ProjectRoot "notebooks\01_analisis_generos.ipynb") --output "01_analisis_generos_ejecutado.ipynb" --output-dir (Join-Path $ProjectRoot "notebooks") --ExecutePreprocessor.timeout=120

Write-Host "Ejecutando notebook 02..."
& $Python -m jupyter nbconvert --to notebook --execute (Join-Path $ProjectRoot "notebooks\02_gratis_vs_pago.ipynb") --output "02_gratis_vs_pago_ejecutado.ipynb" --output-dir (Join-Path $ProjectRoot "notebooks") --ExecutePreprocessor.timeout=120

Write-Host "Ejecutando notebook 03..."
& $Python -m jupyter nbconvert --to notebook --execute (Join-Path $ProjectRoot "notebooks\03_valoraciones_popularidad.ipynb") --output "03_valoraciones_popularidad_ejecutado.ipynb" --output-dir (Join-Path $ProjectRoot "notebooks") --ExecutePreprocessor.timeout=120

Write-Host "Proyecto ejecutado correctamente."
