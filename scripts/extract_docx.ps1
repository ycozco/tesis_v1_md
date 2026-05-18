# Extractar contenido de DOCX usando .NET (nativo en Windows)
Add-Type -AssemblyName System.IO.Compression

$avancePath = "d:\tesis_yoset\avance\Plantilla - Tesis de Investigación 2026 (1).docx"
$formatoPath = "d:\tesis_yoset\formato\Plantilla - Tesis de Investigación 2026.docx"

function Extract-DocxContent {
    param([string]$docxPath)
    
    $tempDir = [System.IO.Path]::GetTempFileName()
    [System.IO.File]::Delete($tempDir)
    [System.IO.Directory]::CreateDirectory($tempDir) | Out-Null
    
    try {
        # DOCX es un ZIP; extraer contenido
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        [System.IO.Compression.ZipFile]::ExtractToDirectory($docxPath, $tempDir)
        
        # Leer document.xml
        $docXml = [xml](Get-Content "$tempDir\word\document.xml")
        
        # Extraer texto (simplificado: buscar todos los párrafos y runs)
        $textNodes = $docXml.GetElementsByTagName("w:t")
        $text = $textNodes | ForEach-Object { $_.InnerText } | Join-String -Separator ""
        
        Write-Output $text
    }
    finally {
        Remove-Item -Recurse -Force $tempDir -ErrorAction SilentlyContinue
    }
}

Write-Output "=== EXTRAYENDO AVANCE ===" 
Extract-DocxContent $avancePath > "d:\tesis_yoset\avance_extracted.txt"

Write-Output "=== EXTRAYENDO FORMATO ===" 
Extract-DocxContent $formatoPath > "d:\tesis_yoset\formato_extracted.txt"

Write-Output "Extracción completada. Ver archivos .txt generados."
