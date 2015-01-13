obj-m += add_mark_to_dmesg.o
INC=-I/usr/include

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	rm *.ko
	rm *.o
	rm *.mod.?
	rm modules.order
	rm Module.symvers 
