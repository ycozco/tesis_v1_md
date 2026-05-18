$urls = @(
    "https://doi.org/10.1145/2939672.2939785",
    "https://arxiv.org/abs/2106.11959",
    "https://arxiv.org/abs/2207.08815",
    "https://arxiv.org/abs/1908.07442",
    "https://doi.org/10.1016/j.ijforecast.2021.03.012",
    "https://doi.org/10.1609/aaai.v37i9.26317",
    "https://arxiv.org/abs/2310.06625",
    "https://arxiv.org/abs/2403.07815",
    "https://arxiv.org/abs/2211.14730",
    "https://arxiv.org/abs/2201.12886",
    "https://doi.org/10.1109/ICDM.2008.17",
    "https://doi.org/10.1145/342009.335388",
    "https://arxiv.org/abs/1802.04365",
    "https://arxiv.org/abs/2206.09426",
    "https://doi.org/10.1109/TKDE.2022.3159580",
    "https://jmlr.org/papers/v20/19-011.html",
    "https://arxiv.org/abs/2211.13358",
    "https://arxiv.org/abs/2210.10723",
    "https://arxiv.org/abs/2403.19735",
    "https://doi.org/10.1007/s12599-025-00945-3",
    "https://arxiv.org/abs/2406.14243",
    "https://arxiv.org/abs/1705.07874",
    "https://doi.org/10.1145/2939672.2939778",
    "https://doi.org/10.1109/ACCESS.2023.3262138",
    "https://arxiv.org/abs/2205.02302",
    "https://doi.org/10.6028/NIST.AI.100-1",
    "https://doi.org/10.1145/3458723",
    "https://doi.org/10.1145/3287560.3287596",
    "https://arxiv.org/abs/2505.24650",
    "https://arxiv.org/abs/2601.09929",
    "https://arxiv.org/abs/2505.10050",
    "https://www.mdpi.com/1911-8074/19/1/13",
    "https://www.mdpi.com/2076-3417/15/13/7329",
    "https://www.bis.org/fsi/fsipapers24.pdf",
    "https://thecaq.org/wp-content/uploads/2024/04/caq_auditing-in-the-age-of-generative-ai__2024-04.pdf",
    "https://eur-lex.europa.eu/eli/reg/2024/1689"
)

$report = @()

foreach ($url in $urls) {
    try {
        $response = Invoke-WebRequest -Uri $url -Method Head -UseBasicParsing -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36" -TimeoutSec 10 -ErrorAction Stop
        $status = $response.StatusCode
        $report += [PSCustomObject]@{
            URL = $url
            Status = $status
            IsAccessible = $true
        }
        Write-Host "OK: $url"
    } catch {
        # Try GET request if HEAD fails
        try {
            $response = Invoke-WebRequest -Uri $url -Method Get -UseBasicParsing -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36" -TimeoutSec 10 -ErrorAction Stop
            $status = $response.StatusCode
            $report += [PSCustomObject]@{
                URL = $url
                Status = $status
                IsAccessible = $true
            }
            Write-Host "OK (GET): $url"
        } catch {
            $errorMsg = $_.Exception.Message
            $report += [PSCustomObject]@{
                URL = $url
                Status = "Error"
                IsAccessible = $false
                Message = $errorMsg
            }
            Write-Host "FAIL: $url - $errorMsg" -ForegroundColor Red
        }
    }
}

$report | Export-Csv -Path "d:\tesis_yoset\url_check_report.csv" -NoTypeInformation
Write-Host "Report saved to url_check_report.csv"
