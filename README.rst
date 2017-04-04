xt_ndpi-kmod
============

This RPM provides nDPI kernel and iptables modules for CentOS 7.

Using
-----

This procedure has been tested with kernel-3.10.0-514.el7.x86_64 from CentOS 7.3.

1. Install the kernel module::

     yum install xt_ndpi-kmod

2. Load the kernel module: ::

     modrpobe xt_ndpi

3. Check the module is correctly loaded: ::

     cat /proc/net/xt_ndpi/proto | head -n5

   The output should be like this: ::

     #id     mark ~mask     name   # count #version 1.7.0
     00         0/000000ff unknown          # 0
     01         1/000000ff ftp_control      # 0
     02         2/000000ff mail_pop         # 0
     03         3/000000ff mail_smtp        # 0

4. Create a sample rule which blocks facebook: ::

     iptables -I OUTPUT -m ndpi --facebook -j DROP
 

To unload the module, use: ::

    conntrack -F && rmmod xt_ndpi


Building RPM
------------

To build the RPM use mock with the EPEL 7 configuration file.

Compiling from source
---------------------

Compile the kernel and iptable modules inside a CentOS 7: ::

  yum -y install kernel-devel gcc iptables-devel libpcap-devel autoconf automake libtool
  wget https://github.com/vel21ripn/nDPI/archive/netfilter.tar.gz
  tar xvzf netfilter.tar.gz
  cd nDPI-netfilter/
  ./autogen.sh
  wget http://devel.aanet.ru/ndpi/nDPI-1.7.20151023.tar.gz
  tar xvzf nDPI-1.7.20151023.tar.gz
  cd ndpi-netfilter
  sed -e '/^MODULES_DIR/d' -e '/^KERNEL_DIR/d' -i src/Makefile
  MODULES_DIR=/lib/modules/3.10.0-514.el7.x86_64 KERNEL_DIR=$MODULES_DIR/build/ NDPI_PATH=$PWD/nDPI-1.7.20151023 make
  MODULES_DIR=/lib/modules/3.10.0-514.el7.x86_64 KERNEL_DIR=$MODULES_DIR/build/ make install
  MODULES_DIR=/lib/modules/3.10.0-514.el7.x86_64 KERNEL_DIR=$MODULES_DIR/build/ make modules_install

Links
-----

- Gihub repo: https://github.com/vel21ripn/nDPI/tree/netfilter
- Official site: http://devel.aanet.ru/ndpi

