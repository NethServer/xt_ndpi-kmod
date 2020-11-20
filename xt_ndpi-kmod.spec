# Define the kmod package name here.
%define kmod_name xt_ndpi
%define ndpi_git_ver 96cf7764577603f1bd2896d414532afe625f6667

# If kversion isn't defined on the rpmbuild line, define it here.
%{!?kversion: %define kversion 3.10.0-1160.6.1.el7.%{_target_cpu}}

Name:    %{kmod_name}-kmod
Version: 2.8.2
Release: 1%{?dist}
Group:   System Environment/Kernel
License: GPLv2
Summary: %{kmod_name} kernel module(s)
URL:     http://www.kernel.org/

BuildRequires: redhat-rpm-config, perl, kernel-devel, gcc, iptables-devel, libpcap-devel, autoconf, automake, libtool
BuildRequires: kernel = 3.10.0-1160.6.1.el7, kernel-devel = 3.10.0-1160.6.1.el7
Requires: kernel >= 3.10.0-1160.6.1
ExclusiveArch: x86_64

# Sources.
Source0: https://github.com/vel21ripn/nDPI/archive/%{ndpi_git_ver}.tar.gz
Source5:  GPL-v2.0.txt
Source10: kmodtool-%{kmod_name}-el7.sh
Patch1: ndpi-netfilter_rhel7.5.patch
Patch2: ndpi-netfilter_nethserver_id.patch
Patch3: ndpi-netfilter_rhel7.6.patch

# Magic hidden here.
%{expand:%(sh %{SOURCE10} rpmtemplate %{kmod_name} %{kversion} "")}

# Disable the building of the debug package(s).
%define debug_package %{nil}

%description
This package provides the %{kmod_name} kernel module(s).
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.

%prep
%setup -q -n nDPI-%{ndpi_git_ver}
%patch1 -p1
%patch2 -p1
%patch3 -p1
./autogen.sh
( cd src/lib ; make ndpi_network_list.c.inc )
cd ndpi-netfilter
sed -e '/^MODULES_DIR/d' -e '/^KERNEL_DIR/d' -i src/Makefile
MODULES_DIR=/lib/modules/%{kversion} KERNEL_DIR=$MODULES_DIR/build/ make
echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf

%build

%install
%{__install} -d %{buildroot}/usr/lib64/xtables
install ndpi-netfilter/ipt/libxt_ndpi.so %{buildroot}/usr/lib64/xtables
ln -fs libxt_ndpi.so %{buildroot}/usr/lib64/xtables/libxt_NDPI.so
%{__install} -d %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__install} ndpi-netfilter/src/%{kmod_name}.ko %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
touch kmod-%{kmod_name}.conf
%{__install} kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} -d %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
%{__install} %{SOURCE5} %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/

# Strip the modules(s).
find %{buildroot} -type f -name \*.ko -exec %{__strip} --strip-debug \{\} \;

# Sign the modules(s).
%if %{?_with_modsign:1}%{!?_with_modsign:0}
# If the module signing keys are not defined, define them here.
%{!?privkey: %define privkey %{_sysconfdir}/pki/SECURE-BOOT-KEY.priv}
%{!?pubkey: %define pubkey %{_sysconfdir}/pki/SECURE-BOOT-KEY.der}
for module in $(find %{buildroot} -type f -name \*.ko);
do %{__perl} /usr/src/kernels/%{kversion}/scripts/sign-file \
    sha256 %{privkey} %{pubkey} $module;
done
%endif

%clean
%{__rm} -rf %{buildroot}

%changelog
* Fri Nov 20 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.8.2-1
- Kernel 3.10.0-1160: rebuild kernel modules - NethServer/dev#6341

* Wed Oct 16 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.8.1-1
- Bump release to override released RPM with git commit - NethServer/dev#5868

* Tue Oct 01 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.8.0-1
- nDPI: update to 2.8.0 for kernel-3.10.0-1062 - NethServer/dev#5841

* Wed Dec 05 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.4.0-1
- Firewall: update to nDPI-netfilter-2.2 and nDPI-2.4  - NethServer/dev#5645

* Wed May 16 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.4-1
- nDPI: support CentOS 7.5 - NethServer/dev#5482

* Thu Dec 07 2017 Filippo Carletti <filippo.carletti@gmail.com> - 2.0.3-1
- Do NOT compress module -- Bug NethServer/dev#5385

* Fri Nov 24 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.2-1
- shorewall: some netfilter helpers not loaded - Bug NethServer/dev#5385

* Tue May 30 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.1-1
- nDPI: BUG: scheduling while atomic - Bug NethServer/dev#5301

* Wed Dec 14 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.0-1
- Release for CentOS 7.3 - NethServer/dev#5170

* Fri Dec 02 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.0-1
- Built on kernel 3.10.0-514.el7

* Wed Sep 28 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.0-1
- First release - NethServer/dev#5102
- Built on kernel-lt 4.4.22-1

