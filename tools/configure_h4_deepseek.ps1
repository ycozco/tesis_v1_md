param(
    [Parameter(Mandatory=$true)][decimal]$BudgetUsd,
    [ValidateSet('Check','Calibrate')][string]$Action='Check',
    [switch]$ReplaceKey
)
$ErrorActionPreference='Stop'
if ($BudgetUsd -le 0) { throw 'Indica un presupuesto positivo en USD.' }
$taskRoot=Split-Path -Parent $PSScriptRoot
$privateDir=Join-Path $taskRoot 'data\h4-deepseek'
$pythonPath=Join-Path $taskRoot 'data\runtime-research-clean\Scripts\python.exe'
$toolPath=Join-Path $taskRoot 'tools\h4_deepseek.py'
New-Item -ItemType Directory -Path $privateDir -Force | Out-Null
& $pythonPath -B $toolPath --init
if ($LASTEXITCODE -ne 0) { throw 'No se pudo preparar la configuracion privada.' }
$configPath=Join-Path $privateDir 'config.json'
$keyPath=Join-Path $privateDir 'key.dpapi'
if ($ReplaceKey -or -not (Test-Path -LiteralPath $keyPath)) {
    $secureKey=Read-Host 'Clave DeepSeek (entrada oculta; no pegar en el chat)' -AsSecureString
    if ($secureKey.Length -eq 0) { throw 'La clave no puede estar vacia.' }
    $secureKey | ConvertFrom-SecureString | Set-Content -LiteralPath $keyPath -Encoding UTF8
} else {
    $secureKey=(Get-Content -LiteralPath $keyPath -Raw).Trim() | ConvertTo-SecureString
}
$config=Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
$config.enabled=$true
$config.budget_usd=$BudgetUsd.ToString([Globalization.CultureInfo]::InvariantCulture)
$config | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $configPath -Encoding UTF8
$previousKey=[Environment]::GetEnvironmentVariable('H4_DEEPSEEK_API_KEY','Process')
$keyPointer=[IntPtr]::Zero
try {
    $keyPointer=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
    $env:H4_DEEPSEEK_API_KEY=[Runtime.InteropServices.Marshal]::PtrToStringBSTR($keyPointer)
    if ($Action -eq 'Calibrate') { & $pythonPath -B $toolPath --calibrate }
    else { & $pythonPath -B $toolPath --check }
    if ($LASTEXITCODE -ne 0) { throw 'Configuracion o calibracion pendiente; revisar el mensaje sin compartir secretos.' }
} finally {
    if ($keyPointer -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($keyPointer) }
    [Environment]::SetEnvironmentVariable('H4_DEEPSEEK_API_KEY',$previousKey,'Process')
    $secureKey.Dispose()
}
