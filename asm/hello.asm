section .data
    message db 'Hello, World!',0
section .text
    global _start
_start:
    ; write the message to stdout
    mov eax, 4      ; system call for write
    mov ebx, 1      ; file descriptor for stdout
    mov ecx, message    ; message to write
    mov edx, 13     ; message length
    int 0x80        ; call kernel
    ; exit program
    mov eax, 1      ; system call for exit
    xor ebx, ebx    ; return 0 status
    int 0x80        ; call kernel
