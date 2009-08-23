# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels newest

Name:		rt2870-kmod
Version:	2.1.2.0
Release:	2%{?dist}.1
Summary:	Kernel module for wireless devices with Ralink's rt2870 chipsets

Group:		System Environment/Kernel
License:	GPLv2+
URL:		http://www.ralinktech.com/ralink/Home/Support/Linux.html
Source0:	http://www.ralinktech.com.tw/data/drivers/2009_0521_RT2870_Linux_STA_V%{version}.tgz
Source11:	rt2870-kmodtool-excludekernel-filterfile
Patch1:		rt2870-no2.4-in-kernelversion.patch
Patch2:		rt2870-Makefile.x-fixes.patch
Patch3:		rt2870-NetworkManager-support.patch
Patch4:		rt2870-strip-tftpboot-copy.patch
Patch5:		rt2870-2.6.31-compile.patch
Patch6:		rt2870-suppress-flood.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	%{_bindir}/kmodtool

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:	i586 i686 x86_64 ppc ppc64

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
pushd *RT2870*Linux*STA*
%patch1 -p1 -b .no24
%patch2 -p1 -b .rpmbuild
%patch3 -p1 -b .NetworkManager
%patch4 -p1 -b .tftpboot
%patch5 -p1 -b .2.6.31
%patch6 -p1 -b .messageflood
popd

# Fix permissions
for ext in c h; do
 find  . -name "*.$ext" -exec chmod -x '{}' \;
done

for kernel_version in %{?kernel_versions} ; do
 cp -a *RT2870*Linux*STA* _kmod_build_${kernel_version%%___*}
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
* Sun Aug 23 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-2.1
- rebuild for new kernels

* Sat Aug 22 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.2.0-2
- Suppress a flood of system log messages
- Fix for kernels >= 2.6.31

* Sat Aug 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-1.9
- rebuild for new kernels

* Sat Aug 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-1.8
- rebuild for new kernels

* Fri Aug 14 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-1.7
- rebuild for new kernels

* Fri Jul 31 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-1.6
- rebuild for new kernels

* Tue Jul 14 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-1.5
- rebuild for new kernels

* Sun Jun 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-1.4
- rebuild for new kernels

* Sun Jun 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-1.3
- rebuild for new kernels

* Thu May 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-1.2
- rebuild for new kernels

* Wed May 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-1.1
- rebuild for new kernels

* Fri May 22 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.2.0-1
- version update (2.1.2.0)

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.5
- rebuild for new kernels

* Wed May 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.4
- rebuild for new kernels

* Tue May 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.3
- rebuild for new kernels

* Sat May 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.2
- rebuild for new kernels

* Sun Apr 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.1
- rebuild for new kernels

* Sat Apr 24 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.1.0-1
- version update (2.1.1.0)

* Sun Apr 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.0.0-2.1
- rebuild for new kernels

* Thu Mar 26 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.0.0-2
- Bugfix: kmod doesn't compile when the kernel version has a "2.4" substring

* Thu Mar 26 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.0.0-1
- New upstream version
- Drop additional-devices patch since it is upstreamed

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-7.1
- rebuild for latest Fedora kernel;

* Wed Feb 11 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.4.0.0-7
- Add Sweex WL303 support

* Sun Feb 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-6.1
- rebuild for latest Fedora kernel;

* Sun Jan 25 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.4.0.0-6
- Add Belkin F5D8053 support

* Sun Jan 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-5.2
- rebuild for latest Fedora kernel;

* Sun Jan 18 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-5.1
- rebuild for latest Fedora kernel;

* Thu Jan 15 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.4.0.0-5
- Add Buffalo WLI-UC-G300N support

* Sun Jan 11 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.4.0.0-4
- Add a patch for compilation against kernels >= 2.6.29

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-3.4
- rebuild for latest Fedora kernel;

* Sun Jan 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-3.3
- rebuild for latest Fedora kernel;

* Sun Dec 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-3.2
- rebuild for latest Fedora kernel;

* Sun Dec 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-3.1
- rebuild for latest Fedora kernel;

* Wed Dec 17 2008 Jarod Wilson <jarod@wilsonet.com> - 1.4.0.0-3
- Add device ID for Linksys WUSB600N

* Sun Dec 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0.0-2.1
- rebuild for latest Fedora kernel;

* Thu Dec 04 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.4.0.0-2
- removed the iwe-stream patch since it is not needed for 2.6.27+ kernels

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

* Sat Oct 04 2008  Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.4.0.0-1
- Rebuild for 1.4.0.0

* Sat Oct 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.3.1.0-4
- Various small adjustments
- exclude ppc due to bugs (see comments)

* Sat Sep 26 2008  Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.3.1.0-3
- Re-wrote the description, removed supported hardware info. 
- Renamed SourceDir to SourceName

* Thu Sep 22 2008  Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.3.1.0-2
- Some cleanup in the SPEC file to match standards
- Separated the patches
- License is GPLv2+

* Thu Sep 20 2008  Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.3.1.0-1
- Initial build. The patch fixes compilation problems for kernels >= 2.6.25 . Also adds support for Linksys WUSB100.
