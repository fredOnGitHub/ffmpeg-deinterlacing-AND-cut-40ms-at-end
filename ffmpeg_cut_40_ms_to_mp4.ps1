clear

#Duration: 00:00:14.40, start: 1.020000, bitrate: 26760 kb/s

# $s = ffmpeg -i $file 2>&1 |  Select-String -Pattern "\d*:\d*:\d*.\d*"
# if ($s){
    # $s
    # Write-Host s $s.Matches.GetValue(0)
    # $d=$s.Matches.GetValue(0).ToString()
    # $h=$d.Substring(0,2)
    # $m=$d.Substring(3,2)
    # $s=$d.Substring(6,2)
    # $c=$d.Substring(9,2)
    # Write-Host "$h $m $s $c"
# }


# Write-Host "Num Args:" $args.Length;

# foreach ($arg in $args) {
    # Write-Host "Arg: $arg";
# }

if(-not($args.Length -eq 1)){
	Write-Host "usage : <nom_pgm>  <répertoire>"
}
else{
	$rep=$args[0]
	$files = Get-ChildItem -Path $rep -File -recurse -Include *.mTS
	# Write-Host "rep = $($rep)"
	foreach ($file in $files) {
		
		$s = ffmpeg -i $file 2>&1 |  Select-String -Pattern "Duration: \d\d:\d\d:\d\d.\d\d"
		# Write-Host $s.Matches.Length#nb de groupes trouvés
		if ($s.Matches.Length -eq 1){
			# Write-Host $s.Matches
			# $s.Matches
			# $s.Matches.Length
			
			$s = $s.ToString() | Select-String -Pattern "\d\d" -AllMatches
			$hour=[int]$s.Matches.GetValue(0).ToString()
			$min=[int]$s.Matches.GetValue(1).ToString()
			$sec=[int]$s.Matches.GetValue(2).ToString()
			$msec=[int]$s.Matches.GetValue(3).ToString() 
			# "$hour $min $sec $msec"
			
			$t=$h*[Math]::pow(60,3)+$m*[Math]::pow(60,2)+$sec*[Math]::pow(60,1)+$msec#en msec
			
			$enleve=40
			$t-=$enleve
			$hour=[Math]::Floor($t/[Math]::pow(60,3))
			$t-=($hour*[Math]::pow(60,3))
			
			$min=[Math]::Floor($t/[Math]::pow(60,2))
			$t-=($min*[Math]::pow(60,2))
			
			$sec=[Math]::Floor($t/[Math]::pow(60,1))
			$t-=($sec*[Math]::pow(60,1))

			$msec=$t
			
			# Write-Host $file.Name
			# Write-Host $file.Directory
			# Write-Host $file.FullName
			
			# ffprobe -i "$file" -show_entries format=duration -v quiet -of csv="p=0"
			$f="$($file.Directory)/v2-$($file.Name).mp4"
			
			# $c="ffmpeg -hide_banner -loglevel error -i $file -ss 00:00:00.00 -t $($hour):$($min):$($sec).$($msec) -c:v libx264 -c:a copy $($f)"
			$c="ffmpeg -hide_banner -loglevel error -i '$($file)' -ss 00:00:00.00 -t $($hour):$($min):$($sec).$($msec) -c:v copy -c:a copy '$($f)'"
			$c
			iex $c
		}
	}
}

# https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/select-string?view=powershell-7.2
# https://docs.microsoft.com/fr-fr/powershell/module/microsoft.powershell.core/about/about_redirection?view=powershell-7.2
# https://www.lojiciels.com/quelle-est-la-signification-de-2-1-sous-linux/

# Opérateur de sous-expression $( )
# https://docs.microsoft.com/fr-fr/powershell/module/microsoft.powershell.core/about/about_operators?view=powershell-7.2