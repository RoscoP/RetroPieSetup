$list = @("Australia",
    "Beta",
    "Demo",
    "Europe",
    "France",
    "Germany",
    "Italy",
    "Japan",
    "Spain")


foreach( $l in $list ){
    md -ea 0 $l
    move "*($l)*" "$l\"
}