$env:PATH = "D:\dev-tools\node-v20.11.1-win-x64;D:\dev-tools\git;" + $env:PATH
$siteDir = "D:\重要技术文件\项目\文本展示\mas-reader-site"
$srcFile = "D:\重要技术文件\项目\文本展示\preview.html"

Copy-Item $srcFile "$siteDir\index.html" -Force
Set-Location $siteDir
git add index.html
git commit -m "update $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
git push origin main

Write-Host ""
Write-Host "✅ 已同步到公网！访问 https://unknown123485.github.io/" -ForegroundColor Green
