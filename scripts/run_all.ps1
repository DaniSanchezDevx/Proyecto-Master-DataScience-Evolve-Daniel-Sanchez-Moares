$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    Write-Host "No se ha encontrado el entorno virtual. Creandolo..."
    python -m venv (Join-Path $ProjectRoot ".venv")
    & $Python -m pip install -r (Join-Path $ProjectRoot "requirements.txt")
}

Write-Host "Ejecutando limpieza y transformacion..."
& $Python (Join-Path $ProjectRoot "src\analyze_genres.py")

Write-Host "Generando figuras del informe..."
& $Python (Join-Path $ProjectRoot "src\create_figures.py")

Write-Host "Ejecutando notebook 01..."
& $Python -m jupyter nbconvert --to notebook --execute (Join-Path $ProjectRoot "notebooks\01_analisis_generos.ipynb") --output "01_analisis_generos_ejecutado.ipynb" --output-dir (Join-Path $ProjectRoot "notebooks") --ExecutePreprocessor.timeout=120

Write-Host "Ejecutando notebook 02..."
& $Python -m jupyter nbconvert --to notebook --execute (Join-Path $ProjectRoot "notebooks\02_gratis_vs_pago.ipynb") --output "02_gratis_vs_pago_ejecutado.ipynb" --output-dir (Join-Path $ProjectRoot "notebooks") --ExecutePreprocessor.timeout=120

Write-Host "Ejecutando notebook 03..."
& $Python -m jupyter nbconvert --to notebook --execute (Join-Path $ProjectRoot "notebooks\03_valoraciones_popularidad.ipynb") --output "03_valoraciones_popularidad_ejecutado.ipynb" --output-dir (Join-Path $ProjectRoot "notebooks") --ExecutePreprocessor.timeout=120

Write-Host "Proyecto ejecutado correctamente."
