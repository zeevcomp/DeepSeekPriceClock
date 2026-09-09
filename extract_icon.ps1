param([string]$exePath, [string]$outPng)
Add-Type -AssemblyName System.Drawing
$icon = [System.Drawing.Icon]::ExtractAssociatedIcon($exePath)
if ($icon -eq $null) { Write-Output "NO_ICON"; exit 1 }
$bmp = $icon.ToBitmap()
$bmp.Save($outPng, [System.Drawing.Imaging.ImageFormat]::Png)
Write-Output ("extracted {0}x{1}" -f $bmp.Width, $bmp.Height)
