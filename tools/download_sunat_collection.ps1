# Recupera los originales exactos documentados; no completa semanas ausentes.
param([string]$RepoRoot = (Split-Path -Parent $PSScriptRoot))
$ErrorActionPreference='Stop'
$manifest=Get-Content -LiteralPath (Join-Path $RepoRoot 'datasets/fuentes/2026-10-31/manifest-sunat.json') -Raw | ConvertFrom-Json
$raw=Join-Path $RepoRoot 'data/fuentes_2026-10-31'
$dest=Join-Path $raw 'sunat'
New-Item -ItemType Directory -Path $dest -Force | Out-Null
Add-Type -AssemblyName System.IO.Compression.FileSystem
foreach($item in $manifest.fuentes){
 $file=Join-Path $dest $item.archivo
 if(-not(Test-Path -LiteralPath $file)){Invoke-WebRequest -Uri $item.url -OutFile $file -TimeoutSec 60}
 if((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash -ne $item.sha256){throw ('Original cambiado: '+$item.archivo)}
 $zip=[IO.Compression.ZipFile]::OpenRead($file)
 try{foreach($entry in $zip.Entries){if($entry.Name -match '\.dbf$'){$stream=$entry.Open();$output=[IO.File]::Create((Join-Path $dest $entry.Name));try{$stream.CopyTo($output)}finally{$stream.Dispose();$output.Dispose()}}}}finally{$zip.Dispose()}
}
$manifest.fuentes|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $raw 'descargas-sunat.json') -Encoding utf8
