xt_ndpi-kmod
============

This RPM provides NDPI kernel and iptable modules for CentOS 7.
The kernel module is compiled against a kernel-lt from elrepo: http://elrepo.org/tiki/kernel-lt

Using
-----

This procedure has been tested with kernel-lt-4.4.19-1.el7.elrepo.x86_64.

1. Make sure to install the kernel-lt and the kernel module::

     yum install http://elrepo.org/linux/kernel/el7/x86_64/RPMS/elrepo-release-7.0-2.el7.elrepo.noarch.rpm -y
     yum --enablerepo=elrepo-kernel install kernel-lt
     yum install xt_ndpi-kmod

2. Reboot the machine 

3. At boot menu select the kernel-lt

4. Load the kernel module: ::

     modrpobe xt_ndpi

5. Check the module is correctly loaded: ::

     cat /proc/net/xt_ndpi/proto | head -n5

   The output should be like this: ::

     #id     mark ~mask     name   # count #version 1.7.0
     00         0/000000ff unknown          # 0
     01         1/000000ff ftp_control      # 0
     02         2/000000ff mail_pop         # 0
     03         3/000000ff mail_smtp        # 0

6. Create a sample rule which blocks facebook: ::

     iptables -I OUTPUT -m ndpi --facebook -j DROP
 

To unload the module, use: ::

    conntrack -F && rmmod xt_ndpi


Building RPM
------------

To build the RPM use mock with the EPEL 7 configuration file.
Before starting the build, add the elerpo-kernel repository
to your mock configuration : ::

  [elrepo-kernel]
  name=ELRepo.org Community Enterprise Linux Kernel Repository - el7
  baseurl=http://elrepo.org/linux/kernel/el7/$basearch/
        http://mirrors.coreix.net/elrepo/kernel/el7/$basearch/
        http://jur-linux.org/download/elrepo/kernel/el7/$basearch/
        http://repos.lax-noc.com/elrepo/kernel/el7/$basearch/
        http://mirror.ventraip.net.au/elrepo/kernel/el7/$basearch/
  mirrorlist=http://mirrors.elrepo.org/mirrors-elrepo-kernel.el7
  enabled=1
  gpgcheck=0
  gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-elrepo.org
  protect=0


Compiling from source
---------------------

Compile the kernel and iptable modules inside a CentOS 7: ::

  yum install http://elrepo.org/linux/kernel/el7/x86_64/RPMS/elrepo-release-7.0-2.el7.elrepo.noarch.rpm -y
  yum --enablerepo=elrepo-kernel install kernel-lt kernel-lt-devel
  yum -y install kernel-devel gcc iptables-devel libpcap-devel autoconf automake libtool
  wget https://github.com/vel21ripn/nDPI/archive/netfilter.tar.gz
  tar xvzf netfilter.tar.gz
  cd nDPI-netfilter/
  ./autogen.sh
  wget http://devel.aanet.ru/ndpi/nDPI-1.7.20151023.tar.gz
  tar xvzf nDPI-1.7.20151023.tar.gz
  cd ndpi-netfilter
  sed -e '/^MODULES_DIR/d' -e '/^KERNEL_DIR/d' -i src/Makefile
  MODULES_DIR=/lib/modules/4.4.19-1.el7.elrepo.x86_64 KERNEL_DIR=$MODULES_DIR/build/ NDPI_PATH=$PWD/nDPI-1.7.20151023 make
  MODULES_DIR=/lib/modules/4.4.19-1.el7.elrepo.x86_64 KERNEL_DIR=$MODULES_DIR/build/ make install
  MODULES_DIR=/lib/modules/4.4.19-1.el7.elrepo.x86_64 KERNEL_DIR=$MODULES_DIR/build/ make modules_install

Links
-----

- Gihub repo: https://github.com/vel21ripn/nDPI/tree/netfilter
- Official site: http://devel.aanet.ru/ndpi

