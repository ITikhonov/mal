.text

# EAX - stack top
# RSI - stack rest

.global vm_go
vm_go:
	movq	%rdi,%rsi
	jmp	vm_6d61696e # main

.macro SAVE
	pushq	%rsi
.endm

.macro RESTORE
	popq	%rsi
.endm

.global vm_312b
vm_312b: # 1+
	incl	%eax
	ret

.global vm_64726f70
vm_64726f70:          # drop
	lodsl
	ret

.global vm_2e
vm_2e:                # .
	SAVE
	movslq %eax,%rdi
	call print_hex
	RESTORE
	jmp vm_64726f70 # drop
_num: .asciz "%x "

.global vm_647570
vm_647570:            # dup
	leaq -4(%rsi),%rsi
	movl %eax,(%rsi)
	ret

.global vm_7072696e74
vm_7072696e74:                # print
	SAVE
	movslq %eax,%rdi
	call print_str
	RESTORE
	jmp vm_64726f70 # drop
	ret
_str: .asciz "%s "

.global vm_6372
vm_6372:              # cr
	SAVE
	movq	$_empty,%rdi
	call	puts
	RESTORE
	ret

_empty: .asciz ""

.global vm_627965
vm_627965:            # bye
	jmp exit

