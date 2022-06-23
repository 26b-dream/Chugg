SetKeyDelay, 100
Sleep, 2000

; Fixes broken quotes
FileEncoding UTF-8
loop, 10
{
    ; Right click the iframe
    ; This value needs to be modified depending on window position, size and text location
    Click, 400 1210 Right

    ; Copy the text from the iframe
    Send {Up}{Up}{Up}{Up}{RIGHT}{DOWN}{ENTER}

    ; Save the text from the iframe
    FileAppend,%Clipboard%,%A_TickCount%.html

    ; Activate the page to make it possible to go to the next page
    Click, 500 500

    ; Go to the next page
    Send {RIGHT}
    sleep 1000
}
; Just in case something goes wrong
Esc::ExitApp