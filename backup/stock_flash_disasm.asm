
flash.bin:     file format binary


Disassembly of section .data:

00000000 <.data>:
       0:	0c 94 5c 00 	jmp	0xb8	;  0xb8
       4:	0c 94 6e 00 	jmp	0xdc	;  0xdc
       8:	0c 94 6e 00 	jmp	0xdc	;  0xdc
       c:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      10:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      14:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      18:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      1c:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      20:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      24:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      28:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      2c:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      30:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      34:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      38:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      3c:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      40:	0c 94 13 01 	jmp	0x226	;  0x226
      44:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      48:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      4c:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      50:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      54:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      58:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      5c:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      60:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      64:	0c 94 6e 00 	jmp	0xdc	;  0xdc
      68:	00 00       	nop
      6a:	00 00       	nop
      6c:	24 00       	.word	0x0024	; ????
      6e:	27 00       	.word	0x0027	; ????
      70:	2a 00       	.word	0x002a	; ????
      72:	00 00       	nop
      74:	00 00       	nop
      76:	25 00       	.word	0x0025	; ????
      78:	28 00       	.word	0x0028	; ????
      7a:	2b 00       	.word	0x002b	; ????
      7c:	04 04       	cpc	r0, r4
      7e:	04 04       	cpc	r0, r4
      80:	04 04       	cpc	r0, r4
      82:	04 04       	cpc	r0, r4
      84:	02 02       	muls	r16, r18
      86:	02 02       	muls	r16, r18
      88:	02 02       	muls	r16, r18
      8a:	03 03       	mulsu	r16, r19
      8c:	03 03       	mulsu	r16, r19
      8e:	03 03       	mulsu	r16, r19
      90:	01 02       	muls	r16, r17
      92:	04 08       	sbc	r0, r4
      94:	10 20       	and	r1, r0
      96:	40 80       	ld	r4, Z
      98:	01 02       	muls	r16, r17
      9a:	04 08       	sbc	r0, r4
      9c:	10 20       	and	r1, r0
      9e:	01 02       	muls	r16, r17
      a0:	04 08       	sbc	r0, r4
      a2:	10 20       	and	r1, r0
      a4:	00 00       	nop
      a6:	00 08       	sbc	r0, r0
      a8:	00 02       	muls	r16, r16
      aa:	01 00       	.word	0x0001	; ????
      ac:	00 03       	mulsu	r16, r16
      ae:	04 07       	cpc	r16, r20
	...
      b8:	11 24       	eor	r1, r1
      ba:	1f be       	out	0x3f, r1	; 63
      bc:	cf ef       	ldi	r28, 0xFF	; 255
      be:	d8 e0       	ldi	r29, 0x08	; 8
      c0:	de bf       	out	0x3e, r29	; 62
      c2:	cd bf       	out	0x3d, r28	; 61
      c4:	21 e0       	ldi	r18, 0x01	; 1
      c6:	a0 e0       	ldi	r26, 0x00	; 0
      c8:	b1 e0       	ldi	r27, 0x01	; 1
      ca:	01 c0       	rjmp	.+2      	;  0xce
      cc:	1d 92       	st	X+, r1
      ce:	a9 30       	cpi	r26, 0x09	; 9
      d0:	b2 07       	cpc	r27, r18
      d2:	e1 f7       	brne	.-8      	;  0xcc
      d4:	0e 94 5d 01 	call	0x2ba	;  0x2ba
      d8:	0c 94 fe 01 	jmp	0x3fc	;  0x3fc
      dc:	0c 94 00 00 	jmp	0	;  0x0
      e0:	90 e0       	ldi	r25, 0x00	; 0
      e2:	fc 01       	movw	r30, r24
      e4:	ec 55       	subi	r30, 0x5C	; 92
      e6:	ff 4f       	sbci	r31, 0xFF	; 255
      e8:	24 91       	lpm	r18, Z
      ea:	fc 01       	movw	r30, r24
      ec:	e0 57       	subi	r30, 0x70	; 112
      ee:	ff 4f       	sbci	r31, 0xFF	; 255
      f0:	34 91       	lpm	r19, Z
      f2:	fc 01       	movw	r30, r24
      f4:	e4 58       	subi	r30, 0x84	; 132
      f6:	ff 4f       	sbci	r31, 0xFF	; 255
      f8:	e4 91       	lpm	r30, Z
      fa:	ee 23       	and	r30, r30
      fc:	c9 f0       	breq	.+50     	;  0x130
      fe:	22 23       	and	r18, r18
     100:	39 f0       	breq	.+14     	;  0x110
     102:	23 30       	cpi	r18, 0x03	; 3
     104:	01 f1       	breq	.+64     	;  0x146
     106:	a8 f4       	brcc	.+42     	;  0x132
     108:	21 30       	cpi	r18, 0x01	; 1
     10a:	19 f1       	breq	.+70     	;  0x152
     10c:	22 30       	cpi	r18, 0x02	; 2
     10e:	29 f1       	breq	.+74     	;  0x15a
     110:	f0 e0       	ldi	r31, 0x00	; 0
     112:	ee 0f       	add	r30, r30
     114:	ff 1f       	adc	r31, r31
     116:	ee 58       	subi	r30, 0x8E	; 142
     118:	ff 4f       	sbci	r31, 0xFF	; 255
     11a:	a5 91       	lpm	r26, Z+
     11c:	b4 91       	lpm	r27, Z
     11e:	8f b7       	in	r24, 0x3f	; 63
     120:	f8 94       	cli
     122:	ec 91       	ld	r30, X
     124:	61 11       	cpse	r22, r1
     126:	26 c0       	rjmp	.+76     	;  0x174
     128:	30 95       	com	r19
     12a:	3e 23       	and	r19, r30
     12c:	3c 93       	st	X, r19
     12e:	8f bf       	out	0x3f, r24	; 63
     130:	08 95       	ret
     132:	27 30       	cpi	r18, 0x07	; 7
     134:	a9 f0       	breq	.+42     	;  0x160
     136:	28 30       	cpi	r18, 0x08	; 8
     138:	c9 f0       	breq	.+50     	;  0x16c
     13a:	24 30       	cpi	r18, 0x04	; 4
     13c:	49 f7       	brne	.-46     	;  0x110
     13e:	80 91 80 00 	lds	r24, 0x0080	;  0x800080
     142:	8f 7d       	andi	r24, 0xDF	; 223
     144:	03 c0       	rjmp	.+6      	;  0x14c
     146:	80 91 80 00 	lds	r24, 0x0080	;  0x800080
     14a:	8f 77       	andi	r24, 0x7F	; 127
     14c:	80 93 80 00 	sts	0x0080, r24	;  0x800080
     150:	df cf       	rjmp	.-66     	;  0x110
     152:	84 b5       	in	r24, 0x24	; 36
     154:	8f 77       	andi	r24, 0x7F	; 127
     156:	84 bd       	out	0x24, r24	; 36
     158:	db cf       	rjmp	.-74     	;  0x110
     15a:	84 b5       	in	r24, 0x24	; 36
     15c:	8f 7d       	andi	r24, 0xDF	; 223
     15e:	fb cf       	rjmp	.-10     	;  0x156
     160:	80 91 b0 00 	lds	r24, 0x00B0	;  0x8000b0
     164:	8f 77       	andi	r24, 0x7F	; 127
     166:	80 93 b0 00 	sts	0x00B0, r24	;  0x8000b0
     16a:	d2 cf       	rjmp	.-92     	;  0x110
     16c:	80 91 b0 00 	lds	r24, 0x00B0	;  0x8000b0
     170:	8f 7d       	andi	r24, 0xDF	; 223
     172:	f9 cf       	rjmp	.-14     	;  0x166
     174:	3e 2b       	or	r19, r30
     176:	da cf       	rjmp	.-76     	;  0x12c
     178:	3f b7       	in	r19, 0x3f	; 63
     17a:	f8 94       	cli
     17c:	80 91 05 01 	lds	r24, 0x0105	;  0x800105
     180:	90 91 06 01 	lds	r25, 0x0106	;  0x800106
     184:	a0 91 07 01 	lds	r26, 0x0107	;  0x800107
     188:	b0 91 08 01 	lds	r27, 0x0108	;  0x800108
     18c:	26 b5       	in	r18, 0x26	; 38
     18e:	a8 9b       	sbis	0x15, 0	; 21
     190:	05 c0       	rjmp	.+10     	;  0x19c
     192:	2f 3f       	cpi	r18, 0xFF	; 255
     194:	19 f0       	breq	.+6      	;  0x19c
     196:	01 96       	adiw	r24, 0x01	; 1
     198:	a1 1d       	adc	r26, r1
     19a:	b1 1d       	adc	r27, r1
     19c:	3f bf       	out	0x3f, r19	; 63
     19e:	ba 2f       	mov	r27, r26
     1a0:	a9 2f       	mov	r26, r25
     1a2:	98 2f       	mov	r25, r24
     1a4:	88 27       	eor	r24, r24
     1a6:	bc 01       	movw	r22, r24
     1a8:	cd 01       	movw	r24, r26
     1aa:	62 0f       	add	r22, r18
     1ac:	71 1d       	adc	r23, r1
     1ae:	81 1d       	adc	r24, r1
     1b0:	91 1d       	adc	r25, r1
     1b2:	42 e0       	ldi	r20, 0x02	; 2
     1b4:	66 0f       	add	r22, r22
     1b6:	77 1f       	adc	r23, r23
     1b8:	88 1f       	adc	r24, r24
     1ba:	99 1f       	adc	r25, r25
     1bc:	4a 95       	dec	r20
     1be:	d1 f7       	brne	.-12     	;  0x1b4
     1c0:	08 95       	ret
     1c2:	8f 92       	push	r8
     1c4:	9f 92       	push	r9
     1c6:	af 92       	push	r10
     1c8:	bf 92       	push	r11
     1ca:	cf 92       	push	r12
     1cc:	df 92       	push	r13
     1ce:	ef 92       	push	r14
     1d0:	ff 92       	push	r15
     1d2:	4b 01       	movw	r8, r22
     1d4:	5c 01       	movw	r10, r24
     1d6:	0e 94 bc 00 	call	0x178	;  0x178
     1da:	6b 01       	movw	r12, r22
     1dc:	7c 01       	movw	r14, r24
     1de:	0e 94 bc 00 	call	0x178	;  0x178
     1e2:	6c 19       	sub	r22, r12
     1e4:	7d 09       	sbc	r23, r13
     1e6:	8e 09       	sbc	r24, r14
     1e8:	9f 09       	sbc	r25, r15
     1ea:	68 3e       	cpi	r22, 0xE8	; 232
     1ec:	73 40       	sbci	r23, 0x03	; 3
     1ee:	81 05       	cpc	r24, r1
     1f0:	91 05       	cpc	r25, r1
     1f2:	a8 f3       	brcs	.-22     	;  0x1de
     1f4:	21 e0       	ldi	r18, 0x01	; 1
     1f6:	82 1a       	sub	r8, r18
     1f8:	91 08       	sbc	r9, r1
     1fa:	a1 08       	sbc	r10, r1
     1fc:	b1 08       	sbc	r11, r1
     1fe:	88 ee       	ldi	r24, 0xE8	; 232
     200:	c8 0e       	add	r12, r24
     202:	83 e0       	ldi	r24, 0x03	; 3
     204:	d8 1e       	adc	r13, r24
     206:	e1 1c       	adc	r14, r1
     208:	f1 1c       	adc	r15, r1
     20a:	81 14       	cp	r8, r1
     20c:	91 04       	cpc	r9, r1
     20e:	a1 04       	cpc	r10, r1
     210:	b1 04       	cpc	r11, r1
     212:	29 f7       	brne	.-54     	;  0x1de
     214:	ff 90       	pop	r15
     216:	ef 90       	pop	r14
     218:	df 90       	pop	r13
     21a:	cf 90       	pop	r12
     21c:	bf 90       	pop	r11
     21e:	af 90       	pop	r10
     220:	9f 90       	pop	r9
     222:	8f 90       	pop	r8
     224:	08 95       	ret
     226:	1f 92       	push	r1
     228:	0f 92       	push	r0
     22a:	0f b6       	in	r0, 0x3f	; 63
     22c:	0f 92       	push	r0
     22e:	11 24       	eor	r1, r1
     230:	2f 93       	push	r18
     232:	3f 93       	push	r19
     234:	8f 93       	push	r24
     236:	9f 93       	push	r25
     238:	af 93       	push	r26
     23a:	bf 93       	push	r27
     23c:	80 91 01 01 	lds	r24, 0x0101	;  0x800101
     240:	90 91 02 01 	lds	r25, 0x0102	;  0x800102
     244:	a0 91 03 01 	lds	r26, 0x0103	;  0x800103
     248:	b0 91 04 01 	lds	r27, 0x0104	;  0x800104
     24c:	30 91 00 01 	lds	r19, 0x0100	;  0x800100
     250:	23 e0       	ldi	r18, 0x03	; 3
     252:	23 0f       	add	r18, r19
     254:	2d 37       	cpi	r18, 0x7D	; 125
     256:	58 f5       	brcc	.+86     	;  0x2ae
     258:	01 96       	adiw	r24, 0x01	; 1
     25a:	a1 1d       	adc	r26, r1
     25c:	b1 1d       	adc	r27, r1
     25e:	20 93 00 01 	sts	0x0100, r18	;  0x800100
     262:	80 93 01 01 	sts	0x0101, r24	;  0x800101
     266:	90 93 02 01 	sts	0x0102, r25	;  0x800102
     26a:	a0 93 03 01 	sts	0x0103, r26	;  0x800103
     26e:	b0 93 04 01 	sts	0x0104, r27	;  0x800104
     272:	80 91 05 01 	lds	r24, 0x0105	;  0x800105
     276:	90 91 06 01 	lds	r25, 0x0106	;  0x800106
     27a:	a0 91 07 01 	lds	r26, 0x0107	;  0x800107
     27e:	b0 91 08 01 	lds	r27, 0x0108	;  0x800108
     282:	01 96       	adiw	r24, 0x01	; 1
     284:	a1 1d       	adc	r26, r1
     286:	b1 1d       	adc	r27, r1
     288:	80 93 05 01 	sts	0x0105, r24	;  0x800105
     28c:	90 93 06 01 	sts	0x0106, r25	;  0x800106
     290:	a0 93 07 01 	sts	0x0107, r26	;  0x800107
     294:	b0 93 08 01 	sts	0x0108, r27	;  0x800108
     298:	bf 91       	pop	r27
     29a:	af 91       	pop	r26
     29c:	9f 91       	pop	r25
     29e:	8f 91       	pop	r24
     2a0:	3f 91       	pop	r19
     2a2:	2f 91       	pop	r18
     2a4:	0f 90       	pop	r0
     2a6:	0f be       	out	0x3f, r0	; 63
     2a8:	0f 90       	pop	r0
     2aa:	1f 90       	pop	r1
     2ac:	18 95       	reti
     2ae:	26 e8       	ldi	r18, 0x86	; 134
     2b0:	23 0f       	add	r18, r19
     2b2:	02 96       	adiw	r24, 0x02	; 2
     2b4:	a1 1d       	adc	r26, r1
     2b6:	b1 1d       	adc	r27, r1
     2b8:	d2 cf       	rjmp	.-92     	;  0x25e
     2ba:	78 94       	sei
     2bc:	84 b5       	in	r24, 0x24	; 36
     2be:	82 60       	ori	r24, 0x02	; 2
     2c0:	84 bd       	out	0x24, r24	; 36
     2c2:	84 b5       	in	r24, 0x24	; 36
     2c4:	81 60       	ori	r24, 0x01	; 1
     2c6:	84 bd       	out	0x24, r24	; 36
     2c8:	85 b5       	in	r24, 0x25	; 37
     2ca:	82 60       	ori	r24, 0x02	; 2
     2cc:	85 bd       	out	0x25, r24	; 37
     2ce:	85 b5       	in	r24, 0x25	; 37
     2d0:	81 60       	ori	r24, 0x01	; 1
     2d2:	85 bd       	out	0x25, r24	; 37
     2d4:	80 91 6e 00 	lds	r24, 0x006E	;  0x80006e
     2d8:	81 60       	ori	r24, 0x01	; 1
     2da:	80 93 6e 00 	sts	0x006E, r24	;  0x80006e
     2de:	10 92 81 00 	sts	0x0081, r1	;  0x800081
     2e2:	80 91 81 00 	lds	r24, 0x0081	;  0x800081
     2e6:	82 60       	ori	r24, 0x02	; 2
     2e8:	80 93 81 00 	sts	0x0081, r24	;  0x800081
     2ec:	80 91 81 00 	lds	r24, 0x0081	;  0x800081
     2f0:	81 60       	ori	r24, 0x01	; 1
     2f2:	80 93 81 00 	sts	0x0081, r24	;  0x800081
     2f6:	80 91 80 00 	lds	r24, 0x0080	;  0x800080
     2fa:	81 60       	ori	r24, 0x01	; 1
     2fc:	80 93 80 00 	sts	0x0080, r24	;  0x800080
     300:	80 91 b1 00 	lds	r24, 0x00B1	;  0x8000b1
     304:	84 60       	ori	r24, 0x04	; 4
     306:	80 93 b1 00 	sts	0x00B1, r24	;  0x8000b1
     30a:	80 91 b0 00 	lds	r24, 0x00B0	;  0x8000b0
     30e:	81 60       	ori	r24, 0x01	; 1
     310:	80 93 b0 00 	sts	0x00B0, r24	;  0x8000b0
     314:	80 91 7a 00 	lds	r24, 0x007A	;  0x80007a
     318:	84 60       	ori	r24, 0x04	; 4
     31a:	80 93 7a 00 	sts	0x007A, r24	;  0x80007a
     31e:	80 91 7a 00 	lds	r24, 0x007A	;  0x80007a
     322:	82 60       	ori	r24, 0x02	; 2
     324:	80 93 7a 00 	sts	0x007A, r24	;  0x80007a
     328:	80 91 7a 00 	lds	r24, 0x007A	;  0x80007a
     32c:	81 60       	ori	r24, 0x01	; 1
     32e:	80 93 7a 00 	sts	0x007A, r24	;  0x80007a
     332:	80 91 7a 00 	lds	r24, 0x007A	;  0x80007a
     336:	80 68       	ori	r24, 0x80	; 128
     338:	80 93 7a 00 	sts	0x007A, r24	;  0x80007a
     33c:	10 92 c1 00 	sts	0x00C1, r1	;  0x8000c1
     340:	e9 e9       	ldi	r30, 0x99	; 153
     342:	f0 e0       	ldi	r31, 0x00	; 0
     344:	24 91       	lpm	r18, Z
     346:	e5 e8       	ldi	r30, 0x85	; 133
     348:	f0 e0       	ldi	r31, 0x00	; 0
     34a:	84 91       	lpm	r24, Z
     34c:	88 23       	and	r24, r24
     34e:	99 f0       	breq	.+38     	;  0x376
     350:	90 e0       	ldi	r25, 0x00	; 0
     352:	88 0f       	add	r24, r24
     354:	99 1f       	adc	r25, r25
     356:	fc 01       	movw	r30, r24
     358:	e8 59       	subi	r30, 0x98	; 152
     35a:	ff 4f       	sbci	r31, 0xFF	; 255
     35c:	a5 91       	lpm	r26, Z+
     35e:	b4 91       	lpm	r27, Z
     360:	fc 01       	movw	r30, r24
     362:	ee 58       	subi	r30, 0x8E	; 142
     364:	ff 4f       	sbci	r31, 0xFF	; 255
     366:	85 91       	lpm	r24, Z+
     368:	94 91       	lpm	r25, Z
     36a:	8f b7       	in	r24, 0x3f	; 63
     36c:	f8 94       	cli
     36e:	ec 91       	ld	r30, X
     370:	e2 2b       	or	r30, r18
     372:	ec 93       	st	X, r30
     374:	8f bf       	out	0x3f, r24	; 63
     376:	c0 e0       	ldi	r28, 0x00	; 0
     378:	d0 e0       	ldi	r29, 0x00	; 0
     37a:	61 e0       	ldi	r22, 0x01	; 1
     37c:	89 e0       	ldi	r24, 0x09	; 9
     37e:	0e 94 70 00 	call	0xe0	;  0xe0
     382:	6c e2       	ldi	r22, 0x2C	; 44
     384:	71 e0       	ldi	r23, 0x01	; 1
     386:	80 e0       	ldi	r24, 0x00	; 0
     388:	90 e0       	ldi	r25, 0x00	; 0
     38a:	0e 94 e1 00 	call	0x1c2	;  0x1c2
     38e:	60 e0       	ldi	r22, 0x00	; 0
     390:	89 e0       	ldi	r24, 0x09	; 9
     392:	0e 94 70 00 	call	0xe0	;  0xe0
     396:	64 e6       	ldi	r22, 0x64	; 100
     398:	70 e0       	ldi	r23, 0x00	; 0
     39a:	80 e0       	ldi	r24, 0x00	; 0
     39c:	90 e0       	ldi	r25, 0x00	; 0
     39e:	0e 94 e1 00 	call	0x1c2	;  0x1c2
     3a2:	61 e0       	ldi	r22, 0x01	; 1
     3a4:	89 e0       	ldi	r24, 0x09	; 9
     3a6:	0e 94 70 00 	call	0xe0	;  0xe0
     3aa:	68 ec       	ldi	r22, 0xC8	; 200
     3ac:	70 e0       	ldi	r23, 0x00	; 0
     3ae:	80 e0       	ldi	r24, 0x00	; 0
     3b0:	90 e0       	ldi	r25, 0x00	; 0
     3b2:	0e 94 e1 00 	call	0x1c2	;  0x1c2
     3b6:	60 e0       	ldi	r22, 0x00	; 0
     3b8:	89 e0       	ldi	r24, 0x09	; 9
     3ba:	0e 94 70 00 	call	0xe0	;  0xe0
     3be:	64 e6       	ldi	r22, 0x64	; 100
     3c0:	70 e0       	ldi	r23, 0x00	; 0
     3c2:	80 e0       	ldi	r24, 0x00	; 0
     3c4:	90 e0       	ldi	r25, 0x00	; 0
     3c6:	0e 94 e1 00 	call	0x1c2	;  0x1c2
     3ca:	61 e0       	ldi	r22, 0x01	; 1
     3cc:	89 e0       	ldi	r24, 0x09	; 9
     3ce:	0e 94 70 00 	call	0xe0	;  0xe0
     3d2:	60 e9       	ldi	r22, 0x90	; 144
     3d4:	71 e0       	ldi	r23, 0x01	; 1
     3d6:	80 e0       	ldi	r24, 0x00	; 0
     3d8:	90 e0       	ldi	r25, 0x00	; 0
     3da:	0e 94 e1 00 	call	0x1c2	;  0x1c2
     3de:	60 e0       	ldi	r22, 0x00	; 0
     3e0:	89 e0       	ldi	r24, 0x09	; 9
     3e2:	0e 94 70 00 	call	0xe0	;  0xe0
     3e6:	64 e6       	ldi	r22, 0x64	; 100
     3e8:	70 e0       	ldi	r23, 0x00	; 0
     3ea:	80 e0       	ldi	r24, 0x00	; 0
     3ec:	90 e0       	ldi	r25, 0x00	; 0
     3ee:	0e 94 e1 00 	call	0x1c2	;  0x1c2
     3f2:	20 97       	sbiw	r28, 0x00	; 0
     3f4:	11 f2       	breq	.-124    	;  0x37a
     3f6:	0e 94 00 00 	call	0	;  0x0
     3fa:	bf cf       	rjmp	.-130    	;  0x37a
     3fc:	f8 94       	cli
     3fe:	ff cf       	rjmp	.-2      	;  0x3fe
     400:	90 e0       	ldi	r25, 0x00	; 0
     402:	0e 94 e1 00 	call	0x1c2	;  0x1c2
     406:	60 e0       	ldi	r22, 0x00	; 0
     408:	89 e0       	ldi	r24, 0x09	; 9
     40a:	0e 94 70 00 	call	0xe0	;  0xe0
     40e:	64 e6       	ldi	r22, 0x64	; 100
     410:	70 e0       	ldi	r23, 0x00	; 0
     412:	80 e0       	ldi	r24, 0x00	; 0
     414:	90 e0       	ldi	r25, 0x00	; 0
     416:	0e 94 e1 00 	call	0x1c2	;  0x1c2
     41a:	20 97       	sbiw	r28, 0x00	; 0
     41c:	09 f4       	brne	.+2      	;  0x420
     41e:	ad cf       	rjmp	.-166    	;  0x37a
     420:	0e 94 00 00 	call	0	;  0x0
     424:	aa cf       	rjmp	.-172    	;  0x37a
     426:	f8 94       	cli
     428:	ff cf       	rjmp	.-2      	;  0x428
     42a:	ff ff       	.word	0xffff	; ????
     42c:	ff ff       	.word	0xffff	; ????
     42e:	ff ff       	.word	0xffff	; ????
     430:	ff ff       	.word	0xffff	; ????
     432:	ff ff       	.word	0xffff	; ????
     434:	ff ff       	.word	0xffff	; ????
     436:	ff ff       	.word	0xffff	; ????
     438:	ff ff       	.word	0xffff	; ????
     43a:	ff ff       	.word	0xffff	; ????
     43c:	ff ff       	.word	0xffff	; ????
     43e:	ff ff       	.word	0xffff	; ????
     440:	ff ff       	.word	0xffff	; ????
     442:	ff ff       	.word	0xffff	; ????
     444:	ff ff       	.word	0xffff	; ????
     446:	ff ff       	.word	0xffff	; ????
     448:	ff ff       	.word	0xffff	; ????
     44a:	ff ff       	.word	0xffff	; ????
     44c:	ff ff       	.word	0xffff	; ????
     44e:	ff ff       	.word	0xffff	; ????
     450:	ff ff       	.word	0xffff	; ????
     452:	ff ff       	.word	0xffff	; ????
     454:	ff ff       	.word	0xffff	; ????
     456:	ff ff       	.word	0xffff	; ????
     458:	ff ff       	.word	0xffff	; ????
     45a:	ff ff       	.word	0xffff	; ????
     45c:	ff ff       	.word	0xffff	; ????
     45e:	ff ff       	.word	0xffff	; ????
     460:	ff ff       	.word	0xffff	; ????
     462:	ff ff       	.word	0xffff	; ????
     464:	ff ff       	.word	0xffff	; ????
     466:	ff ff       	.word	0xffff	; ????
     468:	ff ff       	.word	0xffff	; ????
     46a:	ff ff       	.word	0xffff	; ????
     46c:	ff ff       	.word	0xffff	; ????
     46e:	ff ff       	.word	0xffff	; ????
     470:	ff ff       	.word	0xffff	; ????
     472:	ff ff       	.word	0xffff	; ????
     474:	ff ff       	.word	0xffff	; ????
     476:	ff ff       	.word	0xffff	; ????
     478:	ff ff       	.word	0xffff	; ????
     47a:	ff ff       	.word	0xffff	; ????
     47c:	ff ff       	.word	0xffff	; ????
     47e:	ff ff       	.word	0xffff	; ????
     480:	af 01       	movw	r20, r30
     482:	48 1b       	sub	r20, r24
     484:	59 0b       	sbc	r21, r25
     486:	bc 01       	movw	r22, r24
     488:	8f e4       	ldi	r24, 0x4F	; 79
     48a:	91 e0       	ldi	r25, 0x01	; 1
     48c:	0c 94 2e 01 	jmp	0x25c	;  0x25c
     490:	8f 92       	push	r8
     492:	9f 92       	push	r9
     494:	af 92       	push	r10
     496:	bf 92       	push	r11
     498:	0f 93       	push	r16
     49a:	1f 93       	push	r17
     49c:	cf 93       	push	r28
     49e:	df 93       	push	r29
     4a0:	cd b7       	in	r28, 0x3d	; 61
     4a2:	de b7       	in	r29, 0x3e	; 62
     4a4:	a1 97       	sbiw	r28, 0x21	; 33
     4a6:	0f b6       	in	r0, 0x3f	; 63
     4a8:	f8 94       	cli
     4aa:	de bf       	out	0x3e, r29	; 62
     4ac:	0f be       	out	0x3f, r0	; 63
     4ae:	cd bf       	out	0x3d, r28	; 61
     4b0:	19 a2       	std	Y+33, r1	; 0x21
     4b2:	42 30       	cpi	r20, 0x02	; 2
     4b4:	08 f4       	brcc	.+2      	;  0x4b8
     4b6:	4a e0       	ldi	r20, 0x0A	; 10
     4b8:	8e 01       	movw	r16, r28
     4ba:	0f 5d       	subi	r16, 0xDF	; 223
     4bc:	1f 4f       	sbci	r17, 0xFF	; 255
     4be:	84 2e       	mov	r8, r20
     4c0:	91 2c       	mov	r9, r1
     4c2:	b1 2c       	mov	r11, r1
     4c4:	a1 2c       	mov	r10, r1
     4c6:	a5 01       	movw	r20, r10
     4c8:	94 01       	movw	r18, r8
     4ca:	0e 94 63 07 	call	0xec6	;  0xec6
     4ce:	e6 2f       	mov	r30, r22
     4d0:	b9 01       	movw	r22, r18
     4d2:	ca 01       	movw	r24, r20
     4d4:	ea 30       	cpi	r30, 0x0A	; 10
     4d6:	f4 f4       	brge	.+60     	;  0x514
     4d8:	e0 5d       	subi	r30, 0xD0	; 208
     4da:	d8 01       	movw	r26, r16
     4dc:	ee 93       	st	-X, r30
     4de:	8d 01       	movw	r16, r26
     4e0:	23 2b       	or	r18, r19
     4e2:	24 2b       	or	r18, r20
     4e4:	25 2b       	or	r18, r21
     4e6:	79 f7       	brne	.-34     	;  0x4c6
     4e8:	90 e0       	ldi	r25, 0x00	; 0
     4ea:	80 e0       	ldi	r24, 0x00	; 0
     4ec:	10 97       	sbiw	r26, 0x00	; 0
     4ee:	19 f0       	breq	.+6      	;  0x4f6
     4f0:	cd 01       	movw	r24, r26
     4f2:	0e 94 3b 02 	call	0x476	;  0x476
     4f6:	a1 96       	adiw	r28, 0x21	; 33
     4f8:	0f b6       	in	r0, 0x3f	; 63
     4fa:	f8 94       	cli
     4fc:	de bf       	out	0x3e, r29	; 62
     4fe:	0f be       	out	0x3f, r0	; 63
     500:	cd bf       	out	0x3d, r28	; 61
     502:	df 91       	pop	r29
     504:	cf 91       	pop	r28
     506:	1f 91       	pop	r17
     508:	0f 91       	pop	r16
     50a:	bf 90       	pop	r11
     50c:	af 90       	pop	r10
     50e:	9f 90       	pop	r9
     510:	8f 90       	pop	r8
     512:	08 95       	ret
     514:	e9 5c       	subi	r30, 0xC9	; 201
     516:	e1 cf       	rjmp	.-62     	;  0x4da
     518:	1f 92       	push	r1
     51a:	0f 92       	push	r0
     51c:	0f b6       	in	r0, 0x3f	; 63
     51e:	0f 92       	push	r0
     520:	11 24       	eor	r1, r1
     522:	2f 93       	push	r18
     524:	3f 93       	push	r19
     526:	8f 93       	push	r24
     528:	9f 93       	push	r25
     52a:	af 93       	push	r26
     52c:	bf 93       	push	r27
     52e:	80 91 47 01 	lds	r24, 0x0147	;  0x800147
     532:	90 91 48 01 	lds	r25, 0x0148	;  0x800148
     536:	a0 91 49 01 	lds	r26, 0x0149	;  0x800149
     53a:	b0 91 4a 01 	lds	r27, 0x014A	;  0x80014a
     53e:	30 91 46 01 	lds	r19, 0x0146	;  0x800146
     542:	23 e0       	ldi	r18, 0x03	; 3
     544:	23 0f       	add	r18, r19
     546:	2d 37       	cpi	r18, 0x7D	; 125
     548:	58 f5       	brcc	.+86     	;  0x5a0
     54a:	01 96       	adiw	r24, 0x01	; 1
     54c:	a1 1d       	adc	r26, r1
     54e:	b1 1d       	adc	r27, r1
     550:	20 93 46 01 	sts	0x0146, r18	;  0x800146
     554:	80 93 47 01 	sts	0x0147, r24	;  0x800147
     558:	90 93 48 01 	sts	0x0148, r25	;  0x800148
     55c:	a0 93 49 01 	sts	0x0149, r26	;  0x800149
     560:	b0 93 4a 01 	sts	0x014A, r27	;  0x80014a
     564:	80 91 4b 01 	lds	r24, 0x014B	;  0x80014b
     568:	90 91 4c 01 	lds	r25, 0x014C	;  0x80014c
     56c:	a0 91 4d 01 	lds	r26, 0x014D	;  0x80014d
     570:	b0 91 4e 01 	lds	r27, 0x014E	;  0x80014e
     574:	01 96       	adiw	r24, 0x01	; 1
     576:	a1 1d       	adc	r26, r1
     578:	b1 1d       	adc	r27, r1
     57a:	80 93 4b 01 	sts	0x014B, r24	;  0x80014b
     57e:	90 93 4c 01 	sts	0x014C, r25	;  0x80014c
     582:	a0 93 4d 01 	sts	0x014D, r26	;  0x80014d
     586:	b0 93 4e 01 	sts	0x014E, r27	;  0x80014e
     58a:	bf 91       	pop	r27
     58c:	af 91       	pop	r26
     58e:	9f 91       	pop	r25
     590:	8f 91       	pop	r24
     592:	3f 91       	pop	r19
     594:	2f 91       	pop	r18
     596:	0f 90       	pop	r0
     598:	0f be       	out	0x3f, r0	; 63
     59a:	0f 90       	pop	r0
     59c:	1f 90       	pop	r1
     59e:	18 95       	reti
     5a0:	26 e8       	ldi	r18, 0x86	; 134
     5a2:	23 0f       	add	r18, r19
     5a4:	02 96       	adiw	r24, 0x02	; 2
     5a6:	a1 1d       	adc	r26, r1
     5a8:	b1 1d       	adc	r27, r1
     5aa:	d2 cf       	rjmp	.-92     	;  0x550
     5ac:	1f 92       	push	r1
     5ae:	0f 92       	push	r0
     5b0:	0f b6       	in	r0, 0x3f	; 63
     5b2:	0f 92       	push	r0
     5b4:	11 24       	eor	r1, r1
     5b6:	2f 93       	push	r18
     5b8:	3f 93       	push	r19
     5ba:	4f 93       	push	r20
     5bc:	5f 93       	push	r21
     5be:	6f 93       	push	r22
     5c0:	7f 93       	push	r23
     5c2:	8f 93       	push	r24
     5c4:	9f 93       	push	r25
     5c6:	af 93       	push	r26
     5c8:	bf 93       	push	r27
     5ca:	ef 93       	push	r30
     5cc:	ff 93       	push	r31
     5ce:	8f e4       	ldi	r24, 0x4F	; 79
     5d0:	91 e0       	ldi	r25, 0x01	; 1
     5d2:	0e 94 ac 01 	call	0x358	;  0x358
     5d6:	ff 91       	pop	r31
     5d8:	ef 91       	pop	r30
     5da:	bf 91       	pop	r27
     5dc:	af 91       	pop	r26
     5de:	9f 91       	pop	r25
     5e0:	8f 91       	pop	r24
     5e2:	7f 91       	pop	r23
     5e4:	6f 91       	pop	r22
     5e6:	5f 91       	pop	r21
     5e8:	4f 91       	pop	r20
     5ea:	3f 91       	pop	r19
     5ec:	2f 91       	pop	r18
     5ee:	0f 90       	pop	r0
     5f0:	0f be       	out	0x3f, r0	; 63
     5f2:	0f 90       	pop	r0
     5f4:	1f 90       	pop	r1
     5f6:	18 95       	reti
     5f8:	1f 92       	push	r1
     5fa:	0f 92       	push	r0
     5fc:	0f b6       	in	r0, 0x3f	; 63
     5fe:	0f 92       	push	r0
     600:	11 24       	eor	r1, r1
     602:	2f 93       	push	r18
     604:	8f 93       	push	r24
     606:	9f 93       	push	r25
     608:	ef 93       	push	r30
     60a:	ff 93       	push	r31
     60c:	e0 91 5f 01 	lds	r30, 0x015F	;  0x80015f
     610:	f0 91 60 01 	lds	r31, 0x0160	;  0x800160
     614:	80 81       	ld	r24, Z
     616:	e0 91 65 01 	lds	r30, 0x0165	;  0x800165
     61a:	f0 91 66 01 	lds	r31, 0x0166	;  0x800166
     61e:	82 fd       	sbrc	r24, 2
     620:	1b c0       	rjmp	.+54     	;  0x658
     622:	90 81       	ld	r25, Z
     624:	80 91 68 01 	lds	r24, 0x0168	;  0x800168
     628:	8f 5f       	subi	r24, 0xFF	; 255
     62a:	8f 73       	andi	r24, 0x3F	; 63
     62c:	20 91 69 01 	lds	r18, 0x0169	;  0x800169
     630:	82 17       	cp	r24, r18
     632:	41 f0       	breq	.+16     	;  0x644
     634:	e0 91 68 01 	lds	r30, 0x0168	;  0x800168
     638:	f0 e0       	ldi	r31, 0x00	; 0
     63a:	e1 5b       	subi	r30, 0xB1	; 177
     63c:	fe 4f       	sbci	r31, 0xFE	; 254
     63e:	95 8f       	std	Z+29, r25	; 0x1d
     640:	80 93 68 01 	sts	0x0168, r24	;  0x800168
     644:	ff 91       	pop	r31
     646:	ef 91       	pop	r30
     648:	9f 91       	pop	r25
     64a:	8f 91       	pop	r24
     64c:	2f 91       	pop	r18
     64e:	0f 90       	pop	r0
     650:	0f be       	out	0x3f, r0	; 63
     652:	0f 90       	pop	r0
     654:	1f 90       	pop	r1
     656:	18 95       	reti
     658:	80 81       	ld	r24, Z
     65a:	f4 cf       	rjmp	.-24     	;  0x644
     65c:	78 94       	sei
     65e:	84 b5       	in	r24, 0x24	; 36
     660:	82 60       	ori	r24, 0x02	; 2
     662:	84 bd       	out	0x24, r24	; 36
     664:	84 b5       	in	r24, 0x24	; 36
     666:	81 60       	ori	r24, 0x01	; 1
     668:	84 bd       	out	0x24, r24	; 36
     66a:	85 b5       	in	r24, 0x25	; 37
     66c:	82 60       	ori	r24, 0x02	; 2
     66e:	85 bd       	out	0x25, r24	; 37
     670:	85 b5       	in	r24, 0x25	; 37
     672:	81 60       	ori	r24, 0x01	; 1
     674:	85 bd       	out	0x25, r24	; 37
     676:	80 91 6e 00 	lds	r24, 0x006E	;  0x80006e
     67a:	81 60       	ori	r24, 0x01	; 1
     67c:	80 93 6e 00 	sts	0x006E, r24	;  0x80006e
     680:	10 92 81 00 	sts	0x0081, r1	;  0x800081
     684:	80 91 81 00 	lds	r24, 0x0081	;  0x800081
     688:	82 60       	ori	r24, 0x02	; 2
     68a:	80 93 81 00 	sts	0x0081, r24	;  0x800081
     68e:	80 91 81 00 	lds	r24, 0x0081	;  0x800081
     692:	81 60       	ori	r24, 0x01	; 1
     694:	80 93 81 00 	sts	0x0081, r24	;  0x800081
     698:	80 91 80 00 	lds	r24, 0x0080	;  0x800080
     69c:	81 60       	ori	r24, 0x01	; 1
     69e:	80 93 80 00 	sts	0x0080, r24	;  0x800080
     6a2:	80 91 b1 00 	lds	r24, 0x00B1	;  0x8000b1
     6a6:	84 60       	ori	r24, 0x04	; 4
     6a8:	80 93 b1 00 	sts	0x00B1, r24	;  0x8000b1
     6ac:	80 91 b0 00 	lds	r24, 0x00B0	;  0x8000b0
     6b0:	81 60       	ori	r24, 0x01	; 1
     6b2:	80 93 b0 00 	sts	0x00B0, r24	;  0x8000b0
     6b6:	80 91 7a 00 	lds	r24, 0x007A	;  0x80007a
     6ba:	84 60       	ori	r24, 0x04	; 4
     6bc:	80 93 7a 00 	sts	0x007A, r24	;  0x80007a
     6c0:	80 91 7a 00 	lds	r24, 0x007A	;  0x80007a
     6c4:	82 60       	ori	r24, 0x02	; 2
     6c6:	80 93 7a 00 	sts	0x007A, r24	;  0x80007a
     6ca:	80 91 7a 00 	lds	r24, 0x007A	;  0x80007a
     6ce:	81 60       	ori	r24, 0x01	; 1
     6d0:	80 93 7a 00 	sts	0x007A, r24	;  0x80007a
     6d4:	80 91 7a 00 	lds	r24, 0x007A	;  0x80007a
     6d8:	80 68       	ori	r24, 0x80	; 128
     6da:	80 93 7a 00 	sts	0x007A, r24	;  0x80007a
     6de:	10 92 c1 00 	sts	0x00C1, r1	;  0x8000c1
     6e2:	ee e9       	ldi	r30, 0x9E	; 158
     6e4:	f0 e0       	ldi	r31, 0x00	; 0
     6e6:	24 91       	lpm	r18, Z
     6e8:	ea e8       	ldi	r30, 0x8A	; 138
     6ea:	f0 e0       	ldi	r31, 0x00	; 0
     6ec:	84 91       	lpm	r24, Z
     6ee:	88 23       	and	r24, r24
     6f0:	c1 f0       	breq	.+48     	;  0x722
     6f2:	90 e0       	ldi	r25, 0x00	; 0
     6f4:	88 0f       	add	r24, r24
     6f6:	99 1f       	adc	r25, r25
     6f8:	fc 01       	movw	r30, r24
     6fa:	e8 59       	subi	r30, 0x98	; 152
     6fc:	ff 4f       	sbci	r31, 0xFF	; 255
     6fe:	c5 91       	lpm	r28, Z+
     700:	d4 91       	lpm	r29, Z
     702:	fc 01       	movw	r30, r24
     704:	ee 58       	subi	r30, 0x8E	; 142
     706:	ff 4f       	sbci	r31, 0xFF	; 255
     708:	a5 91       	lpm	r26, Z+
     70a:	b4 91       	lpm	r27, Z
     70c:	9f b7       	in	r25, 0x3f	; 63
     70e:	f8 94       	cli
     710:	88 81       	ld	r24, Y
     712:	e2 2f       	mov	r30, r18
     714:	e0 95       	com	r30
     716:	8e 23       	and	r24, r30
     718:	88 83       	st	Y, r24
     71a:	8c 91       	ld	r24, X
     71c:	e8 23       	and	r30, r24
     71e:	ec 93       	st	X, r30
     720:	9f bf       	out	0x3f, r25	; 63
     722:	ed e9       	ldi	r30, 0x9D	; 157
     724:	f0 e0       	ldi	r31, 0x00	; 0
     726:	24 91       	lpm	r18, Z
     728:	e9 e8       	ldi	r30, 0x89	; 137
     72a:	f0 e0       	ldi	r31, 0x00	; 0
     72c:	84 91       	lpm	r24, Z
     72e:	88 23       	and	r24, r24
     730:	99 f0       	breq	.+38     	;  0x758
     732:	90 e0       	ldi	r25, 0x00	; 0
     734:	88 0f       	add	r24, r24
     736:	99 1f       	adc	r25, r25
     738:	fc 01       	movw	r30, r24
     73a:	e8 59       	subi	r30, 0x98	; 152
     73c:	ff 4f       	sbci	r31, 0xFF	; 255
     73e:	a5 91       	lpm	r26, Z+
     740:	b4 91       	lpm	r27, Z
     742:	fc 01       	movw	r30, r24
     744:	ee 58       	subi	r30, 0x8E	; 142
     746:	ff 4f       	sbci	r31, 0xFF	; 255
     748:	85 91       	lpm	r24, Z+
     74a:	94 91       	lpm	r25, Z
     74c:	8f b7       	in	r24, 0x3f	; 63
     74e:	f8 94       	cli
     750:	ec 91       	ld	r30, X
     752:	e2 2b       	or	r30, r18
     754:	ec 93       	st	X, r30
     756:	8f bf       	out	0x3f, r24	; 63
     758:	e0 91 5f 01 	lds	r30, 0x015F	;  0x80015f
     75c:	f0 91 60 01 	lds	r31, 0x0160	;  0x800160
     760:	82 e0       	ldi	r24, 0x02	; 2
     762:	80 83       	st	Z, r24
     764:	e0 91 5b 01 	lds	r30, 0x015B	;  0x80015b
     768:	f0 91 5c 01 	lds	r31, 0x015C	;  0x80015c
     76c:	10 82       	st	Z, r1
     76e:	e0 91 5d 01 	lds	r30, 0x015D	;  0x80015d
     772:	f0 91 5e 01 	lds	r31, 0x015E	;  0x80015e
     776:	8f ec       	ldi	r24, 0xCF	; 207
     778:	80 83       	st	Z, r24
     77a:	10 92 67 01 	sts	0x0167, r1	;  0x800167
     77e:	e0 91 63 01 	lds	r30, 0x0163	;  0x800163
     782:	f0 91 64 01 	lds	r31, 0x0164	;  0x800164
     786:	86 e0       	ldi	r24, 0x06	; 6
     788:	80 83       	st	Z, r24
     78a:	e0 91 61 01 	lds	r30, 0x0161	;  0x800161
     78e:	f0 91 62 01 	lds	r31, 0x0162	;  0x800162
     792:	80 81       	ld	r24, Z
     794:	80 61       	ori	r24, 0x10	; 16
     796:	80 83       	st	Z, r24
     798:	e0 91 61 01 	lds	r30, 0x0161	;  0x800161
     79c:	f0 91 62 01 	lds	r31, 0x0162	;  0x800162
     7a0:	80 81       	ld	r24, Z
     7a2:	88 60       	ori	r24, 0x08	; 8
     7a4:	80 83       	st	Z, r24
     7a6:	e0 91 61 01 	lds	r30, 0x0161	;  0x800161
     7aa:	f0 91 62 01 	lds	r31, 0x0162	;  0x800162
     7ae:	80 81       	ld	r24, Z
     7b0:	80 68       	ori	r24, 0x80	; 128
     7b2:	80 83       	st	Z, r24
     7b4:	e0 91 61 01 	lds	r30, 0x0161	;  0x800161
     7b8:	f0 91 62 01 	lds	r31, 0x0162	;  0x800162
     7bc:	80 81       	ld	r24, Z
     7be:	8f 7d       	andi	r24, 0xDF	; 223
     7c0:	80 83       	st	Z, r24
     7c2:	10 e4       	ldi	r17, 0x40	; 64
     7c4:	c0 e0       	ldi	r28, 0x00	; 0
     7c6:	d0 e0       	ldi	r29, 0x00	; 0
     7c8:	61 e0       	ldi	r22, 0x01	; 1
     7ca:	8d e0       	ldi	r24, 0x0D	; 13
     7cc:	0e 94 87 00 	call	0x10e	;  0x10e
     7d0:	10 93 7c 00 	sts	0x007C, r17	;  0x80007c
     7d4:	80 91 7a 00 	lds	r24, 0x007A	;  0x80007a
     7d8:	80 64       	ori	r24, 0x40	; 64
     7da:	80 93 7a 00 	sts	0x007A, r24	;  0x80007a
     7de:	80 91 7a 00 	lds	r24, 0x007A	;  0x80007a
     7e2:	86 fd       	sbrc	r24, 6
     7e4:	fc cf       	rjmp	.-8      	;  0x7de
     7e6:	60 91 78 00 	lds	r22, 0x0078	;  0x800078
     7ea:	70 91 79 00 	lds	r23, 0x0079	;  0x800079
     7ee:	70 93 45 01 	sts	0x0145, r23	;  0x800145
     7f2:	60 93 44 01 	sts	0x0144, r22	;  0x800144
     7f6:	07 2e       	mov	r0, r23
     7f8:	00 0c       	add	r0, r0
     7fa:	88 0b       	sbc	r24, r24
     7fc:	99 0b       	sbc	r25, r25
     7fe:	0e 94 3c 06 	call	0xc78	;  0xc78
     802:	20 e0       	ldi	r18, 0x00	; 0
     804:	30 ec       	ldi	r19, 0xC0	; 192
     806:	4f e7       	ldi	r20, 0x7F	; 127
     808:	54 e4       	ldi	r21, 0x44	; 68
     80a:	0e 94 99 05 	call	0xb32	;  0xb32
     80e:	20 e0       	ldi	r18, 0x00	; 0
     810:	30 e0       	ldi	r19, 0x00	; 0
     812:	40 ea       	ldi	r20, 0xA0	; 160
     814:	50 e4       	ldi	r21, 0x40	; 64
     816:	0e 94 f1 06 	call	0xde2	;  0xde2
     81a:	60 93 40 01 	sts	0x0140, r22	;  0x800140
     81e:	70 93 41 01 	sts	0x0141, r23	;  0x800141
     822:	80 93 42 01 	sts	0x0142, r24	;  0x800142
     826:	90 93 43 01 	sts	0x0143, r25	;  0x800143
     82a:	82 e1       	ldi	r24, 0x12	; 18
     82c:	91 e0       	ldi	r25, 0x01	; 1
     82e:	0e 94 3b 02 	call	0x476	;  0x476
     832:	c0 90 44 01 	lds	r12, 0x0144	;  0x800144
     836:	d0 90 45 01 	lds	r13, 0x0145	;  0x800145
     83a:	0d 2c       	mov	r0, r13
     83c:	00 0c       	add	r0, r0
     83e:	ee 08       	sbc	r14, r14
     840:	ff 08       	sbc	r15, r15
     842:	4a e0       	ldi	r20, 0x0A	; 10
     844:	c7 01       	movw	r24, r14
     846:	b6 01       	movw	r22, r12
     848:	f7 fe       	sbrs	r15, 7
     84a:	0d c0       	rjmp	.+26     	;  0x866
     84c:	6d e2       	ldi	r22, 0x2D	; 45
     84e:	8f e4       	ldi	r24, 0x4F	; 79
     850:	91 e0       	ldi	r25, 0x01	; 1
     852:	0e 94 ce 01 	call	0x39c	;  0x39c
     856:	66 27       	eor	r22, r22
     858:	77 27       	eor	r23, r23
     85a:	cb 01       	movw	r24, r22
     85c:	6c 19       	sub	r22, r12
     85e:	7d 09       	sbc	r23, r13
     860:	8e 09       	sbc	r24, r14
     862:	9f 09       	sbc	r25, r15
     864:	4a e0       	ldi	r20, 0x0A	; 10
     866:	0e 94 48 02 	call	0x490	;  0x490
     86a:	84 e2       	ldi	r24, 0x24	; 36
     86c:	91 e0       	ldi	r25, 0x01	; 1
     86e:	0e 94 3b 02 	call	0x476	;  0x476
     872:	80 e3       	ldi	r24, 0x30	; 48
     874:	91 e0       	ldi	r25, 0x01	; 1
     876:	0e 94 3b 02 	call	0x476	;  0x476
     87a:	c0 90 40 01 	lds	r12, 0x0140	;  0x800140
     87e:	d0 90 41 01 	lds	r13, 0x0141	;  0x800141
     882:	e0 90 42 01 	lds	r14, 0x0142	;  0x800142
     886:	f0 90 43 01 	lds	r15, 0x0143	;  0x800143
     88a:	a7 01       	movw	r20, r14
     88c:	96 01       	movw	r18, r12
     88e:	c7 01       	movw	r24, r14
     890:	b6 01       	movw	r22, r12
     892:	0e 94 5e 07 	call	0xebc	;  0xebc
     896:	88 23       	and	r24, r24
     898:	d9 f0       	breq	.+54     	;  0x8d0
     89a:	83 e3       	ldi	r24, 0x33	; 51
     89c:	91 e0       	ldi	r25, 0x01	; 1
     89e:	0e 94 3b 02 	call	0x476	;  0x476
     8a2:	80 e3       	ldi	r24, 0x30	; 48
     8a4:	91 e0       	ldi	r25, 0x01	; 1
     8a6:	0e 94 3b 02 	call	0x476	;  0x476
     8aa:	0e 94 f8 00 	call	0x1f0	;  0x1f0
     8ae:	60 e0       	ldi	r22, 0x00	; 0
     8b0:	8d e0       	ldi	r24, 0x0D	; 13
     8b2:	0e 94 87 00 	call	0x10e	;  0x10e
     8b6:	0e 94 f8 00 	call	0x1f0	;  0x1f0
     8ba:	20 97       	sbiw	r28, 0x00	; 0
     8bc:	09 f4       	brne	.+2      	;  0x8c0
     8be:	84 cf       	rjmp	.-248    	;  0x7c8
     8c0:	0e 94 98 01 	call	0x330	;  0x330
     8c4:	88 23       	and	r24, r24
     8c6:	09 f4       	brne	.+2      	;  0x8ca
     8c8:	7f cf       	rjmp	.-258    	;  0x7c8
     8ca:	0e 94 00 00 	call	0	;  0x0
     8ce:	7c cf       	rjmp	.-264    	;  0x7c8
     8d0:	46 01       	movw	r8, r12
     8d2:	57 01       	movw	r10, r14
     8d4:	e8 94       	clt
     8d6:	b7 f8       	bld	r11, 7
     8d8:	2f ef       	ldi	r18, 0xFF	; 255
     8da:	3f ef       	ldi	r19, 0xFF	; 255
     8dc:	4f e7       	ldi	r20, 0x7F	; 127
     8de:	5f e7       	ldi	r21, 0x7F	; 127
     8e0:	c5 01       	movw	r24, r10
     8e2:	b4 01       	movw	r22, r8
     8e4:	0e 94 5e 07 	call	0xebc	;  0xebc
     8e8:	81 11       	cpse	r24, r1
     8ea:	0d c0       	rjmp	.+26     	;  0x906
     8ec:	2f ef       	ldi	r18, 0xFF	; 255
     8ee:	3f ef       	ldi	r19, 0xFF	; 255
     8f0:	4f e7       	ldi	r20, 0x7F	; 127
     8f2:	5f e7       	ldi	r21, 0x7F	; 127
     8f4:	c5 01       	movw	r24, r10
     8f6:	b4 01       	movw	r22, r8
     8f8:	0e 94 94 05 	call	0xb28	;  0xb28
     8fc:	18 16       	cp	r1, r24
     8fe:	1c f4       	brge	.+6      	;  0x906
     900:	87 e3       	ldi	r24, 0x37	; 55
     902:	91 e0       	ldi	r25, 0x01	; 1
     904:	cc cf       	rjmp	.-104    	;  0x89e
     906:	2f ef       	ldi	r18, 0xFF	; 255
     908:	3f ef       	ldi	r19, 0xFF	; 255
     90a:	4f e7       	ldi	r20, 0x7F	; 127
     90c:	5f e4       	ldi	r21, 0x4F	; 79
     90e:	c7 01       	movw	r24, r14
     910:	b6 01       	movw	r22, r12
     912:	0e 94 ec 06 	call	0xdd8	;  0xdd8
     916:	18 16       	cp	r1, r24
     918:	1c f4       	brge	.+6      	;  0x920
     91a:	8b e3       	ldi	r24, 0x3B	; 59
     91c:	91 e0       	ldi	r25, 0x01	; 1
     91e:	bf cf       	rjmp	.-130    	;  0x89e
     920:	2f ef       	ldi	r18, 0xFF	; 255
     922:	3f ef       	ldi	r19, 0xFF	; 255
     924:	4f e7       	ldi	r20, 0x7F	; 127
     926:	5f ec       	ldi	r21, 0xCF	; 207
     928:	c7 01       	movw	r24, r14
     92a:	b6 01       	movw	r22, r12
     92c:	0e 94 94 05 	call	0xb28	;  0xb28
     930:	87 fd       	sbrc	r24, 7
     932:	f3 cf       	rjmp	.-26     	;  0x91a
     934:	20 e0       	ldi	r18, 0x00	; 0
     936:	30 e0       	ldi	r19, 0x00	; 0
     938:	a9 01       	movw	r20, r18
     93a:	c7 01       	movw	r24, r14
     93c:	b6 01       	movw	r22, r12
     93e:	0e 94 94 05 	call	0xb28	;  0xb28
     942:	87 ff       	sbrs	r24, 7
     944:	09 c0       	rjmp	.+18     	;  0x958
     946:	6d e2       	ldi	r22, 0x2D	; 45
     948:	8f e4       	ldi	r24, 0x4F	; 79
     94a:	91 e0       	ldi	r25, 0x01	; 1
     94c:	0e 94 ce 01 	call	0x39c	;  0x39c
     950:	f7 fa       	bst	r15, 7
     952:	f0 94       	com	r15
     954:	f7 f8       	bld	r15, 7
     956:	f0 94       	com	r15
     958:	2a e0       	ldi	r18, 0x0A	; 10
     95a:	37 ed       	ldi	r19, 0xD7	; 215
     95c:	43 ea       	ldi	r20, 0xA3	; 163
     95e:	5b e3       	ldi	r21, 0x3B	; 59
     960:	c7 01       	movw	r24, r14
     962:	b6 01       	movw	r22, r12
     964:	0e 94 28 05 	call	0xa50	;  0xa50
     968:	4b 01       	movw	r8, r22
     96a:	5c 01       	movw	r10, r24
     96c:	0e 94 0b 06 	call	0xc16	;  0xc16
     970:	6b 01       	movw	r12, r22
     972:	7c 01       	movw	r14, r24
     974:	0e 94 3a 06 	call	0xc74	;  0xc74
     978:	9b 01       	movw	r18, r22
     97a:	ac 01       	movw	r20, r24
     97c:	c5 01       	movw	r24, r10
     97e:	b4 01       	movw	r22, r8
     980:	0e 94 27 05 	call	0xa4e	;  0xa4e
     984:	4b 01       	movw	r8, r22
     986:	5c 01       	movw	r10, r24
     988:	4a e0       	ldi	r20, 0x0A	; 10
     98a:	c7 01       	movw	r24, r14
     98c:	b6 01       	movw	r22, r12
     98e:	0e 94 48 02 	call	0x490	;  0x490
     992:	6e e2       	ldi	r22, 0x2E	; 46
     994:	8f e4       	ldi	r24, 0x4F	; 79
     996:	91 e0       	ldi	r25, 0x01	; 1
     998:	0e 94 ce 01 	call	0x39c	;  0x39c
     99c:	20 e0       	ldi	r18, 0x00	; 0
     99e:	30 e0       	ldi	r19, 0x00	; 0
     9a0:	40 e2       	ldi	r20, 0x20	; 32
     9a2:	51 e4       	ldi	r21, 0x41	; 65
     9a4:	c5 01       	movw	r24, r10
     9a6:	b4 01       	movw	r22, r8
     9a8:	0e 94 f1 06 	call	0xde2	;  0xde2
     9ac:	4b 01       	movw	r8, r22
     9ae:	5c 01       	movw	r10, r24
     9b0:	0e 94 0b 06 	call	0xc16	;  0xc16
     9b4:	6b 01       	movw	r12, r22
     9b6:	f1 2c       	mov	r15, r1
     9b8:	e1 2c       	mov	r14, r1
     9ba:	4a e0       	ldi	r20, 0x0A	; 10
     9bc:	c7 01       	movw	r24, r14
     9be:	b6 01       	movw	r22, r12
     9c0:	0e 94 48 02 	call	0x490	;  0x490
     9c4:	c7 01       	movw	r24, r14
     9c6:	b6 01       	movw	r22, r12
     9c8:	0e 94 3a 06 	call	0xc74	;  0xc74
     9cc:	9b 01       	movw	r18, r22
     9ce:	ac 01       	movw	r20, r24
     9d0:	c5 01       	movw	r24, r10
     9d2:	b4 01       	movw	r22, r8
     9d4:	0e 94 27 05 	call	0xa4e	;  0xa4e
     9d8:	20 e0       	ldi	r18, 0x00	; 0
     9da:	30 e0       	ldi	r19, 0x00	; 0
     9dc:	40 e2       	ldi	r20, 0x20	; 32
     9de:	51 e4       	ldi	r21, 0x41	; 65
     9e0:	0e 94 f1 06 	call	0xde2	;  0xde2
     9e4:	0e 94 0b 06 	call	0xc16	;  0xc16
     9e8:	90 e0       	ldi	r25, 0x00	; 0
     9ea:	80 e0       	ldi	r24, 0x00	; 0
     9ec:	4a e0       	ldi	r20, 0x0A	; 10
     9ee:	0e 94 48 02 	call	0x490	;  0x490
     9f2:	57 cf       	rjmp	.-338    	;  0x8a2
     9f4:	ef e4       	ldi	r30, 0x4F	; 79
     9f6:	f1 e0       	ldi	r31, 0x01	; 1
     9f8:	13 82       	std	Z+3, r1	; 0x03
     9fa:	12 82       	std	Z+2, r1	; 0x02
     9fc:	88 ee       	ldi	r24, 0xE8	; 232
     9fe:	93 e0       	ldi	r25, 0x03	; 3
     a00:	a0 e0       	ldi	r26, 0x00	; 0
     a02:	b0 e0       	ldi	r27, 0x00	; 0
     a04:	84 83       	std	Z+4, r24	; 0x04
     a06:	95 83       	std	Z+5, r25	; 0x05
     a08:	a6 83       	std	Z+6, r26	; 0x06
     a0a:	b7 83       	std	Z+7, r27	; 0x07
     a0c:	84 e0       	ldi	r24, 0x04	; 4
     a0e:	91 e0       	ldi	r25, 0x01	; 1
     a10:	91 83       	std	Z+1, r25	; 0x01
     a12:	80 83       	st	Z, r24
     a14:	85 ec       	ldi	r24, 0xC5	; 197
     a16:	90 e0       	ldi	r25, 0x00	; 0
     a18:	95 87       	std	Z+13, r25	; 0x0d
     a1a:	84 87       	std	Z+12, r24	; 0x0c
     a1c:	84 ec       	ldi	r24, 0xC4	; 196
     a1e:	90 e0       	ldi	r25, 0x00	; 0
     a20:	97 87       	std	Z+15, r25	; 0x0f
     a22:	86 87       	std	Z+14, r24	; 0x0e
     a24:	80 ec       	ldi	r24, 0xC0	; 192
     a26:	90 e0       	ldi	r25, 0x00	; 0
     a28:	91 8b       	std	Z+17, r25	; 0x11
     a2a:	80 8b       	std	Z+16, r24	; 0x10
     a2c:	81 ec       	ldi	r24, 0xC1	; 193
     a2e:	90 e0       	ldi	r25, 0x00	; 0
     a30:	93 8b       	std	Z+19, r25	; 0x13
     a32:	82 8b       	std	Z+18, r24	; 0x12
     a34:	82 ec       	ldi	r24, 0xC2	; 194
     a36:	90 e0       	ldi	r25, 0x00	; 0
     a38:	95 8b       	std	Z+21, r25	; 0x15
     a3a:	84 8b       	std	Z+20, r24	; 0x14
     a3c:	86 ec       	ldi	r24, 0xC6	; 198
     a3e:	90 e0       	ldi	r25, 0x00	; 0
     a40:	97 8b       	std	Z+23, r25	; 0x17
     a42:	86 8b       	std	Z+22, r24	; 0x16
     a44:	11 8e       	std	Z+25, r1	; 0x19
     a46:	12 8e       	std	Z+26, r1	; 0x1a
     a48:	13 8e       	std	Z+27, r1	; 0x1b
     a4a:	14 8e       	std	Z+28, r1	; 0x1c
     a4c:	08 95       	ret
     a4e:	50 58       	subi	r21, 0x80	; 128
     a50:	bb 27       	eor	r27, r27
     a52:	aa 27       	eor	r26, r26
     a54:	0e 94 3f 05 	call	0xa7e	;  0xa7e
     a58:	0c 94 b2 06 	jmp	0xd64	;  0xd64
     a5c:	0e 94 a4 06 	call	0xd48	;  0xd48
     a60:	38 f0       	brcs	.+14     	;  0xa70
     a62:	0e 94 ab 06 	call	0xd56	;  0xd56
     a66:	20 f0       	brcs	.+8      	;  0xa70
     a68:	39 f4       	brne	.+14     	;  0xa78
     a6a:	9f 3f       	cpi	r25, 0xFF	; 255
     a6c:	19 f4       	brne	.+6      	;  0xa74
     a6e:	26 f4       	brtc	.+8      	;  0xa78
     a70:	0c 94 a1 06 	jmp	0xd42	;  0xd42
     a74:	0e f4       	brtc	.+2      	;  0xa78
     a76:	e0 95       	com	r30
     a78:	e7 fb       	bst	r30, 7
     a7a:	0c 94 9b 06 	jmp	0xd36	;  0xd36
     a7e:	e9 2f       	mov	r30, r25
     a80:	0e 94 c3 06 	call	0xd86	;  0xd86
     a84:	58 f3       	brcs	.-42     	;  0xa5c
     a86:	ba 17       	cp	r27, r26
     a88:	62 07       	cpc	r22, r18
     a8a:	73 07       	cpc	r23, r19
     a8c:	84 07       	cpc	r24, r20
     a8e:	95 07       	cpc	r25, r21
     a90:	20 f0       	brcs	.+8      	;  0xa9a
     a92:	79 f4       	brne	.+30     	;  0xab2
     a94:	a6 f5       	brtc	.+104    	;  0xafe
     a96:	0c 94 e5 06 	jmp	0xdca	;  0xdca
     a9a:	0e f4       	brtc	.+2      	;  0xa9e
     a9c:	e0 95       	com	r30
     a9e:	0b 2e       	mov	r0, r27
     aa0:	ba 2f       	mov	r27, r26
     aa2:	a0 2d       	mov	r26, r0
     aa4:	0b 01       	movw	r0, r22
     aa6:	b9 01       	movw	r22, r18
     aa8:	90 01       	movw	r18, r0
     aaa:	0c 01       	movw	r0, r24
     aac:	ca 01       	movw	r24, r20
     aae:	a0 01       	movw	r20, r0
     ab0:	11 24       	eor	r1, r1
     ab2:	ff 27       	eor	r31, r31
     ab4:	59 1b       	sub	r21, r25
     ab6:	99 f0       	breq	.+38     	;  0xade
     ab8:	59 3f       	cpi	r21, 0xF9	; 249
     aba:	50 f4       	brcc	.+20     	;  0xad0
     abc:	50 3e       	cpi	r21, 0xE0	; 224
     abe:	68 f1       	brcs	.+90     	;  0xb1a
     ac0:	1a 16       	cp	r1, r26
     ac2:	f0 40       	sbci	r31, 0x00	; 0
     ac4:	a2 2f       	mov	r26, r18
     ac6:	23 2f       	mov	r18, r19
     ac8:	34 2f       	mov	r19, r20
     aca:	44 27       	eor	r20, r20
     acc:	58 5f       	subi	r21, 0xF8	; 248
     ace:	f3 cf       	rjmp	.-26     	;  0xab6
     ad0:	46 95       	lsr	r20
     ad2:	37 95       	ror	r19
     ad4:	27 95       	ror	r18
     ad6:	a7 95       	ror	r26
     ad8:	f0 40       	sbci	r31, 0x00	; 0
     ada:	53 95       	inc	r21
     adc:	c9 f7       	brne	.-14     	;  0xad0
     ade:	7e f4       	brtc	.+30     	;  0xafe
     ae0:	1f 16       	cp	r1, r31
     ae2:	ba 0b       	sbc	r27, r26
     ae4:	62 0b       	sbc	r22, r18
     ae6:	73 0b       	sbc	r23, r19
     ae8:	84 0b       	sbc	r24, r20
     aea:	ba f0       	brmi	.+46     	;  0xb1a
     aec:	91 50       	subi	r25, 0x01	; 1
     aee:	a1 f0       	breq	.+40     	;  0xb18
     af0:	ff 0f       	add	r31, r31
     af2:	bb 1f       	adc	r27, r27
     af4:	66 1f       	adc	r22, r22
     af6:	77 1f       	adc	r23, r23
     af8:	88 1f       	adc	r24, r24
     afa:	c2 f7       	brpl	.-16     	;  0xaec
     afc:	0e c0       	rjmp	.+28     	;  0xb1a
     afe:	ba 0f       	add	r27, r26
     b00:	62 1f       	adc	r22, r18
     b02:	73 1f       	adc	r23, r19
     b04:	84 1f       	adc	r24, r20
     b06:	48 f4       	brcc	.+18     	;  0xb1a
     b08:	87 95       	ror	r24
     b0a:	77 95       	ror	r23
     b0c:	67 95       	ror	r22
     b0e:	b7 95       	ror	r27
     b10:	f7 95       	ror	r31
     b12:	9e 3f       	cpi	r25, 0xFE	; 254
     b14:	08 f0       	brcs	.+2      	;  0xb18
     b16:	b0 cf       	rjmp	.-160    	;  0xa78
     b18:	93 95       	inc	r25
     b1a:	88 0f       	add	r24, r24
     b1c:	08 f0       	brcs	.+2      	;  0xb20
     b1e:	99 27       	eor	r25, r25
     b20:	ee 0f       	add	r30, r30
     b22:	97 95       	ror	r25
     b24:	87 95       	ror	r24
     b26:	08 95       	ret
     b28:	0e 94 77 06 	call	0xcee	;  0xcee
     b2c:	08 f4       	brcc	.+2      	;  0xb30
     b2e:	81 e0       	ldi	r24, 0x01	; 1
     b30:	08 95       	ret
     b32:	0e 94 ad 05 	call	0xb5a	;  0xb5a
     b36:	0c 94 b2 06 	jmp	0xd64	;  0xd64
     b3a:	0e 94 ab 06 	call	0xd56	;  0xd56
     b3e:	58 f0       	brcs	.+22     	;  0xb56
     b40:	0e 94 a4 06 	call	0xd48	;  0xd48
     b44:	40 f0       	brcs	.+16     	;  0xb56
     b46:	29 f4       	brne	.+10     	;  0xb52
     b48:	5f 3f       	cpi	r21, 0xFF	; 255
     b4a:	29 f0       	breq	.+10     	;  0xb56
     b4c:	0c 94 9b 06 	jmp	0xd36	;  0xd36
     b50:	51 11       	cpse	r21, r1
     b52:	0c 94 e6 06 	jmp	0xdcc	;  0xdcc
     b56:	0c 94 a1 06 	jmp	0xd42	;  0xd42
     b5a:	0e 94 c3 06 	call	0xd86	;  0xd86
     b5e:	68 f3       	brcs	.-38     	;  0xb3a
     b60:	99 23       	and	r25, r25
     b62:	b1 f3       	breq	.-20     	;  0xb50
     b64:	55 23       	and	r21, r21
     b66:	91 f3       	breq	.-28     	;  0xb4c
     b68:	95 1b       	sub	r25, r21
     b6a:	55 0b       	sbc	r21, r21
     b6c:	bb 27       	eor	r27, r27
     b6e:	aa 27       	eor	r26, r26
     b70:	62 17       	cp	r22, r18
     b72:	73 07       	cpc	r23, r19
     b74:	84 07       	cpc	r24, r20
     b76:	38 f0       	brcs	.+14     	;  0xb86
     b78:	9f 5f       	subi	r25, 0xFF	; 255
     b7a:	5f 4f       	sbci	r21, 0xFF	; 255
     b7c:	22 0f       	add	r18, r18
     b7e:	33 1f       	adc	r19, r19
     b80:	44 1f       	adc	r20, r20
     b82:	aa 1f       	adc	r26, r26
     b84:	a9 f3       	breq	.-22     	;  0xb70
     b86:	35 d0       	rcall	.+106    	;  0xbf2
     b88:	0e 2e       	mov	r0, r30
     b8a:	3a f0       	brmi	.+14     	;  0xb9a
     b8c:	e0 e8       	ldi	r30, 0x80	; 128
     b8e:	32 d0       	rcall	.+100    	;  0xbf4
     b90:	91 50       	subi	r25, 0x01	; 1
     b92:	50 40       	sbci	r21, 0x00	; 0
     b94:	e6 95       	lsr	r30
     b96:	00 1c       	adc	r0, r0
     b98:	ca f7       	brpl	.-14     	;  0xb8c
     b9a:	2b d0       	rcall	.+86     	;  0xbf2
     b9c:	fe 2f       	mov	r31, r30
     b9e:	29 d0       	rcall	.+82     	;  0xbf2
     ba0:	66 0f       	add	r22, r22
     ba2:	77 1f       	adc	r23, r23
     ba4:	88 1f       	adc	r24, r24
     ba6:	bb 1f       	adc	r27, r27
     ba8:	26 17       	cp	r18, r22
     baa:	37 07       	cpc	r19, r23
     bac:	48 07       	cpc	r20, r24
     bae:	ab 07       	cpc	r26, r27
     bb0:	b0 e8       	ldi	r27, 0x80	; 128
     bb2:	09 f0       	breq	.+2      	;  0xbb6
     bb4:	bb 0b       	sbc	r27, r27
     bb6:	80 2d       	mov	r24, r0
     bb8:	bf 01       	movw	r22, r30
     bba:	ff 27       	eor	r31, r31
     bbc:	93 58       	subi	r25, 0x83	; 131
     bbe:	5f 4f       	sbci	r21, 0xFF	; 255
     bc0:	3a f0       	brmi	.+14     	;  0xbd0
     bc2:	9e 3f       	cpi	r25, 0xFE	; 254
     bc4:	51 05       	cpc	r21, r1
     bc6:	78 f0       	brcs	.+30     	;  0xbe6
     bc8:	0c 94 9b 06 	jmp	0xd36	;  0xd36
     bcc:	0c 94 e6 06 	jmp	0xdcc	;  0xdcc
     bd0:	5f 3f       	cpi	r21, 0xFF	; 255
     bd2:	e4 f3       	brlt	.-8      	;  0xbcc
     bd4:	98 3e       	cpi	r25, 0xE8	; 232
     bd6:	d4 f3       	brlt	.-12     	;  0xbcc
     bd8:	86 95       	lsr	r24
     bda:	77 95       	ror	r23
     bdc:	67 95       	ror	r22
     bde:	b7 95       	ror	r27
     be0:	f7 95       	ror	r31
     be2:	9f 5f       	subi	r25, 0xFF	; 255
     be4:	c9 f7       	brne	.-14     	;  0xbd8
     be6:	88 0f       	add	r24, r24
     be8:	91 1d       	adc	r25, r1
     bea:	96 95       	lsr	r25
     bec:	87 95       	ror	r24
     bee:	97 f9       	bld	r25, 7
     bf0:	08 95       	ret
     bf2:	e1 e0       	ldi	r30, 0x01	; 1
     bf4:	66 0f       	add	r22, r22
     bf6:	77 1f       	adc	r23, r23
     bf8:	88 1f       	adc	r24, r24
     bfa:	bb 1f       	adc	r27, r27
     bfc:	62 17       	cp	r22, r18
     bfe:	73 07       	cpc	r23, r19
     c00:	84 07       	cpc	r24, r20
     c02:	ba 07       	cpc	r27, r26
     c04:	20 f0       	brcs	.+8      	;  0xc0e
     c06:	62 1b       	sub	r22, r18
     c08:	73 0b       	sbc	r23, r19
     c0a:	84 0b       	sbc	r24, r20
     c0c:	ba 0b       	sbc	r27, r26
     c0e:	ee 1f       	adc	r30, r30
     c10:	88 f7       	brcc	.-30     	;  0xbf4
     c12:	e0 95       	com	r30
     c14:	08 95       	ret
     c16:	0e 94 cb 06 	call	0xd96	;  0xd96
     c1a:	88 f0       	brcs	.+34     	;  0xc3e
     c1c:	9f 57       	subi	r25, 0x7F	; 127
     c1e:	98 f0       	brcs	.+38     	;  0xc46
     c20:	b9 2f       	mov	r27, r25
     c22:	99 27       	eor	r25, r25
     c24:	b7 51       	subi	r27, 0x17	; 23
     c26:	b0 f0       	brcs	.+44     	;  0xc54
     c28:	e1 f0       	breq	.+56     	;  0xc62
     c2a:	66 0f       	add	r22, r22
     c2c:	77 1f       	adc	r23, r23
     c2e:	88 1f       	adc	r24, r24
     c30:	99 1f       	adc	r25, r25
     c32:	1a f0       	brmi	.+6      	;  0xc3a
     c34:	ba 95       	dec	r27
     c36:	c9 f7       	brne	.-14     	;  0xc2a
     c38:	14 c0       	rjmp	.+40     	;  0xc62
     c3a:	b1 30       	cpi	r27, 0x01	; 1
     c3c:	91 f0       	breq	.+36     	;  0xc62
     c3e:	0e 94 e5 06 	call	0xdca	;  0xdca
     c42:	b1 e0       	ldi	r27, 0x01	; 1
     c44:	08 95       	ret
     c46:	0c 94 e5 06 	jmp	0xdca	;  0xdca
     c4a:	67 2f       	mov	r22, r23
     c4c:	78 2f       	mov	r23, r24
     c4e:	88 27       	eor	r24, r24
     c50:	b8 5f       	subi	r27, 0xF8	; 248
     c52:	39 f0       	breq	.+14     	;  0xc62
     c54:	b9 3f       	cpi	r27, 0xF9	; 249
     c56:	cc f3       	brlt	.-14     	;  0xc4a
     c58:	86 95       	lsr	r24
     c5a:	77 95       	ror	r23
     c5c:	67 95       	ror	r22
     c5e:	b3 95       	inc	r27
     c60:	d9 f7       	brne	.-10     	;  0xc58
     c62:	3e f4       	brtc	.+14     	;  0xc72
     c64:	90 95       	com	r25
     c66:	80 95       	com	r24
     c68:	70 95       	com	r23
     c6a:	61 95       	neg	r22
     c6c:	7f 4f       	sbci	r23, 0xFF	; 255
     c6e:	8f 4f       	sbci	r24, 0xFF	; 255
     c70:	9f 4f       	sbci	r25, 0xFF	; 255
     c72:	08 95       	ret
     c74:	e8 94       	clt
     c76:	09 c0       	rjmp	.+18     	;  0xc8a
     c78:	97 fb       	bst	r25, 7
     c7a:	3e f4       	brtc	.+14     	;  0xc8a
     c7c:	90 95       	com	r25
     c7e:	80 95       	com	r24
     c80:	70 95       	com	r23
     c82:	61 95       	neg	r22
     c84:	7f 4f       	sbci	r23, 0xFF	; 255
     c86:	8f 4f       	sbci	r24, 0xFF	; 255
     c88:	9f 4f       	sbci	r25, 0xFF	; 255
     c8a:	99 23       	and	r25, r25
     c8c:	a9 f0       	breq	.+42     	;  0xcb8
     c8e:	f9 2f       	mov	r31, r25
     c90:	96 e9       	ldi	r25, 0x96	; 150
     c92:	bb 27       	eor	r27, r27
     c94:	93 95       	inc	r25
     c96:	f6 95       	lsr	r31
     c98:	87 95       	ror	r24
     c9a:	77 95       	ror	r23
     c9c:	67 95       	ror	r22
     c9e:	b7 95       	ror	r27
     ca0:	f1 11       	cpse	r31, r1
     ca2:	f8 cf       	rjmp	.-16     	;  0xc94
     ca4:	fa f4       	brpl	.+62     	;  0xce4
     ca6:	bb 0f       	add	r27, r27
     ca8:	11 f4       	brne	.+4      	;  0xcae
     caa:	60 ff       	sbrs	r22, 0
     cac:	1b c0       	rjmp	.+54     	;  0xce4
     cae:	6f 5f       	subi	r22, 0xFF	; 255
     cb0:	7f 4f       	sbci	r23, 0xFF	; 255
     cb2:	8f 4f       	sbci	r24, 0xFF	; 255
     cb4:	9f 4f       	sbci	r25, 0xFF	; 255
     cb6:	16 c0       	rjmp	.+44     	;  0xce4
     cb8:	88 23       	and	r24, r24
     cba:	11 f0       	breq	.+4      	;  0xcc0
     cbc:	96 e9       	ldi	r25, 0x96	; 150
     cbe:	11 c0       	rjmp	.+34     	;  0xce2
     cc0:	77 23       	and	r23, r23
     cc2:	21 f0       	breq	.+8      	;  0xccc
     cc4:	9e e8       	ldi	r25, 0x8E	; 142
     cc6:	87 2f       	mov	r24, r23
     cc8:	76 2f       	mov	r23, r22
     cca:	05 c0       	rjmp	.+10     	;  0xcd6
     ccc:	66 23       	and	r22, r22
     cce:	71 f0       	breq	.+28     	;  0xcec
     cd0:	96 e8       	ldi	r25, 0x86	; 134
     cd2:	86 2f       	mov	r24, r22
     cd4:	70 e0       	ldi	r23, 0x00	; 0
     cd6:	60 e0       	ldi	r22, 0x00	; 0
     cd8:	2a f0       	brmi	.+10     	;  0xce4
     cda:	9a 95       	dec	r25
     cdc:	66 0f       	add	r22, r22
     cde:	77 1f       	adc	r23, r23
     ce0:	88 1f       	adc	r24, r24
     ce2:	da f7       	brpl	.-10     	;  0xcda
     ce4:	88 0f       	add	r24, r24
     ce6:	96 95       	lsr	r25
     ce8:	87 95       	ror	r24
     cea:	97 f9       	bld	r25, 7
     cec:	08 95       	ret
     cee:	99 0f       	add	r25, r25
     cf0:	00 08       	sbc	r0, r0
     cf2:	55 0f       	add	r21, r21
     cf4:	aa 0b       	sbc	r26, r26
     cf6:	e0 e8       	ldi	r30, 0x80	; 128
     cf8:	fe ef       	ldi	r31, 0xFE	; 254
     cfa:	16 16       	cp	r1, r22
     cfc:	17 06       	cpc	r1, r23
     cfe:	e8 07       	cpc	r30, r24
     d00:	f9 07       	cpc	r31, r25
     d02:	c0 f0       	brcs	.+48     	;  0xd34
     d04:	12 16       	cp	r1, r18
     d06:	13 06       	cpc	r1, r19
     d08:	e4 07       	cpc	r30, r20
     d0a:	f5 07       	cpc	r31, r21
     d0c:	98 f0       	brcs	.+38     	;  0xd34
     d0e:	62 1b       	sub	r22, r18
     d10:	73 0b       	sbc	r23, r19
     d12:	84 0b       	sbc	r24, r20
     d14:	95 0b       	sbc	r25, r21
     d16:	39 f4       	brne	.+14     	;  0xd26
     d18:	0a 26       	eor	r0, r26
     d1a:	61 f0       	breq	.+24     	;  0xd34
     d1c:	23 2b       	or	r18, r19
     d1e:	24 2b       	or	r18, r20
     d20:	25 2b       	or	r18, r21
     d22:	21 f4       	brne	.+8      	;  0xd2c
     d24:	08 95       	ret
     d26:	0a 26       	eor	r0, r26
     d28:	09 f4       	brne	.+2      	;  0xd2c
     d2a:	a1 40       	sbci	r26, 0x01	; 1
     d2c:	a6 95       	lsr	r26
     d2e:	8f ef       	ldi	r24, 0xFF	; 255
     d30:	81 1d       	adc	r24, r1
     d32:	81 1d       	adc	r24, r1
     d34:	08 95       	ret
     d36:	97 f9       	bld	r25, 7
     d38:	9f 67       	ori	r25, 0x7F	; 127
     d3a:	80 e8       	ldi	r24, 0x80	; 128
     d3c:	70 e0       	ldi	r23, 0x00	; 0
     d3e:	60 e0       	ldi	r22, 0x00	; 0
     d40:	08 95       	ret
     d42:	9f ef       	ldi	r25, 0xFF	; 255
     d44:	80 ec       	ldi	r24, 0xC0	; 192
     d46:	08 95       	ret
     d48:	00 24       	eor	r0, r0
     d4a:	0a 94       	dec	r0
     d4c:	16 16       	cp	r1, r22
     d4e:	17 06       	cpc	r1, r23
     d50:	18 06       	cpc	r1, r24
     d52:	09 06       	cpc	r0, r25
     d54:	08 95       	ret
     d56:	00 24       	eor	r0, r0
     d58:	0a 94       	dec	r0
     d5a:	12 16       	cp	r1, r18
     d5c:	13 06       	cpc	r1, r19
     d5e:	14 06       	cpc	r1, r20
     d60:	05 06       	cpc	r0, r21
     d62:	08 95       	ret
     d64:	09 2e       	mov	r0, r25
     d66:	03 94       	inc	r0
     d68:	00 0c       	add	r0, r0
     d6a:	11 f4       	brne	.+4      	;  0xd70
     d6c:	88 23       	and	r24, r24
     d6e:	52 f0       	brmi	.+20     	;  0xd84
     d70:	bb 0f       	add	r27, r27
     d72:	40 f4       	brcc	.+16     	;  0xd84
     d74:	bf 2b       	or	r27, r31
     d76:	11 f4       	brne	.+4      	;  0xd7c
     d78:	60 ff       	sbrs	r22, 0
     d7a:	04 c0       	rjmp	.+8      	;  0xd84
     d7c:	6f 5f       	subi	r22, 0xFF	; 255
     d7e:	7f 4f       	sbci	r23, 0xFF	; 255
     d80:	8f 4f       	sbci	r24, 0xFF	; 255
     d82:	9f 4f       	sbci	r25, 0xFF	; 255
     d84:	08 95       	ret
     d86:	57 fd       	sbrc	r21, 7
     d88:	90 58       	subi	r25, 0x80	; 128
     d8a:	44 0f       	add	r20, r20
     d8c:	55 1f       	adc	r21, r21
     d8e:	59 f0       	breq	.+22     	;  0xda6
     d90:	5f 3f       	cpi	r21, 0xFF	; 255
     d92:	71 f0       	breq	.+28     	;  0xdb0
     d94:	47 95       	ror	r20
     d96:	88 0f       	add	r24, r24
     d98:	97 fb       	bst	r25, 7
     d9a:	99 1f       	adc	r25, r25
     d9c:	61 f0       	breq	.+24     	;  0xdb6
     d9e:	9f 3f       	cpi	r25, 0xFF	; 255
     da0:	79 f0       	breq	.+30     	;  0xdc0
     da2:	87 95       	ror	r24
     da4:	08 95       	ret
     da6:	12 16       	cp	r1, r18
     da8:	13 06       	cpc	r1, r19
     daa:	14 06       	cpc	r1, r20
     dac:	55 1f       	adc	r21, r21
     dae:	f2 cf       	rjmp	.-28     	;  0xd94
     db0:	46 95       	lsr	r20
     db2:	f1 df       	rcall	.-30     	;  0xd96
     db4:	08 c0       	rjmp	.+16     	;  0xdc6
     db6:	16 16       	cp	r1, r22
     db8:	17 06       	cpc	r1, r23
     dba:	18 06       	cpc	r1, r24
     dbc:	99 1f       	adc	r25, r25
     dbe:	f1 cf       	rjmp	.-30     	;  0xda2
     dc0:	86 95       	lsr	r24
     dc2:	71 05       	cpc	r23, r1
     dc4:	61 05       	cpc	r22, r1
     dc6:	08 94       	sec
     dc8:	08 95       	ret
     dca:	e8 94       	clt
     dcc:	bb 27       	eor	r27, r27
     dce:	66 27       	eor	r22, r22
     dd0:	77 27       	eor	r23, r23
     dd2:	cb 01       	movw	r24, r22
     dd4:	97 f9       	bld	r25, 7
     dd6:	08 95       	ret
     dd8:	0e 94 77 06 	call	0xcee	;  0xcee
     ddc:	08 f4       	brcc	.+2      	;  0xde0
     dde:	8f ef       	ldi	r24, 0xFF	; 255
     de0:	08 95       	ret
     de2:	0e 94 04 07 	call	0xe08	;  0xe08
     de6:	0c 94 b2 06 	jmp	0xd64	;  0xd64
     dea:	0e 94 a4 06 	call	0xd48	;  0xd48
     dee:	38 f0       	brcs	.+14     	;  0xdfe
     df0:	0e 94 ab 06 	call	0xd56	;  0xd56
     df4:	20 f0       	brcs	.+8      	;  0xdfe
     df6:	95 23       	and	r25, r21
     df8:	11 f0       	breq	.+4      	;  0xdfe
     dfa:	0c 94 9b 06 	jmp	0xd36	;  0xd36
     dfe:	0c 94 a1 06 	jmp	0xd42	;  0xd42
     e02:	11 24       	eor	r1, r1
     e04:	0c 94 e6 06 	jmp	0xdcc	;  0xdcc
     e08:	0e 94 c3 06 	call	0xd86	;  0xd86
     e0c:	70 f3       	brcs	.-36     	;  0xdea
     e0e:	95 9f       	mul	r25, r21
     e10:	c1 f3       	breq	.-16     	;  0xe02
     e12:	95 0f       	add	r25, r21
     e14:	50 e0       	ldi	r21, 0x00	; 0
     e16:	55 1f       	adc	r21, r21
     e18:	62 9f       	mul	r22, r18
     e1a:	f0 01       	movw	r30, r0
     e1c:	72 9f       	mul	r23, r18
     e1e:	bb 27       	eor	r27, r27
     e20:	f0 0d       	add	r31, r0
     e22:	b1 1d       	adc	r27, r1
     e24:	63 9f       	mul	r22, r19
     e26:	aa 27       	eor	r26, r26
     e28:	f0 0d       	add	r31, r0
     e2a:	b1 1d       	adc	r27, r1
     e2c:	aa 1f       	adc	r26, r26
     e2e:	64 9f       	mul	r22, r20
     e30:	66 27       	eor	r22, r22
     e32:	b0 0d       	add	r27, r0
     e34:	a1 1d       	adc	r26, r1
     e36:	66 1f       	adc	r22, r22
     e38:	82 9f       	mul	r24, r18
     e3a:	22 27       	eor	r18, r18
     e3c:	b0 0d       	add	r27, r0
     e3e:	a1 1d       	adc	r26, r1
     e40:	62 1f       	adc	r22, r18
     e42:	73 9f       	mul	r23, r19
     e44:	b0 0d       	add	r27, r0
     e46:	a1 1d       	adc	r26, r1
     e48:	62 1f       	adc	r22, r18
     e4a:	83 9f       	mul	r24, r19
     e4c:	a0 0d       	add	r26, r0
     e4e:	61 1d       	adc	r22, r1
     e50:	22 1f       	adc	r18, r18
     e52:	74 9f       	mul	r23, r20
     e54:	33 27       	eor	r19, r19
     e56:	a0 0d       	add	r26, r0
     e58:	61 1d       	adc	r22, r1
     e5a:	23 1f       	adc	r18, r19
     e5c:	84 9f       	mul	r24, r20
     e5e:	60 0d       	add	r22, r0
     e60:	21 1d       	adc	r18, r1
     e62:	82 2f       	mov	r24, r18
     e64:	76 2f       	mov	r23, r22
     e66:	6a 2f       	mov	r22, r26
     e68:	11 24       	eor	r1, r1
     e6a:	9f 57       	subi	r25, 0x7F	; 127
     e6c:	50 40       	sbci	r21, 0x00	; 0
     e6e:	9a f0       	brmi	.+38     	;  0xe96
     e70:	f1 f0       	breq	.+60     	;  0xeae
     e72:	88 23       	and	r24, r24
     e74:	4a f0       	brmi	.+18     	;  0xe88
     e76:	ee 0f       	add	r30, r30
     e78:	ff 1f       	adc	r31, r31
     e7a:	bb 1f       	adc	r27, r27
     e7c:	66 1f       	adc	r22, r22
     e7e:	77 1f       	adc	r23, r23
     e80:	88 1f       	adc	r24, r24
     e82:	91 50       	subi	r25, 0x01	; 1
     e84:	50 40       	sbci	r21, 0x00	; 0
     e86:	a9 f7       	brne	.-22     	;  0xe72
     e88:	9e 3f       	cpi	r25, 0xFE	; 254
     e8a:	51 05       	cpc	r21, r1
     e8c:	80 f0       	brcs	.+32     	;  0xeae
     e8e:	0c 94 9b 06 	jmp	0xd36	;  0xd36
     e92:	0c 94 e6 06 	jmp	0xdcc	;  0xdcc
     e96:	5f 3f       	cpi	r21, 0xFF	; 255
     e98:	e4 f3       	brlt	.-8      	;  0xe92
     e9a:	98 3e       	cpi	r25, 0xE8	; 232
     e9c:	d4 f3       	brlt	.-12     	;  0xe92
     e9e:	86 95       	lsr	r24
     ea0:	77 95       	ror	r23
     ea2:	67 95       	ror	r22
     ea4:	b7 95       	ror	r27
     ea6:	f7 95       	ror	r31
     ea8:	e7 95       	ror	r30
     eaa:	9f 5f       	subi	r25, 0xFF	; 255
     eac:	c1 f7       	brne	.-16     	;  0xe9e
     eae:	fe 2b       	or	r31, r30
     eb0:	88 0f       	add	r24, r24
     eb2:	91 1d       	adc	r25, r1
     eb4:	96 95       	lsr	r25
     eb6:	87 95       	ror	r24
     eb8:	97 f9       	bld	r25, 7
     eba:	08 95       	ret
     ebc:	0e 94 77 06 	call	0xcee	;  0xcee
     ec0:	88 0b       	sbc	r24, r24
     ec2:	99 0b       	sbc	r25, r25
     ec4:	08 95       	ret
     ec6:	a1 e2       	ldi	r26, 0x21	; 33
     ec8:	1a 2e       	mov	r1, r26
     eca:	aa 1b       	sub	r26, r26
     ecc:	bb 1b       	sub	r27, r27
     ece:	fd 01       	movw	r30, r26
     ed0:	0d c0       	rjmp	.+26     	;  0xeec
     ed2:	aa 1f       	adc	r26, r26
     ed4:	bb 1f       	adc	r27, r27
     ed6:	ee 1f       	adc	r30, r30
     ed8:	ff 1f       	adc	r31, r31
     eda:	a2 17       	cp	r26, r18
     edc:	b3 07       	cpc	r27, r19
     ede:	e4 07       	cpc	r30, r20
     ee0:	f5 07       	cpc	r31, r21
     ee2:	20 f0       	brcs	.+8      	;  0xeec
     ee4:	a2 1b       	sub	r26, r18
     ee6:	b3 0b       	sbc	r27, r19
     ee8:	e4 0b       	sbc	r30, r20
     eea:	f5 0b       	sbc	r31, r21
     eec:	66 1f       	adc	r22, r22
     eee:	77 1f       	adc	r23, r23
     ef0:	88 1f       	adc	r24, r24
     ef2:	99 1f       	adc	r25, r25
     ef4:	1a 94       	dec	r1
     ef6:	69 f7       	brne	.-38     	;  0xed2
     ef8:	60 95       	com	r22
     efa:	70 95       	com	r23
     efc:	80 95       	com	r24
     efe:	90 95       	com	r25
     f00:	9b 01       	movw	r18, r22
     f02:	ac 01       	movw	r20, r24
     f04:	bd 01       	movw	r22, r26
     f06:	cf 01       	movw	r24, r30
     f08:	08 95       	ret
     f0a:	ee 0f       	add	r30, r30
     f0c:	ff 1f       	adc	r31, r31
     f0e:	05 90       	lpm	r0, Z+
     f10:	f4 91       	lpm	r31, Z
     f12:	e0 2d       	mov	r30, r0
     f14:	09 94       	ijmp
     f16:	f8 94       	cli
     f18:	ff cf       	rjmp	.-2      	;  0xf18
     f1a:	00 00       	nop
     f1c:	00 00       	nop
     f1e:	ce 01       	movw	r24, r28
     f20:	2e 01       	movw	r4, r28
     f22:	5b 01       	movw	r10, r22
     f24:	1b 02       	muls	r17, r27
     f26:	8c 01       	movw	r16, r24
     f28:	6a 01       	movw	r12, r20
     f2a:	7e 01       	movw	r14, r28
     f2c:	67 65       	ori	r22, 0x57	; 87
     f2e:	74 20       	and	r7, r4
     f30:	61 64       	ori	r22, 0x41	; 65
     f32:	20 70       	andi	r18, 0x00	; 0
     f34:	69 6e       	ori	r22, 0xE9	; 233
     f36:	20 76       	andi	r18, 0x60	; 96
     f38:	61 6c       	ori	r22, 0xC1	; 193
     f3a:	75 65       	ori	r23, 0x55	; 85
     f3c:	20 00       	.word	0x0020	; ????
     f3e:	0a 76       	andi	r16, 0x6A	; 106
     f40:	6f 6c       	ori	r22, 0xCF	; 207
     f42:	74 61       	ori	r23, 0x14	; 20
     f44:	67 65       	ori	r22, 0x57	; 87
     f46:	20 3d       	cpi	r18, 0xD0	; 208
     f48:	20 00       	.word	0x0020	; ????
     f4a:	0d 0a       	sbc	r0, r29
     f4c:	00 6e       	ori	r16, 0xE0	; 224
     f4e:	61 6e       	ori	r22, 0xE1	; 225
     f50:	00 69       	ori	r16, 0x90	; 144
     f52:	6e 66       	ori	r22, 0x6E	; 110
     f54:	00 6f       	ori	r16, 0xF0	; 240
     f56:	76 66       	ori	r23, 0x66	; 102
     f58:	00 00       	nop
     f5a:	ff ff       	.word	0xffff	; ????
     f5c:	ff ff       	.word	0xffff	; ????
     f5e:	ff ff       	.word	0xffff	; ????
     f60:	ff ff       	.word	0xffff	; ????
     f62:	ff ff       	.word	0xffff	; ????
     f64:	ff ff       	.word	0xffff	; ????
     f66:	ff ff       	.word	0xffff	; ????
     f68:	ff ff       	.word	0xffff	; ????
     f6a:	ff ff       	.word	0xffff	; ????
     f6c:	ff ff       	.word	0xffff	; ????
     f6e:	ff ff       	.word	0xffff	; ????
     f70:	ff ff       	.word	0xffff	; ????
     f72:	ff ff       	.word	0xffff	; ????
     f74:	ff ff       	.word	0xffff	; ????
     f76:	ff ff       	.word	0xffff	; ????
     f78:	ff ff       	.word	0xffff	; ????
     f7a:	ff ff       	.word	0xffff	; ????
     f7c:	ff ff       	.word	0xffff	; ????
     f7e:	ff ff       	.word	0xffff	; ????
     f80:	ff 91       	pop	r31
     f82:	ef 91       	pop	r30
     f84:	9f 91       	pop	r25
     f86:	8f 91       	pop	r24
     f88:	2f 91       	pop	r18
     f8a:	0f 90       	pop	r0
     f8c:	0f be       	out	0x3f, r0	; 63
     f8e:	0f 90       	pop	r0
     f90:	1f 90       	pop	r1
     f92:	18 95       	reti
     f94:	1f 92       	push	r1
     f96:	0f 92       	push	r0
     f98:	0f b6       	in	r0, 0x3f	; 63
     f9a:	0f 92       	push	r0
     f9c:	11 24       	eor	r1, r1
     f9e:	2f 93       	push	r18
     fa0:	3f 93       	push	r19
     fa2:	4f 93       	push	r20
     fa4:	5f 93       	push	r21
     fa6:	6f 93       	push	r22
     fa8:	7f 93       	push	r23
     faa:	8f 93       	push	r24
     fac:	9f 93       	push	r25
     fae:	af 93       	push	r26
     fb0:	bf 93       	push	r27
     fb2:	ef 93       	push	r30
     fb4:	ff 93       	push	r31
     fb6:	88 ef       	ldi	r24, 0xF8	; 248
     fb8:	93 e0       	ldi	r25, 0x03	; 3
     fba:	0e 94 8e 06 	call	0xd1c	;  0xd1c
     fbe:	ff 91       	pop	r31
     fc0:	ef 91       	pop	r30
     fc2:	bf 91       	pop	r27
     fc4:	af 91       	pop	r26
     fc6:	9f 91       	pop	r25
     fc8:	8f 91       	pop	r24
     fca:	7f 91       	pop	r23
     fcc:	6f 91       	pop	r22
     fce:	5f 91       	pop	r21
     fd0:	4f 91       	pop	r20
     fd2:	3f 91       	pop	r19
     fd4:	2f 91       	pop	r18
     fd6:	0f 90       	pop	r0
     fd8:	0f be       	out	0x3f, r0	; 63
     fda:	0f 90       	pop	r0
     fdc:	1f 90       	pop	r1
     fde:	18 95       	reti
     fe0:	88 ef       	ldi	r24, 0xF8	; 248
     fe2:	93 e0       	ldi	r25, 0x03	; 3
     fe4:	0e 94 53 06 	call	0xca6	;  0xca6
     fe8:	21 e0       	ldi	r18, 0x01	; 1
     fea:	89 2b       	or	r24, r25
     fec:	09 f4       	brne	.+2      	;  0xff0
     fee:	20 e0       	ldi	r18, 0x00	; 0
     ff0:	82 2f       	mov	r24, r18
     ff2:	08 95       	ret
     ff4:	10 92 fb 03 	sts	0x03FB, r1	;  0x8003fb
     ff8:	10 92 fa 03 	sts	0x03FA, r1	;  0x8003fa
     ffc:	88 ee       	ldi	r24, 0xE8	; 232
     ffe:	93 e0       	ldi	r25, 0x03	; 3
    1000:	a0 e0       	ldi	r26, 0x00	; 0
    1002:	b0 e0       	ldi	r27, 0x00	; 0
    1004:	80 93 fc 03 	sts	0x03FC, r24	;  0x8003fc
    1008:	90 93 fd 03 	sts	0x03FD, r25	;  0x8003fd
    100c:	a0 93 fe 03 	sts	0x03FE, r26	;  0x8003fe
    1010:	b0 93 ff 03 	sts	0x03FF, r27	;  0x8003ff
    1014:	8f e5       	ldi	r24, 0x5F	; 95
    1016:	91 e0       	ldi	r25, 0x01	; 1
    1018:	90 93 f9 03 	sts	0x03F9, r25	;  0x8003f9
    101c:	80 93 f8 03 	sts	0x03F8, r24	;  0x8003f8
    1020:	85 ec       	ldi	r24, 0xC5	; 197
    1022:	90 e0       	ldi	r25, 0x00	; 0
    1024:	90 93 05 04 	sts	0x0405, r25	;  0x800405
    1028:	80 93 04 04 	sts	0x0404, r24	;  0x800404
    102c:	84 ec       	ldi	r24, 0xC4	; 196
    102e:	90 e0       	ldi	r25, 0x00	; 0
    1030:	90 93 07 04 	sts	0x0407, r25	;  0x800407
    1034:	80 93 06 04 	sts	0x0406, r24	;  0x800406
    1038:	80 ec       	ldi	r24, 0xC0	; 192
    103a:	90 e0       	ldi	r25, 0x00	; 0
    103c:	90 93 09 04 	sts	0x0409, r25	;  0x800409
    1040:	80 93 08 04 	sts	0x0408, r24	;  0x800408
    1044:	81 ec       	ldi	r24, 0xC1	; 193
    1046:	90 e0       	ldi	r25, 0x00	; 0
    1048:	90 93 0b 04 	sts	0x040B, r25	;  0x80040b
    104c:	80 93 0a 04 	sts	0x040A, r24	;  0x80040a
    1050:	82 ec       	ldi	r24, 0xC2	; 194
    1052:	90 e0       	ldi	r25, 0x00	; 0
    1054:	90 93 0d 04 	sts	0x040D, r25	;  0x80040d
    1058:	80 93 0c 04 	sts	0x040C, r24	;  0x80040c
    105c:	86 ec       	ldi	r24, 0xC6	; 198
    105e:	90 e0       	ldi	r25, 0x00	; 0
    1060:	90 93 0f 04 	sts	0x040F, r25	;  0x80040f
    1064:	80 93 0e 04 	sts	0x040E, r24	;  0x80040e
    1068:	10 92 11 04 	sts	0x0411, r1	;  0x800411
    106c:	10 92 12 04 	sts	0x0412, r1	;  0x800412
    1070:	10 92 13 04 	sts	0x0413, r1	;  0x800413
    1074:	10 92 14 04 	sts	0x0414, r1	;  0x800414
    1078:	08 95       	ret
    107a:	08 95       	ret
    107c:	0e 94 c6 05 	call	0xb8c	;  0xb8c
    1080:	0e 94 3d 08 	call	0x107a	;  0x107a
    1084:	0e 94 cf 02 	call	0x59e	;  0x59e
    1088:	c0 e8       	ldi	r28, 0x80	; 128
    108a:	d6 e0       	ldi	r29, 0x06	; 6
    108c:	0e 94 d8 02 	call	0x5b0	;  0x5b0
    1090:	20 97       	sbiw	r28, 0x00	; 0
    1092:	e1 f3       	breq	.-8      	;  0x108c
    1094:	0e 94 80 06 	call	0xd00	;  0xd00
    1098:	f9 cf       	rjmp	.-14     	;  0x108c
    109a:	cf 92       	push	r12
    109c:	df 92       	push	r13
    109e:	ef 92       	push	r14
    10a0:	ff 92       	push	r15
    10a2:	0f 93       	push	r16
    10a4:	1f 93       	push	r17
    10a6:	cf 93       	push	r28
    10a8:	df 93       	push	r29
    10aa:	6c 01       	movw	r12, r24
    10ac:	7a 01       	movw	r14, r20
    10ae:	eb 01       	movw	r28, r22
    10b0:	e6 0e       	add	r14, r22
    10b2:	f7 1e       	adc	r15, r23
    10b4:	00 e0       	ldi	r16, 0x00	; 0
    10b6:	10 e0       	ldi	r17, 0x00	; 0
    10b8:	ce 15       	cp	r28, r14
    10ba:	df 05       	cpc	r29, r15
    10bc:	61 f0       	breq	.+24     	;  0x10d6
    10be:	69 91       	ld	r22, Y+
    10c0:	d6 01       	movw	r26, r12
    10c2:	ed 91       	ld	r30, X+
    10c4:	fc 91       	ld	r31, X
    10c6:	01 90       	ld	r0, Z+
    10c8:	f0 81       	ld	r31, Z
    10ca:	e0 2d       	mov	r30, r0
    10cc:	c6 01       	movw	r24, r12
    10ce:	09 95       	icall
    10d0:	08 0f       	add	r16, r24
    10d2:	19 1f       	adc	r17, r25
    10d4:	f1 cf       	rjmp	.-30     	;  0x10b8
    10d6:	c8 01       	movw	r24, r16
    10d8:	df 91       	pop	r29
    10da:	cf 91       	pop	r28
    10dc:	1f 91       	pop	r17
    10de:	0f 91       	pop	r16
    10e0:	ff 90       	pop	r15
    10e2:	ef 90       	pop	r14
    10e4:	df 90       	pop	r13
    10e6:	cf 90       	pop	r12
    10e8:	08 95       	ret
    10ea:	61 15       	cp	r22, r1
    10ec:	71 05       	cpc	r23, r1
    10ee:	81 f0       	breq	.+32     	;  0x1110
    10f0:	db 01       	movw	r26, r22
    10f2:	0d 90       	ld	r0, X+
    10f4:	00 20       	and	r0, r0
    10f6:	e9 f7       	brne	.-6      	;  0x10f2
    10f8:	ad 01       	movw	r20, r26
    10fa:	41 50       	subi	r20, 0x01	; 1
    10fc:	51 09       	sbc	r21, r1
    10fe:	46 1b       	sub	r20, r22
    1100:	57 0b       	sbc	r21, r23
    1102:	dc 01       	movw	r26, r24
    1104:	ed 91       	ld	r30, X+
    1106:	fc 91       	ld	r31, X
    1108:	02 80       	ldd	r0, Z+2	; 0x02
    110a:	f3 81       	ldd	r31, Z+3	; 0x03
    110c:	e0 2d       	mov	r30, r0
    110e:	09 94       	ijmp
    1110:	80 e0       	ldi	r24, 0x00	; 0
    1112:	90 e0       	ldi	r25, 0x00	; 0
    1114:	08 95       	ret
    1116:	6b e6       	ldi	r22, 0x6B	; 107
    1118:	71 e0       	ldi	r23, 0x01	; 1
    111a:	0c 94 75 08 	jmp	0x10ea	;  0x10ea
    111e:	0f 93       	push	r16
    1120:	1f 93       	push	r17
    1122:	cf 93       	push	r28
    1124:	df 93       	push	r29
    1126:	ec 01       	movw	r28, r24
    1128:	0e 94 75 08 	call	0x10ea	;  0x10ea
    112c:	8c 01       	movw	r16, r24
    112e:	ce 01       	movw	r24, r28
    1130:	0e 94 8b 08 	call	0x1116	;  0x1116
    1134:	80 0f       	add	r24, r16
    1136:	91 1f       	adc	r25, r17
    1138:	df 91       	pop	r29
    113a:	cf 91       	pop	r28
    113c:	1f 91       	pop	r17
    113e:	0f 91       	pop	r16
    1140:	08 95       	ret
    1142:	fc 01       	movw	r30, r24
    1144:	80 81       	ld	r24, Z
    1146:	91 81       	ldd	r25, Z+1	; 0x01
    1148:	0c 94 e5 09 	jmp	0x13ca	;  0x13ca
    114c:	cf 93       	push	r28
    114e:	df 93       	push	r29
    1150:	ec 01       	movw	r28, r24
    1152:	88 81       	ld	r24, Y
    1154:	99 81       	ldd	r25, Y+1	; 0x01
    1156:	00 97       	sbiw	r24, 0x00	; 0
    1158:	11 f0       	breq	.+4      	;  0x115e
    115a:	0e 94 e5 09 	call	0x13ca	;  0x13ca
    115e:	19 82       	std	Y+1, r1	; 0x01
    1160:	18 82       	st	Y, r1
    1162:	1d 82       	std	Y+5, r1	; 0x05
    1164:	1c 82       	std	Y+4, r1	; 0x04
    1166:	1b 82       	std	Y+3, r1	; 0x03
    1168:	1a 82       	std	Y+2, r1	; 0x02
    116a:	df 91       	pop	r29
    116c:	cf 91       	pop	r28
    116e:	08 95       	ret
    1170:	0f 93       	push	r16
    1172:	1f 93       	push	r17
    1174:	cf 93       	push	r28
    1176:	df 93       	push	r29
    1178:	ec 01       	movw	r28, r24
    117a:	8b 01       	movw	r16, r22
    117c:	6f 5f       	subi	r22, 0xFF	; 255
    117e:	7f 4f       	sbci	r23, 0xFF	; 255
    1180:	88 81       	ld	r24, Y
    1182:	99 81       	ldd	r25, Y+1	; 0x01
    1184:	0e 94 74 0a 	call	0x14e8	;  0x14e8
    1188:	00 97       	sbiw	r24, 0x00	; 0
    118a:	31 f0       	breq	.+12     	;  0x1198
    118c:	99 83       	std	Y+1, r25	; 0x01
    118e:	88 83       	st	Y, r24
    1190:	1b 83       	std	Y+3, r17	; 0x03
    1192:	0a 83       	std	Y+2, r16	; 0x02
    1194:	81 e0       	ldi	r24, 0x01	; 1
    1196:	01 c0       	rjmp	.+2      	;  0x119a
    1198:	80 e0       	ldi	r24, 0x00	; 0
    119a:	df 91       	pop	r29
    119c:	cf 91       	pop	r28
    119e:	1f 91       	pop	r17
    11a0:	0f 91       	pop	r16
    11a2:	08 95       	ret
    11a4:	cf 93       	push	r28
    11a6:	df 93       	push	r29
    11a8:	ec 01       	movw	r28, r24
    11aa:	88 81       	ld	r24, Y
    11ac:	99 81       	ldd	r25, Y+1	; 0x01
    11ae:	89 2b       	or	r24, r25
    11b0:	29 f0       	breq	.+10     	;  0x11bc
    11b2:	8a 81       	ldd	r24, Y+2	; 0x02
    11b4:	9b 81       	ldd	r25, Y+3	; 0x03
    11b6:	86 17       	cp	r24, r22
    11b8:	97 07       	cpc	r25, r23
    11ba:	60 f4       	brcc	.+24     	;  0x11d4
    11bc:	ce 01       	movw	r24, r28
    11be:	0e 94 b8 08 	call	0x1170	;  0x1170
    11c2:	88 23       	and	r24, r24
    11c4:	41 f0       	breq	.+16     	;  0x11d6
    11c6:	8c 81       	ldd	r24, Y+4	; 0x04
    11c8:	9d 81       	ldd	r25, Y+5	; 0x05
    11ca:	89 2b       	or	r24, r25
    11cc:	19 f4       	brne	.+6      	;  0x11d4
    11ce:	e8 81       	ld	r30, Y
    11d0:	f9 81       	ldd	r31, Y+1	; 0x01
    11d2:	10 82       	st	Z, r1
    11d4:	81 e0       	ldi	r24, 0x01	; 1
    11d6:	df 91       	pop	r29
    11d8:	cf 91       	pop	r28
    11da:	08 95       	ret
    11dc:	ef 92       	push	r14
    11de:	ff 92       	push	r15
    11e0:	0f 93       	push	r16
    11e2:	1f 93       	push	r17
    11e4:	cf 93       	push	r28
    11e6:	df 93       	push	r29
    11e8:	ec 01       	movw	r28, r24
    11ea:	7b 01       	movw	r14, r22
    11ec:	8a 01       	movw	r16, r20
    11ee:	ba 01       	movw	r22, r20
    11f0:	0e 94 d2 08 	call	0x11a4	;  0x11a4
    11f4:	81 11       	cpse	r24, r1
    11f6:	04 c0       	rjmp	.+8      	;  0x1200
    11f8:	ce 01       	movw	r24, r28
    11fa:	0e 94 a6 08 	call	0x114c	;  0x114c
    11fe:	07 c0       	rjmp	.+14     	;  0x120e
    1200:	1d 83       	std	Y+5, r17	; 0x05
    1202:	0c 83       	std	Y+4, r16	; 0x04
    1204:	b7 01       	movw	r22, r14
    1206:	88 81       	ld	r24, Y
    1208:	99 81       	ldd	r25, Y+1	; 0x01
    120a:	0e 94 47 0b 	call	0x168e	;  0x168e
    120e:	ce 01       	movw	r24, r28
    1210:	df 91       	pop	r29
    1212:	cf 91       	pop	r28
    1214:	1f 91       	pop	r17
    1216:	0f 91       	pop	r16
    1218:	ff 90       	pop	r15
    121a:	ef 90       	pop	r14
    121c:	08 95       	ret
    121e:	fc 01       	movw	r30, r24
    1220:	11 82       	std	Z+1, r1	; 0x01
    1222:	10 82       	st	Z, r1
    1224:	13 82       	std	Z+3, r1	; 0x03
    1226:	12 82       	std	Z+2, r1	; 0x02
    1228:	15 82       	std	Z+5, r1	; 0x05
    122a:	14 82       	std	Z+4, r1	; 0x04
    122c:	61 15       	cp	r22, r1
    122e:	71 05       	cpc	r23, r1
    1230:	59 f0       	breq	.+22     	;  0x1248
    1232:	fb 01       	movw	r30, r22
    1234:	01 90       	ld	r0, Z+
    1236:	00 20       	and	r0, r0
    1238:	e9 f7       	brne	.-6      	;  0x1234
    123a:	af 01       	movw	r20, r30
    123c:	41 50       	subi	r20, 0x01	; 1
    123e:	51 09       	sbc	r21, r1
    1240:	46 1b       	sub	r20, r22
    1242:	57 0b       	sbc	r21, r23
    1244:	0c 94 ee 08 	jmp	0x11dc	;  0x11dc
    1248:	08 95       	ret
    124a:	a1 e2       	ldi	r26, 0x21	; 33
    124c:	1a 2e       	mov	r1, r26
    124e:	aa 1b       	sub	r26, r26
    1250:	bb 1b       	sub	r27, r27
    1252:	fd 01       	movw	r30, r26
    1254:	0d c0       	rjmp	.+26     	;  0x1270
    1256:	aa 1f       	adc	r26, r26
    1258:	bb 1f       	adc	r27, r27
    125a:	ee 1f       	adc	r30, r30
    125c:	ff 1f       	adc	r31, r31
    125e:	a2 17       	cp	r26, r18
    1260:	b3 07       	cpc	r27, r19
    1262:	e4 07       	cpc	r30, r20
    1264:	f5 07       	cpc	r31, r21
    1266:	20 f0       	brcs	.+8      	;  0x1270
    1268:	a2 1b       	sub	r26, r18
    126a:	b3 0b       	sbc	r27, r19
    126c:	e4 0b       	sbc	r30, r20
    126e:	f5 0b       	sbc	r31, r21
    1270:	66 1f       	adc	r22, r22
    1272:	77 1f       	adc	r23, r23
    1274:	88 1f       	adc	r24, r24
    1276:	99 1f       	adc	r25, r25
    1278:	1a 94       	dec	r1
    127a:	69 f7       	brne	.-38     	;  0x1256
    127c:	60 95       	com	r22
    127e:	70 95       	com	r23
    1280:	80 95       	com	r24
    1282:	90 95       	com	r25
    1284:	9b 01       	movw	r18, r22
    1286:	ac 01       	movw	r20, r24
    1288:	bd 01       	movw	r22, r26
    128a:	cf 01       	movw	r24, r30
    128c:	08 95       	ret
    128e:	ee 0f       	add	r30, r30
    1290:	ff 1f       	adc	r31, r31
    1292:	05 90       	lpm	r0, Z+
    1294:	f4 91       	lpm	r31, Z
    1296:	e0 2d       	mov	r30, r0
    1298:	09 94       	ijmp
    129a:	cf 93       	push	r28
    129c:	df 93       	push	r29
    129e:	82 30       	cpi	r24, 0x02	; 2
    12a0:	91 05       	cpc	r25, r1
    12a2:	10 f4       	brcc	.+4      	;  0x12a8
    12a4:	82 e0       	ldi	r24, 0x02	; 2
    12a6:	90 e0       	ldi	r25, 0x00	; 0
    12a8:	e0 91 97 04 	lds	r30, 0x0497	;  0x800497
    12ac:	f0 91 98 04 	lds	r31, 0x0498	;  0x800498
    12b0:	20 e0       	ldi	r18, 0x00	; 0
    12b2:	30 e0       	ldi	r19, 0x00	; 0
    12b4:	a0 e0       	ldi	r26, 0x00	; 0
    12b6:	b0 e0       	ldi	r27, 0x00	; 0
    12b8:	30 97       	sbiw	r30, 0x00	; 0
    12ba:	39 f1       	breq	.+78     	;  0x130a
    12bc:	40 81       	ld	r20, Z
    12be:	51 81       	ldd	r21, Z+1	; 0x01
    12c0:	48 17       	cp	r20, r24
    12c2:	59 07       	cpc	r21, r25
    12c4:	b8 f0       	brcs	.+46     	;  0x12f4
    12c6:	48 17       	cp	r20, r24
    12c8:	59 07       	cpc	r21, r25
    12ca:	71 f4       	brne	.+28     	;  0x12e8
    12cc:	82 81       	ldd	r24, Z+2	; 0x02
    12ce:	93 81       	ldd	r25, Z+3	; 0x03
    12d0:	10 97       	sbiw	r26, 0x00	; 0
    12d2:	29 f0       	breq	.+10     	;  0x12de
    12d4:	13 96       	adiw	r26, 0x03	; 3
    12d6:	9c 93       	st	X, r25
    12d8:	8e 93       	st	-X, r24
    12da:	12 97       	sbiw	r26, 0x02	; 2
    12dc:	2c c0       	rjmp	.+88     	;  0x1336
    12de:	90 93 98 04 	sts	0x0498, r25	;  0x800498
    12e2:	80 93 97 04 	sts	0x0497, r24	;  0x800497
    12e6:	27 c0       	rjmp	.+78     	;  0x1336
    12e8:	21 15       	cp	r18, r1
    12ea:	31 05       	cpc	r19, r1
    12ec:	31 f0       	breq	.+12     	;  0x12fa
    12ee:	42 17       	cp	r20, r18
    12f0:	53 07       	cpc	r21, r19
    12f2:	18 f0       	brcs	.+6      	;  0x12fa
    12f4:	a9 01       	movw	r20, r18
    12f6:	db 01       	movw	r26, r22
    12f8:	01 c0       	rjmp	.+2      	;  0x12fc
    12fa:	ef 01       	movw	r28, r30
    12fc:	9a 01       	movw	r18, r20
    12fe:	bd 01       	movw	r22, r26
    1300:	df 01       	movw	r26, r30
    1302:	02 80       	ldd	r0, Z+2	; 0x02
    1304:	f3 81       	ldd	r31, Z+3	; 0x03
    1306:	e0 2d       	mov	r30, r0
    1308:	d7 cf       	rjmp	.-82     	;  0x12b8
    130a:	21 15       	cp	r18, r1
    130c:	31 05       	cpc	r19, r1
    130e:	f9 f0       	breq	.+62     	;  0x134e
    1310:	28 1b       	sub	r18, r24
    1312:	39 0b       	sbc	r19, r25
    1314:	24 30       	cpi	r18, 0x04	; 4
    1316:	31 05       	cpc	r19, r1
    1318:	80 f4       	brcc	.+32     	;  0x133a
    131a:	8a 81       	ldd	r24, Y+2	; 0x02
    131c:	9b 81       	ldd	r25, Y+3	; 0x03
    131e:	61 15       	cp	r22, r1
    1320:	71 05       	cpc	r23, r1
    1322:	21 f0       	breq	.+8      	;  0x132c
    1324:	fb 01       	movw	r30, r22
    1326:	93 83       	std	Z+3, r25	; 0x03
    1328:	82 83       	std	Z+2, r24	; 0x02
    132a:	04 c0       	rjmp	.+8      	;  0x1334
    132c:	90 93 98 04 	sts	0x0498, r25	;  0x800498
    1330:	80 93 97 04 	sts	0x0497, r24	;  0x800497
    1334:	fe 01       	movw	r30, r28
    1336:	32 96       	adiw	r30, 0x02	; 2
    1338:	44 c0       	rjmp	.+136    	;  0x13c2
    133a:	fe 01       	movw	r30, r28
    133c:	e2 0f       	add	r30, r18
    133e:	f3 1f       	adc	r31, r19
    1340:	81 93       	st	Z+, r24
    1342:	91 93       	st	Z+, r25
    1344:	22 50       	subi	r18, 0x02	; 2
    1346:	31 09       	sbc	r19, r1
    1348:	39 83       	std	Y+1, r19	; 0x01
    134a:	28 83       	st	Y, r18
    134c:	3a c0       	rjmp	.+116    	;  0x13c2
    134e:	20 91 95 04 	lds	r18, 0x0495	;  0x800495
    1352:	30 91 96 04 	lds	r19, 0x0496	;  0x800496
    1356:	23 2b       	or	r18, r19
    1358:	41 f4       	brne	.+16     	;  0x136a
    135a:	20 91 02 01 	lds	r18, 0x0102	;  0x800102
    135e:	30 91 03 01 	lds	r19, 0x0103	;  0x800103
    1362:	30 93 96 04 	sts	0x0496, r19	;  0x800496
    1366:	20 93 95 04 	sts	0x0495, r18	;  0x800495
    136a:	20 91 00 01 	lds	r18, 0x0100	;  0x800100
    136e:	30 91 01 01 	lds	r19, 0x0101	;  0x800101
    1372:	21 15       	cp	r18, r1
    1374:	31 05       	cpc	r19, r1
    1376:	41 f4       	brne	.+16     	;  0x1388
    1378:	2d b7       	in	r18, 0x3d	; 61
    137a:	3e b7       	in	r19, 0x3e	; 62
    137c:	40 91 04 01 	lds	r20, 0x0104	;  0x800104
    1380:	50 91 05 01 	lds	r21, 0x0105	;  0x800105
    1384:	24 1b       	sub	r18, r20
    1386:	35 0b       	sbc	r19, r21
    1388:	e0 91 95 04 	lds	r30, 0x0495	;  0x800495
    138c:	f0 91 96 04 	lds	r31, 0x0496	;  0x800496
    1390:	e2 17       	cp	r30, r18
    1392:	f3 07       	cpc	r31, r19
    1394:	a0 f4       	brcc	.+40     	;  0x13be
    1396:	2e 1b       	sub	r18, r30
    1398:	3f 0b       	sbc	r19, r31
    139a:	28 17       	cp	r18, r24
    139c:	39 07       	cpc	r19, r25
    139e:	78 f0       	brcs	.+30     	;  0x13be
    13a0:	ac 01       	movw	r20, r24
    13a2:	4e 5f       	subi	r20, 0xFE	; 254
    13a4:	5f 4f       	sbci	r21, 0xFF	; 255
    13a6:	24 17       	cp	r18, r20
    13a8:	35 07       	cpc	r19, r21
    13aa:	48 f0       	brcs	.+18     	;  0x13be
    13ac:	4e 0f       	add	r20, r30
    13ae:	5f 1f       	adc	r21, r31
    13b0:	50 93 96 04 	sts	0x0496, r21	;  0x800496
    13b4:	40 93 95 04 	sts	0x0495, r20	;  0x800495
    13b8:	81 93       	st	Z+, r24
    13ba:	91 93       	st	Z+, r25
    13bc:	02 c0       	rjmp	.+4      	;  0x13c2
    13be:	e0 e0       	ldi	r30, 0x00	; 0
    13c0:	f0 e0       	ldi	r31, 0x00	; 0
    13c2:	cf 01       	movw	r24, r30
    13c4:	df 91       	pop	r29
    13c6:	cf 91       	pop	r28
    13c8:	08 95       	ret
    13ca:	cf 93       	push	r28
    13cc:	df 93       	push	r29
    13ce:	00 97       	sbiw	r24, 0x00	; 0
    13d0:	09 f4       	brne	.+2      	;  0x13d4
    13d2:	87 c0       	rjmp	.+270    	;  0x14e2
    13d4:	fc 01       	movw	r30, r24
    13d6:	32 97       	sbiw	r30, 0x02	; 2
    13d8:	13 82       	std	Z+3, r1	; 0x03
    13da:	12 82       	std	Z+2, r1	; 0x02
    13dc:	c0 91 97 04 	lds	r28, 0x0497	;  0x800497
    13e0:	d0 91 98 04 	lds	r29, 0x0498	;  0x800498
    13e4:	20 97       	sbiw	r28, 0x00	; 0
    13e6:	81 f4       	brne	.+32     	;  0x1408
    13e8:	20 81       	ld	r18, Z
    13ea:	31 81       	ldd	r19, Z+1	; 0x01
    13ec:	28 0f       	add	r18, r24
    13ee:	39 1f       	adc	r19, r25
    13f0:	80 91 95 04 	lds	r24, 0x0495	;  0x800495
    13f4:	90 91 96 04 	lds	r25, 0x0496	;  0x800496
    13f8:	82 17       	cp	r24, r18
    13fa:	93 07       	cpc	r25, r19
    13fc:	79 f5       	brne	.+94     	;  0x145c
    13fe:	f0 93 96 04 	sts	0x0496, r31	;  0x800496
    1402:	e0 93 95 04 	sts	0x0495, r30	;  0x800495
    1406:	6d c0       	rjmp	.+218    	;  0x14e2
    1408:	de 01       	movw	r26, r28
    140a:	20 e0       	ldi	r18, 0x00	; 0
    140c:	30 e0       	ldi	r19, 0x00	; 0
    140e:	ae 17       	cp	r26, r30
    1410:	bf 07       	cpc	r27, r31
    1412:	50 f4       	brcc	.+20     	;  0x1428
    1414:	12 96       	adiw	r26, 0x02	; 2
    1416:	4d 91       	ld	r20, X+
    1418:	5c 91       	ld	r21, X
    141a:	13 97       	sbiw	r26, 0x03	; 3
    141c:	9d 01       	movw	r18, r26
    141e:	41 15       	cp	r20, r1
    1420:	51 05       	cpc	r21, r1
    1422:	09 f1       	breq	.+66     	;  0x1466
    1424:	da 01       	movw	r26, r20
    1426:	f3 cf       	rjmp	.-26     	;  0x140e
    1428:	b3 83       	std	Z+3, r27	; 0x03
    142a:	a2 83       	std	Z+2, r26	; 0x02
    142c:	40 81       	ld	r20, Z
    142e:	51 81       	ldd	r21, Z+1	; 0x01
    1430:	84 0f       	add	r24, r20
    1432:	95 1f       	adc	r25, r21
    1434:	8a 17       	cp	r24, r26
    1436:	9b 07       	cpc	r25, r27
    1438:	71 f4       	brne	.+28     	;  0x1456
    143a:	8d 91       	ld	r24, X+
    143c:	9c 91       	ld	r25, X
    143e:	11 97       	sbiw	r26, 0x01	; 1
    1440:	84 0f       	add	r24, r20
    1442:	95 1f       	adc	r25, r21
    1444:	02 96       	adiw	r24, 0x02	; 2
    1446:	91 83       	std	Z+1, r25	; 0x01
    1448:	80 83       	st	Z, r24
    144a:	12 96       	adiw	r26, 0x02	; 2
    144c:	8d 91       	ld	r24, X+
    144e:	9c 91       	ld	r25, X
    1450:	13 97       	sbiw	r26, 0x03	; 3
    1452:	93 83       	std	Z+3, r25	; 0x03
    1454:	82 83       	std	Z+2, r24	; 0x02
    1456:	21 15       	cp	r18, r1
    1458:	31 05       	cpc	r19, r1
    145a:	29 f4       	brne	.+10     	;  0x1466
    145c:	f0 93 98 04 	sts	0x0498, r31	;  0x800498
    1460:	e0 93 97 04 	sts	0x0497, r30	;  0x800497
    1464:	3e c0       	rjmp	.+124    	;  0x14e2
    1466:	d9 01       	movw	r26, r18
    1468:	13 96       	adiw	r26, 0x03	; 3
    146a:	fc 93       	st	X, r31
    146c:	ee 93       	st	-X, r30
    146e:	12 97       	sbiw	r26, 0x02	; 2
    1470:	4d 91       	ld	r20, X+
    1472:	5d 91       	ld	r21, X+
    1474:	a4 0f       	add	r26, r20
    1476:	b5 1f       	adc	r27, r21
    1478:	ea 17       	cp	r30, r26
    147a:	fb 07       	cpc	r31, r27
    147c:	79 f4       	brne	.+30     	;  0x149c
    147e:	80 81       	ld	r24, Z
    1480:	91 81       	ldd	r25, Z+1	; 0x01
    1482:	84 0f       	add	r24, r20
    1484:	95 1f       	adc	r25, r21
    1486:	02 96       	adiw	r24, 0x02	; 2
    1488:	d9 01       	movw	r26, r18
    148a:	11 96       	adiw	r26, 0x01	; 1
    148c:	9c 93       	st	X, r25
    148e:	8e 93       	st	-X, r24
    1490:	82 81       	ldd	r24, Z+2	; 0x02
    1492:	93 81       	ldd	r25, Z+3	; 0x03
    1494:	13 96       	adiw	r26, 0x03	; 3
    1496:	9c 93       	st	X, r25
    1498:	8e 93       	st	-X, r24
    149a:	12 97       	sbiw	r26, 0x02	; 2
    149c:	e0 e0       	ldi	r30, 0x00	; 0
    149e:	f0 e0       	ldi	r31, 0x00	; 0
    14a0:	8a 81       	ldd	r24, Y+2	; 0x02
    14a2:	9b 81       	ldd	r25, Y+3	; 0x03
    14a4:	00 97       	sbiw	r24, 0x00	; 0
    14a6:	19 f0       	breq	.+6      	;  0x14ae
    14a8:	fe 01       	movw	r30, r28
    14aa:	ec 01       	movw	r28, r24
    14ac:	f9 cf       	rjmp	.-14     	;  0x14a0
    14ae:	ce 01       	movw	r24, r28
    14b0:	02 96       	adiw	r24, 0x02	; 2
    14b2:	28 81       	ld	r18, Y
    14b4:	39 81       	ldd	r19, Y+1	; 0x01
    14b6:	82 0f       	add	r24, r18
    14b8:	93 1f       	adc	r25, r19
    14ba:	20 91 95 04 	lds	r18, 0x0495	;  0x800495
    14be:	30 91 96 04 	lds	r19, 0x0496	;  0x800496
    14c2:	28 17       	cp	r18, r24
    14c4:	39 07       	cpc	r19, r25
    14c6:	69 f4       	brne	.+26     	;  0x14e2
    14c8:	30 97       	sbiw	r30, 0x00	; 0
    14ca:	29 f4       	brne	.+10     	;  0x14d6
    14cc:	10 92 98 04 	sts	0x0498, r1	;  0x800498
    14d0:	10 92 97 04 	sts	0x0497, r1	;  0x800497
    14d4:	02 c0       	rjmp	.+4      	;  0x14da
    14d6:	13 82       	std	Z+3, r1	; 0x03
    14d8:	12 82       	std	Z+2, r1	; 0x02
    14da:	d0 93 96 04 	sts	0x0496, r29	;  0x800496
    14de:	c0 93 95 04 	sts	0x0495, r28	;  0x800495
    14e2:	df 91       	pop	r29
    14e4:	cf 91       	pop	r28
    14e6:	08 95       	ret
    14e8:	a0 e0       	ldi	r26, 0x00	; 0
    14ea:	b0 e0       	ldi	r27, 0x00	; 0
    14ec:	ea e7       	ldi	r30, 0x7A	; 122
    14ee:	fa e0       	ldi	r31, 0x0A	; 10
    14f0:	0c 94 52 0b 	jmp	0x16a4	;  0x16a4
    14f4:	ec 01       	movw	r28, r24
    14f6:	cb 01       	movw	r24, r22
    14f8:	20 97       	sbiw	r28, 0x00	; 0
    14fa:	19 f4       	brne	.+6      	;  0x1502
    14fc:	0e 94 4d 09 	call	0x129a	;  0x129a
    1500:	b8 c0       	rjmp	.+368    	;  0x1672
    1502:	fe 01       	movw	r30, r28
    1504:	e6 0f       	add	r30, r22
    1506:	f7 1f       	adc	r31, r23
    1508:	9e 01       	movw	r18, r28
    150a:	22 50       	subi	r18, 0x02	; 2
    150c:	31 09       	sbc	r19, r1
    150e:	e2 17       	cp	r30, r18
    1510:	f3 07       	cpc	r31, r19
    1512:	08 f4       	brcc	.+2      	;  0x1516
    1514:	ac c0       	rjmp	.+344    	;  0x166e
    1516:	d9 01       	movw	r26, r18
    1518:	0d 91       	ld	r16, X+
    151a:	1c 91       	ld	r17, X
    151c:	11 97       	sbiw	r26, 0x01	; 1
    151e:	06 17       	cp	r16, r22
    1520:	17 07       	cpc	r17, r23
    1522:	b8 f0       	brcs	.+46     	;  0x1552
    1524:	05 30       	cpi	r16, 0x05	; 5
    1526:	11 05       	cpc	r17, r1
    1528:	08 f4       	brcc	.+2      	;  0x152c
    152a:	9f c0       	rjmp	.+318    	;  0x166a
    152c:	a8 01       	movw	r20, r16
    152e:	44 50       	subi	r20, 0x04	; 4
    1530:	51 09       	sbc	r21, r1
    1532:	46 17       	cp	r20, r22
    1534:	57 07       	cpc	r21, r23
    1536:	08 f4       	brcc	.+2      	;  0x153a
    1538:	98 c0       	rjmp	.+304    	;  0x166a
    153a:	02 50       	subi	r16, 0x02	; 2
    153c:	11 09       	sbc	r17, r1
    153e:	06 1b       	sub	r16, r22
    1540:	17 0b       	sbc	r17, r23
    1542:	01 93       	st	Z+, r16
    1544:	11 93       	st	Z+, r17
    1546:	6d 93       	st	X+, r22
    1548:	7c 93       	st	X, r23
    154a:	cf 01       	movw	r24, r30
    154c:	0e 94 e5 09 	call	0x13ca	;  0x13ca
    1550:	8c c0       	rjmp	.+280    	;  0x166a
    1552:	5b 01       	movw	r10, r22
    1554:	a0 1a       	sub	r10, r16
    1556:	b1 0a       	sbc	r11, r17
    1558:	4e 01       	movw	r8, r28
    155a:	80 0e       	add	r8, r16
    155c:	91 1e       	adc	r9, r17
    155e:	a0 91 97 04 	lds	r26, 0x0497	;  0x800497
    1562:	b0 91 98 04 	lds	r27, 0x0498	;  0x800498
    1566:	61 2c       	mov	r6, r1
    1568:	71 2c       	mov	r7, r1
    156a:	60 e0       	ldi	r22, 0x00	; 0
    156c:	70 e0       	ldi	r23, 0x00	; 0
    156e:	10 97       	sbiw	r26, 0x00	; 0
    1570:	09 f4       	brne	.+2      	;  0x1574
    1572:	49 c0       	rjmp	.+146    	;  0x1606
    1574:	a8 15       	cp	r26, r8
    1576:	b9 05       	cpc	r27, r9
    1578:	c9 f5       	brne	.+114    	;  0x15ec
    157a:	ed 90       	ld	r14, X+
    157c:	fc 90       	ld	r15, X
    157e:	11 97       	sbiw	r26, 0x01	; 1
    1580:	67 01       	movw	r12, r14
    1582:	42 e0       	ldi	r20, 0x02	; 2
    1584:	c4 0e       	add	r12, r20
    1586:	d1 1c       	adc	r13, r1
    1588:	ca 14       	cp	r12, r10
    158a:	db 04       	cpc	r13, r11
    158c:	78 f1       	brcs	.+94     	;  0x15ec
    158e:	47 01       	movw	r8, r14
    1590:	8a 18       	sub	r8, r10
    1592:	9b 08       	sbc	r9, r11
    1594:	64 01       	movw	r12, r8
    1596:	42 e0       	ldi	r20, 0x02	; 2
    1598:	c4 0e       	add	r12, r20
    159a:	d1 1c       	adc	r13, r1
    159c:	12 96       	adiw	r26, 0x02	; 2
    159e:	bc 90       	ld	r11, X
    15a0:	12 97       	sbiw	r26, 0x02	; 2
    15a2:	13 96       	adiw	r26, 0x03	; 3
    15a4:	ac 91       	ld	r26, X
    15a6:	b5 e0       	ldi	r27, 0x05	; 5
    15a8:	cb 16       	cp	r12, r27
    15aa:	d1 04       	cpc	r13, r1
    15ac:	40 f0       	brcs	.+16     	;  0x15be
    15ae:	b2 82       	std	Z+2, r11	; 0x02
    15b0:	a3 83       	std	Z+3, r26	; 0x03
    15b2:	91 82       	std	Z+1, r9	; 0x01
    15b4:	80 82       	st	Z, r8
    15b6:	d9 01       	movw	r26, r18
    15b8:	8d 93       	st	X+, r24
    15ba:	9c 93       	st	X, r25
    15bc:	09 c0       	rjmp	.+18     	;  0x15d0
    15be:	0e 5f       	subi	r16, 0xFE	; 254
    15c0:	1f 4f       	sbci	r17, 0xFF	; 255
    15c2:	0e 0d       	add	r16, r14
    15c4:	1f 1d       	adc	r17, r15
    15c6:	f9 01       	movw	r30, r18
    15c8:	11 83       	std	Z+1, r17	; 0x01
    15ca:	00 83       	st	Z, r16
    15cc:	eb 2d       	mov	r30, r11
    15ce:	fa 2f       	mov	r31, r26
    15d0:	61 15       	cp	r22, r1
    15d2:	71 05       	cpc	r23, r1
    15d4:	31 f0       	breq	.+12     	;  0x15e2
    15d6:	db 01       	movw	r26, r22
    15d8:	13 96       	adiw	r26, 0x03	; 3
    15da:	fc 93       	st	X, r31
    15dc:	ee 93       	st	-X, r30
    15de:	12 97       	sbiw	r26, 0x02	; 2
    15e0:	44 c0       	rjmp	.+136    	;  0x166a
    15e2:	f0 93 98 04 	sts	0x0498, r31	;  0x800498
    15e6:	e0 93 97 04 	sts	0x0497, r30	;  0x800497
    15ea:	3f c0       	rjmp	.+126    	;  0x166a
    15ec:	6d 91       	ld	r22, X+
    15ee:	7c 91       	ld	r23, X
    15f0:	11 97       	sbiw	r26, 0x01	; 1
    15f2:	66 16       	cp	r6, r22
    15f4:	77 06       	cpc	r7, r23
    15f6:	08 f4       	brcc	.+2      	;  0x15fa
    15f8:	3b 01       	movw	r6, r22
    15fa:	bd 01       	movw	r22, r26
    15fc:	12 96       	adiw	r26, 0x02	; 2
    15fe:	0d 90       	ld	r0, X+
    1600:	bc 91       	ld	r27, X
    1602:	a0 2d       	mov	r26, r0
    1604:	b4 cf       	rjmp	.-152    	;  0x156e
    1606:	60 91 95 04 	lds	r22, 0x0495	;  0x800495
    160a:	70 91 96 04 	lds	r23, 0x0496	;  0x800496
    160e:	68 15       	cp	r22, r8
    1610:	79 05       	cpc	r23, r9
    1612:	e9 f4       	brne	.+58     	;  0x164e
    1614:	68 16       	cp	r6, r24
    1616:	79 06       	cpc	r7, r25
    1618:	d0 f4       	brcc	.+52     	;  0x164e
    161a:	40 91 00 01 	lds	r20, 0x0100	;  0x800100
    161e:	50 91 01 01 	lds	r21, 0x0101	;  0x800101
    1622:	41 15       	cp	r20, r1
    1624:	51 05       	cpc	r21, r1
    1626:	41 f4       	brne	.+16     	;  0x1638
    1628:	4d b7       	in	r20, 0x3d	; 61
    162a:	5e b7       	in	r21, 0x3e	; 62
    162c:	60 91 04 01 	lds	r22, 0x0104	;  0x800104
    1630:	70 91 05 01 	lds	r23, 0x0105	;  0x800105
    1634:	46 1b       	sub	r20, r22
    1636:	57 0b       	sbc	r21, r23
    1638:	e4 17       	cp	r30, r20
    163a:	f5 07       	cpc	r31, r21
    163c:	c0 f4       	brcc	.+48     	;  0x166e
    163e:	f0 93 96 04 	sts	0x0496, r31	;  0x800496
    1642:	e0 93 95 04 	sts	0x0495, r30	;  0x800495
    1646:	f9 01       	movw	r30, r18
    1648:	91 83       	std	Z+1, r25	; 0x01
    164a:	80 83       	st	Z, r24
    164c:	0e c0       	rjmp	.+28     	;  0x166a
    164e:	0e 94 4d 09 	call	0x129a	;  0x129a
    1652:	7c 01       	movw	r14, r24
    1654:	00 97       	sbiw	r24, 0x00	; 0
    1656:	59 f0       	breq	.+22     	;  0x166e
    1658:	a8 01       	movw	r20, r16
    165a:	be 01       	movw	r22, r28
    165c:	0e 94 3e 0b 	call	0x167c	;  0x167c
    1660:	ce 01       	movw	r24, r28
    1662:	0e 94 e5 09 	call	0x13ca	;  0x13ca
    1666:	c7 01       	movw	r24, r14
    1668:	04 c0       	rjmp	.+8      	;  0x1672
    166a:	ce 01       	movw	r24, r28
    166c:	02 c0       	rjmp	.+4      	;  0x1672
    166e:	80 e0       	ldi	r24, 0x00	; 0
    1670:	90 e0       	ldi	r25, 0x00	; 0
    1672:	cd b7       	in	r28, 0x3d	; 61
    1674:	de b7       	in	r29, 0x3e	; 62
    1676:	ee e0       	ldi	r30, 0x0E	; 14
    1678:	0c 94 6e 0b 	jmp	0x16dc	;  0x16dc
    167c:	fb 01       	movw	r30, r22
    167e:	dc 01       	movw	r26, r24
    1680:	02 c0       	rjmp	.+4      	;  0x1686
    1682:	01 90       	ld	r0, Z+
    1684:	0d 92       	st	X+, r0
    1686:	41 50       	subi	r20, 0x01	; 1
    1688:	50 40       	sbci	r21, 0x00	; 0
    168a:	d8 f7       	brcc	.-10     	;  0x1682
    168c:	08 95       	ret
    168e:	fb 01       	movw	r30, r22
    1690:	dc 01       	movw	r26, r24
    1692:	01 90       	ld	r0, Z+
    1694:	0d 92       	st	X+, r0
    1696:	00 20       	and	r0, r0
    1698:	e1 f7       	brne	.-8      	;  0x1692
    169a:	08 95       	ret
    169c:	2f 92       	push	r2
    169e:	3f 92       	push	r3
    16a0:	4f 92       	push	r4
    16a2:	5f 92       	push	r5
    16a4:	6f 92       	push	r6
    16a6:	7f 92       	push	r7
    16a8:	8f 92       	push	r8
    16aa:	9f 92       	push	r9
    16ac:	af 92       	push	r10
    16ae:	bf 92       	push	r11
    16b0:	cf 92       	push	r12
    16b2:	df 92       	push	r13
    16b4:	ef 92       	push	r14
    16b6:	ff 92       	push	r15
    16b8:	0f 93       	push	r16
    16ba:	1f 93       	push	r17
    16bc:	cf 93       	push	r28
    16be:	df 93       	push	r29
    16c0:	cd b7       	in	r28, 0x3d	; 61
    16c2:	de b7       	in	r29, 0x3e	; 62
    16c4:	ca 1b       	sub	r28, r26
    16c6:	db 0b       	sbc	r29, r27
    16c8:	0f b6       	in	r0, 0x3f	; 63
    16ca:	f8 94       	cli
    16cc:	de bf       	out	0x3e, r29	; 62
    16ce:	0f be       	out	0x3f, r0	; 63
    16d0:	cd bf       	out	0x3d, r28	; 61
    16d2:	09 94       	ijmp
    16d4:	2a 88       	ldd	r2, Y+18	; 0x12
    16d6:	39 88       	ldd	r3, Y+17	; 0x11
    16d8:	48 88       	ldd	r4, Y+16	; 0x10
    16da:	5f 84       	ldd	r5, Y+15	; 0x0f
    16dc:	6e 84       	ldd	r6, Y+14	; 0x0e
    16de:	7d 84       	ldd	r7, Y+13	; 0x0d
    16e0:	8c 84       	ldd	r8, Y+12	; 0x0c
    16e2:	9b 84       	ldd	r9, Y+11	; 0x0b
    16e4:	aa 84       	ldd	r10, Y+10	; 0x0a
    16e6:	b9 84       	ldd	r11, Y+9	; 0x09
    16e8:	c8 84       	ldd	r12, Y+8	; 0x08
    16ea:	df 80       	ldd	r13, Y+7	; 0x07
    16ec:	ee 80       	ldd	r14, Y+6	; 0x06
    16ee:	fd 80       	ldd	r15, Y+5	; 0x05
    16f0:	0c 81       	ldd	r16, Y+4	; 0x04
    16f2:	1b 81       	ldd	r17, Y+3	; 0x03
    16f4:	aa 81       	ldd	r26, Y+2	; 0x02
    16f6:	b9 81       	ldd	r27, Y+1	; 0x01
    16f8:	ce 0f       	add	r28, r30
    16fa:	d1 1d       	adc	r29, r1
    16fc:	0f b6       	in	r0, 0x3f	; 63
    16fe:	f8 94       	cli
    1700:	de bf       	out	0x3e, r29	; 62
    1702:	0f be       	out	0x3f, r0	; 63
    1704:	cd bf       	out	0x3d, r28	; 61
    1706:	ed 01       	movw	r28, r26
    1708:	08 95       	ret
    170a:	10 e0       	ldi	r17, 0x00	; 0
    170c:	c4 eb       	ldi	r28, 0xB4	; 180
    170e:	d0 e0       	ldi	r29, 0x00	; 0
    1710:	04 c0       	rjmp	.+8      	;  0x171a
    1712:	fe 01       	movw	r30, r28
    1714:	0e 94 49 09 	call	0x1292	;  0x1292
    1718:	22 96       	adiw	r28, 0x02	; 2
    171a:	c6 3b       	cpi	r28, 0xB6	; 182
    171c:	d1 07       	cpc	r29, r17
    171e:	c9 f7       	brne	.-14     	;  0x1712
    1720:	f8 94       	cli
    1722:	ff cf       	rjmp	.-2      	;  0x1722
    1724:	00 00       	nop
    1726:	99 04       	cpc	r9, r9
    1728:	80 00       	.word	0x0080	; ????
    172a:	31 00       	.word	0x0031	; ????
    172c:	32 00       	.word	0x0032	; ????
    172e:	33 00       	.word	0x0033	; ????
    1730:	34 00       	.word	0x0034	; ????
    1732:	35 00       	.word	0x0035	; ????
    1734:	36 00       	.word	0x0036	; ????
    1736:	37 00       	.word	0x0037	; ????
    1738:	38 00       	.word	0x0038	; ????
    173a:	39 00       	.word	0x0039	; ????
    173c:	30 00       	.word	0x0030	; ????
    173e:	2a 00       	.word	0x002a	; ????
    1740:	23 00       	.word	0x0023	; ????
    1742:	75 70       	andi	r23, 0x05	; 5
    1744:	00 64       	ori	r16, 0x40	; 64
    1746:	6f 77       	andi	r22, 0x7F	; 127
    1748:	6e 00       	.word	0x006e	; ????
    174a:	6f 6b       	ori	r22, 0xBF	; 191
    174c:	00 6c       	ori	r16, 0xC0	; 192
    174e:	65 66       	ori	r22, 0x65	; 101
    1750:	74 00       	.word	0x0074	; ????
    1752:	72 69       	ori	r23, 0x92	; 146
    1754:	67 68       	ori	r22, 0x87	; 135
    1756:	74 00       	.word	0x0074	; ????
    1758:	41 00       	.word	0x0041	; ????
    175a:	42 00       	.word	0x0042	; ????
    175c:	43 00       	.word	0x0043	; ????
    175e:	44 00       	.word	0x0044	; ????
    1760:	2b 00       	.word	0x002b	; ????
    1762:	2d 00       	.word	0x002d	; ????
    1764:	73 75       	andi	r23, 0x53	; 83
    1766:	6e 7a       	andi	r22, 0xAE	; 174
    1768:	68 65       	ori	r22, 0x58	; 88
    176a:	68 61       	ori	r22, 0x18	; 24
    176c:	6e 67       	ori	r22, 0x7E	; 126
    176e:	00 00       	nop
    1770:	00 00       	nop
    1772:	00 5d       	subi	r16, 0xD0	; 208
    1774:	03 30       	cpi	r16, 0x03	; 3
    1776:	03 05       	cpc	r16, r3
    1778:	03 0d       	add	r16, r3
    177a:	03 20       	and	r0, r3
    177c:	03 2f       	mov	r16, r19
    177e:	03 00       	.word	0x0003	; ????
    1780:	00 00       	nop
    1782:	00 d1       	rcall	.+512    	;  0x1984
    1784:	06 4d       	sbci	r16, 0xD6	; 214
    1786:	08 53       	subi	r16, 0x38	; 56
    1788:	06 6c       	ori	r16, 0xC6	; 198
    178a:	06 5e       	subi	r16, 0xE6	; 230
    178c:	06 af       	std	Z+62, r16	; 0x3e
    178e:	06 0d       	add	r16, r6
    1790:	0a 00       	.word	0x000a	; ????
    1792:	6e 61       	ori	r22, 0x1E	; 30
    1794:	6e 00       	.word	0x006e	; ????
    1796:	69 6e       	ori	r22, 0xE9	; 233
    1798:	66 00       	.word	0x0066	; ????
    179a:	6f 76       	andi	r22, 0x6F	; 111
    179c:	66 00       	.word	0x0066	; ????
    179e:	2e 00       	.word	0x002e	; ????
    17a0:	ff ff       	.word	0xffff	; ????
    17a2:	ff ff       	.word	0xffff	; ????
    17a4:	ff ff       	.word	0xffff	; ????
    17a6:	ff ff       	.word	0xffff	; ????
    17a8:	ff ff       	.word	0xffff	; ????
    17aa:	ff ff       	.word	0xffff	; ????
    17ac:	ff ff       	.word	0xffff	; ????
    17ae:	ff ff       	.word	0xffff	; ????
    17b0:	ff ff       	.word	0xffff	; ????
    17b2:	ff ff       	.word	0xffff	; ????
    17b4:	ff ff       	.word	0xffff	; ????
    17b6:	ff ff       	.word	0xffff	; ????
    17b8:	ff ff       	.word	0xffff	; ????
    17ba:	ff ff       	.word	0xffff	; ????
    17bc:	ff ff       	.word	0xffff	; ????
    17be:	ff ff       	.word	0xffff	; ????
    17c0:	ff ff       	.word	0xffff	; ????
    17c2:	ff ff       	.word	0xffff	; ????
    17c4:	ff ff       	.word	0xffff	; ????
    17c6:	ff ff       	.word	0xffff	; ????
    17c8:	ff ff       	.word	0xffff	; ????
    17ca:	ff ff       	.word	0xffff	; ????
    17cc:	ff ff       	.word	0xffff	; ????
    17ce:	ff ff       	.word	0xffff	; ????
    17d0:	ff ff       	.word	0xffff	; ????
    17d2:	ff ff       	.word	0xffff	; ????
    17d4:	ff ff       	.word	0xffff	; ????
    17d6:	ff ff       	.word	0xffff	; ????
    17d8:	ff ff       	.word	0xffff	; ????
    17da:	ff ff       	.word	0xffff	; ????
    17dc:	ff ff       	.word	0xffff	; ????
    17de:	ff ff       	.word	0xffff	; ????
    17e0:	ff ff       	.word	0xffff	; ????
    17e2:	ff ff       	.word	0xffff	; ????
    17e4:	ff ff       	.word	0xffff	; ????
    17e6:	ff ff       	.word	0xffff	; ????
    17e8:	ff ff       	.word	0xffff	; ????
    17ea:	ff ff       	.word	0xffff	; ????
    17ec:	ff ff       	.word	0xffff	; ????
    17ee:	ff ff       	.word	0xffff	; ????
    17f0:	ff ff       	.word	0xffff	; ????
    17f2:	ff ff       	.word	0xffff	; ????
    17f4:	ff ff       	.word	0xffff	; ????
    17f6:	ff ff       	.word	0xffff	; ????
    17f8:	ff ff       	.word	0xffff	; ????
    17fa:	ff ff       	.word	0xffff	; ????
    17fc:	ff ff       	.word	0xffff	; ????
    17fe:	ff ff       	.word	0xffff	; ????
    1800:	ff ff       	.word	0xffff	; ????
    1802:	ff ff       	.word	0xffff	; ????
    1804:	ff ff       	.word	0xffff	; ????
    1806:	ff ff       	.word	0xffff	; ????
    1808:	ff ff       	.word	0xffff	; ????
    180a:	ff ff       	.word	0xffff	; ????
    180c:	ff ff       	.word	0xffff	; ????
    180e:	ff ff       	.word	0xffff	; ????
    1810:	ff ff       	.word	0xffff	; ????
    1812:	ff ff       	.word	0xffff	; ????
    1814:	ff ff       	.word	0xffff	; ????
    1816:	ff ff       	.word	0xffff	; ????
    1818:	ff ff       	.word	0xffff	; ????
    181a:	ff ff       	.word	0xffff	; ????
    181c:	ff ff       	.word	0xffff	; ????
    181e:	ff ff       	.word	0xffff	; ????
    1820:	ff ff       	.word	0xffff	; ????
    1822:	ff ff       	.word	0xffff	; ????
    1824:	ff ff       	.word	0xffff	; ????
    1826:	ff ff       	.word	0xffff	; ????
    1828:	ff ff       	.word	0xffff	; ????
    182a:	ff ff       	.word	0xffff	; ????
    182c:	ff ff       	.word	0xffff	; ????
    182e:	ff ff       	.word	0xffff	; ????
    1830:	ff ff       	.word	0xffff	; ????
    1832:	ff ff       	.word	0xffff	; ????
    1834:	ff ff       	.word	0xffff	; ????
    1836:	ff ff       	.word	0xffff	; ????
    1838:	ff ff       	.word	0xffff	; ????
    183a:	ff ff       	.word	0xffff	; ????
    183c:	ff ff       	.word	0xffff	; ????
    183e:	ff ff       	.word	0xffff	; ????
    1840:	ff ff       	.word	0xffff	; ????
    1842:	ff ff       	.word	0xffff	; ????
    1844:	ff ff       	.word	0xffff	; ????
    1846:	ff ff       	.word	0xffff	; ????
    1848:	ff ff       	.word	0xffff	; ????
    184a:	ff ff       	.word	0xffff	; ????
    184c:	ff ff       	.word	0xffff	; ????
    184e:	ff ff       	.word	0xffff	; ????
    1850:	ff ff       	.word	0xffff	; ????
    1852:	ff ff       	.word	0xffff	; ????
    1854:	ff ff       	.word	0xffff	; ????
    1856:	ff ff       	.word	0xffff	; ????
    1858:	ff ff       	.word	0xffff	; ????
    185a:	ff ff       	.word	0xffff	; ????
    185c:	ff ff       	.word	0xffff	; ????
    185e:	ff ff       	.word	0xffff	; ????
    1860:	ff ff       	.word	0xffff	; ????
    1862:	ff ff       	.word	0xffff	; ????
    1864:	ff ff       	.word	0xffff	; ????
    1866:	ff ff       	.word	0xffff	; ????
    1868:	ff ff       	.word	0xffff	; ????
    186a:	ff ff       	.word	0xffff	; ????
    186c:	ff ff       	.word	0xffff	; ????
    186e:	ff ff       	.word	0xffff	; ????
    1870:	ff ff       	.word	0xffff	; ????
    1872:	ff ff       	.word	0xffff	; ????
    1874:	ff ff       	.word	0xffff	; ????
    1876:	ff ff       	.word	0xffff	; ????
    1878:	ff ff       	.word	0xffff	; ????
    187a:	ff ff       	.word	0xffff	; ????
    187c:	ff ff       	.word	0xffff	; ????
    187e:	ff ff       	.word	0xffff	; ????
    1880:	ff ff       	.word	0xffff	; ????
    1882:	ff ff       	.word	0xffff	; ????
    1884:	ff ff       	.word	0xffff	; ????
    1886:	ff ff       	.word	0xffff	; ????
    1888:	ff ff       	.word	0xffff	; ????
    188a:	ff ff       	.word	0xffff	; ????
    188c:	ff ff       	.word	0xffff	; ????
    188e:	ff ff       	.word	0xffff	; ????
    1890:	ff ff       	.word	0xffff	; ????
    1892:	ff ff       	.word	0xffff	; ????
    1894:	ff ff       	.word	0xffff	; ????
    1896:	ff ff       	.word	0xffff	; ????
    1898:	ff ff       	.word	0xffff	; ????
    189a:	ff ff       	.word	0xffff	; ????
    189c:	ff ff       	.word	0xffff	; ????
    189e:	ff ff       	.word	0xffff	; ????
    18a0:	ff ff       	.word	0xffff	; ????
    18a2:	ff ff       	.word	0xffff	; ????
    18a4:	ff ff       	.word	0xffff	; ????
    18a6:	ff ff       	.word	0xffff	; ????
    18a8:	ff ff       	.word	0xffff	; ????
    18aa:	ff ff       	.word	0xffff	; ????
    18ac:	ff ff       	.word	0xffff	; ????
    18ae:	ff ff       	.word	0xffff	; ????
    18b0:	ff ff       	.word	0xffff	; ????
    18b2:	ff ff       	.word	0xffff	; ????
    18b4:	ff ff       	.word	0xffff	; ????
    18b6:	ff ff       	.word	0xffff	; ????
    18b8:	ff ff       	.word	0xffff	; ????
    18ba:	ff ff       	.word	0xffff	; ????
    18bc:	ff ff       	.word	0xffff	; ????
    18be:	ff ff       	.word	0xffff	; ????
    18c0:	ff ff       	.word	0xffff	; ????
    18c2:	ff ff       	.word	0xffff	; ????
    18c4:	ff ff       	.word	0xffff	; ????
    18c6:	ff ff       	.word	0xffff	; ????
    18c8:	ff ff       	.word	0xffff	; ????
    18ca:	ff ff       	.word	0xffff	; ????
    18cc:	ff ff       	.word	0xffff	; ????
    18ce:	ff ff       	.word	0xffff	; ????
    18d0:	ff ff       	.word	0xffff	; ????
    18d2:	ff ff       	.word	0xffff	; ????
    18d4:	ff ff       	.word	0xffff	; ????
    18d6:	ff ff       	.word	0xffff	; ????
    18d8:	ff ff       	.word	0xffff	; ????
    18da:	ff ff       	.word	0xffff	; ????
    18dc:	ff ff       	.word	0xffff	; ????
    18de:	ff ff       	.word	0xffff	; ????
    18e0:	ff ff       	.word	0xffff	; ????
    18e2:	ff ff       	.word	0xffff	; ????
    18e4:	ff ff       	.word	0xffff	; ????
    18e6:	ff ff       	.word	0xffff	; ????
    18e8:	ff ff       	.word	0xffff	; ????
    18ea:	ff ff       	.word	0xffff	; ????
    18ec:	ff ff       	.word	0xffff	; ????
    18ee:	ff ff       	.word	0xffff	; ????
    18f0:	ff ff       	.word	0xffff	; ????
    18f2:	ff ff       	.word	0xffff	; ????
    18f4:	ff ff       	.word	0xffff	; ????
    18f6:	ff ff       	.word	0xffff	; ????
    18f8:	ff ff       	.word	0xffff	; ????
    18fa:	ff ff       	.word	0xffff	; ????
    18fc:	ff ff       	.word	0xffff	; ????
    18fe:	ff ff       	.word	0xffff	; ????
