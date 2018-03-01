### Copy the contents of the iso
mount -o loop isofile.sio /mnt

cp -rT /mnt ~tmp/debianiso/
chmod +w ~/tmp/debianiso/isolinux/isolinux.bin

### Generate new md5sums
md5sum `find ! -name "md5sum.txt" ! -path "./isolinux/*" -follow -type f` > md5sum.txt

### isolinux.cfg

_the md5-sum for preseed file is required in debian, optional i ubuntu_

    # D-I config version 2.0
    # search path for the c32 support libraries (libcom32, libutil etc.)
    #path
    UI vesamenu.c32
    DEFAULT preseed
    TIMEOUT 70
    LABEL preseed
        MENU LABEL ^Install Debian 9 (preseed)
        KERNEL /install.amd/vmlinuz
        APPEND initrd=/install.amd/initrd.gz gfxpayload=800x600x16,800x600 \
        hostname=preseeded DEBCONF_DEBUG=5 locale=en_US keymap=se locale=en_US \
        keyboard-configuration/layoutcode=se hostname=preseeded \
        domain=sub.domain.tld ipv6.disable_ipv6=0 --- auto=true \
        file=/cdrom/install.amd/preseed.cfg \
        preseed-md5=3c1ddc92b5344fdb04f57b1a035dcc33 quiet
    LABEL sda
        MENU LABEL Boot first HD
        kernel chain.c32
        append hd0 0


### Generate the iso
**Debian9**
genisoimage -r -J -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -o debian9.iso debianiso /no-emul-boot
isohybrid debian9.iso

**Ubuntu 16.04**
genisoimage -r -J -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -o ubuntu1604.iso ubuntuiso

