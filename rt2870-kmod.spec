# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
#%%define buildforkernels newest

Name:		rt2870-kmod
Version:	1.4.0.0
Release:	4%{?dist}
Summary:	Kernel module for wireless devices with Ralink's rt2870 chipsets

Group:		System Environment/Kernel
License:	GPLv2+
URL:		http://www.ralinktech.com/ralink/Home/Support/Linux.html
Source0:	http://www.ralinktech.com.tw/data/drivers/2008_0925_RT2870_Linux_STA_v1.4.0.0.tar.bz2
Source11:	rt2870-kmodtool-excludekernel-filterfile

Patch1:		rt2870-linksys-wusb100-wusb600n-support.patch
Patch2:		rt2870-Makefile.x-fixes.patch
Patch3:		rt2870-NetworkManager-support.patch
Patch4:		rt2870-strip-tftpboot-copy.patch
Patch5:		rt2870-2.6.29-compile.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	%{_bindir}/kmodtool

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i586 i686 x86_64 ppc ppc64

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This package contains the documentation and configuration files for the Ralink
Driver for WiFi, a linux device driver for 802.11a/b/g universal NIC cards - 
either PCI, PCIe or MiniPCI - that use Ralink rt2870 chipsets.

%prep
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

%patch1 -p1 -b .linksys
%patch2 -p1 -b .rpmbuild
%patch3 -p1 -b .NetworkManager
%patch4 -p1 -b .tftpboot

for kernel_version in %{?kernel_versions} ; do
 cp -a *RT2870_Linux_STA* _kmod_build_${kernel_version%%___*}
 pushd _kmod_build_${kernel_version%%___*}
  if [[ $kernel_version > "2.6.29" ]]; then
%patch5 -p2 -b .2.6.29
  fi
 popd
done

%build
for kernel_version in %{?kernel_versions}; do
 make -C _kmod_build_${kernel_version%%___*} LINUX_SRC="${kernel_version##*___}"
done

%install
rm -rf ${RPM_BUILD_ROOT}
for kernel_version in %{?kernel_versions}; do
 make -C _kmod_build_${kernel_version%%___*} KERNELPATH="${kernel_version##*___}" KERNELRELEASE="${kernel_version%%___*}" INST_DIR=${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix} install
done

chmod 0755 $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/*/%{kmodinstdir_postfix}/*
%{?akmod_install}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Jan 11 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.4.0.0-4
- Add a patch for compilation against kernels >= 2.6.29

* Sat Dec 20 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-3.1
- rebuild for latest Fedora kernel;

* Fri Dec 19 2008 Jarod Wilson <jarod@wilsonet.com> - 1.4.0.0-3
- add device ID for Linksys WUSB600N

* Sat Dec 06 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-2.1
- rebuild for latest Fedora kernel;

* Thu Dec 04 2008 Orcan Ogetbil <orcanbahri [AT] yahoo [DOT] com> - 1.4.0.0-2
- removed the iwe-stream patch since it is not needed for 2.6.27+ kernels

* Tue Dec 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.10
- rebuild for latest Fedora kernel;

* Sat Nov 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.9
- rebuild for latest Fedora kernel;

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.8
- rebuild for latest Fedora kernel;

* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.7
- rebuild for latest Fedora kernel;

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.6
- rebuild for latest Fedora kernel;

* Sun Nov 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.5
- rebuild for latest Fedora kernel;

* Sun Nov 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.4
- rebuild for latest rawhide kernel;

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.3
- rebuild for latest rawhide kernel; enable ppc and ppc64 again

* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-1.2
- rebuild for latest rawhide kernel

* Sun Oct 05 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.4.0.0-1.1
- adjust make call in build to build properly is running kernel and target
  kernel are different

* Sat Oct 04 2008  Orcan Ogetbil <orcanbahri[AT]yahoo[DOT]com> - 1.4.0.0-1
- Rebuild for 1.4.0.0

* Sat Oct 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.3.1.0-4
- Various small adjustments
- exclude ppc due to bugs (see comments)

* Sat Sep 26 2008  Orcan Ogetbil <orcanbahri[AT]yahoo[DOT]com> - 1.3.1.0-3
- Re-wrote the description, removed supported hardware info. 
- Renamed SourceDir to SourceName

* Thu Sep 22 2008  Orcan Ogetbil <orcanbahri[AT]yahoo[DOT]com> - 1.3.1.0-2
- Some cleanup in the SPEC file to match standards
- Separated the patches
- License is GPLv2+

* Thu Sep 20 2008  Orcan Ogetbil <orcanbahri[AT]yahoo[DOT]com> - 1.3.1.0-1
- Initial build. The patch fixes compilation problems for kernels >= 2.6.25 . Also adds support for Linksys WUSB100.
