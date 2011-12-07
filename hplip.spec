Summary: HP Linux Imaging and Printing Project
Name: hplip
Version: 3.9.8
Release: 33%{?dist}
License: GPLv2+ and MIT
Group: System Environment/Daemons
Conflicts: system-config-printer < 0.6.132
Obsoletes: hpoj <= 0.91
Obsoletes: xojpanel <= 0.91

# Need selinux-policy to know about new port numbers (bug #201357).
Conflicts: selinux-policy < 3.0.3-3

Url: http://hplip.sourceforge.net/
Source0: http://kent.dl.sourceforge.net/sourceforge/hplip/%{name}-%{version}.tar.gz
Patch1: hplip-hpcups-reorder.patch
Patch2: hplip-strstr-const.patch
Patch3: hplip-ui-optional.patch
Patch4: hplip-no-asm.patch
Patch5: hplip-clear-previous-state-reasons.patch
Patch6: hplip-state-reasons-newline.patch
Patch7: hplip-parenths.patch
Patch8: hplip-retry-open.patch
Patch9: hplip-requirespageregion.patch
Patch10: hplip-discovery-method.patch
Patch11: hplip-device-reconnected.patch
Patch12: hplip-duplex-vs-number-up.patch
Patch13: hplip-plugin-error.patch
Patch14: hplip-hpcups-sigpipe.patch
Patch15: hplip-hpcups-plugin.patch
Patch16: hplip-bad-low-ink-warning.patch
Patch17: hplip-preferences-crash.patch
Patch18: hplip-tray-icon-crash.patch
Patch19: hplip-snmp-quirks.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(pre): /sbin/service
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(preun): /sbin/chkconfig

%define hpijs_epoch 1
Requires: hpijs = %{hpijs_epoch}:%{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: python-imaging
Requires: hal

BuildRequires: net-snmp-devel
BuildRequires: cups-devel
BuildRequires: python-devel
BuildRequires: libjpeg-devel
BuildRequires: desktop-file-utils
BuildRequires: libusb-devel
BuildRequires: openssl-devel
BuildRequires: sane-backends-devel
BuildRequires: dbus-devel

%description
The Hewlett-Packard Linux Imaging and Printing Project provides
drivers for HP printers and multi-function peripherals.

%package common
Summary: Files needed by the HPLIP printer and scanner drivers
Group: System Environment/Libraries
License: GPLv2+

%description common
Files needed by the HPLIP printer and scanner drivers.

%package libs
Summary: HPLIP libraries
Group: System Environment/Libraries
License: GPLv2+ and MIT
Requires: %{name}-common = %{version}-%{release}

%description libs
Libraries needed by HPLIP.

%package gui
Summary: HPLIP graphical tools
Group: Applications/System
License: BSD
Requires: PyQt4
Requires: python-reportlab
Requires(post): desktop-file-utils >= 0.2.92
Requires(postun): desktop-file-utils >= 0.2.92
Requires: %{name} = %{version}-%{release}
Requires: libsane-hpaio = %{version}-%{release}

%description gui
HPLIP graphical tools.

%package -n hpijs
Summary: HP Printer Drivers
Group: Applications/Publishing
License: BSD
Epoch: %{hpijs_epoch}
Requires: %{name}-libs = %{version}-%{release}
Requires: net-snmp
Requires: cupsddk-drivers

%description -n hpijs
hpijs is a collection of optimized drivers for HP printers.
hpijs supports the DeskJet 350C, 600C, 600C Photo, 630C, Apollo 2000,
Apollo 2100, Apollo 2560, DeskJet 800C, DeskJet 825, DeskJet 900,
PhotoSmart, DeskJet 990C, and PhotoSmart 100 series.

%package -n libsane-hpaio
Summary: SANE driver for scanners in HP's multi-function devices
Group: System Environment/Daemons
License: GPLv2+
Obsoletes: libsane-hpoj <= 0.91
Requires: sane-backends
Requires: %{name}-libs = %{version}-%{release}
ExcludeArch: s390 s390x

%description -n libsane-hpaio
SANE driver for scanners in HP's multi-function devices (from HPOJ).

%prep
rm -rf $RPM_BUILD_DIR/%{name}-%{version}
%setup -q

# Upstream patch to fix paper size order and LJColor device class color space.
%patch1 -p1 -b .hpcups-reorder

# Fix compilation.
%patch2 -p1 -b .strstr-const

# Make utils.checkPyQtImport() look for the gui sub-package (bug #243273).
%patch3 -p1 -b .ui-optional

# Make sure to avoid handwritten asm.
%patch4 -p1 -b .no-asm

# Clear previous state reasons in the hp backend (bug #501338).
%patch5 -p1 -b .clear-previous-state-reasons

# Don't hide state reason changes by missing out newlines in stderr.
%patch6 -p1 -b .state-reasons-newline

# Fixed typos in page sizes (bug #515469).
%patch7 -p1 -b .parenths

# Retry when connecting to device fails (bug #552582).
%patch8 -p1 -b .retry-open

# Set RequiresPageRegion in hpcups PPDs (bug #518756).
%patch9 -p1 -b .requirespageregion

# Fixed hp-setup traceback when discovery page is skipped (bug #523685).
%patch10 -p1 -b .discovery-method

# Give up trying to print a job to a reconnected device (bug #515481).
%patch11 -p1 -b .device-reconnected

# Fixed duplex handling in hpcups.drv (bug #557515).
%patch12 -p1 -b .duplex-vs-number-up

# Set a printer-state-reason when there's a missing required plugin
# (bug #531330).
%patch13 -p1 -b .plugin-error

# Avoid busy loop in hpcups when backend has exited (bug #525944).
%patch14 -p1 -b .hpcups-sigpipe

# Added 'requires proprietary plugin' to appropriate model names
# (bug #513283).
%patch15 -p1 -b .hpcups-plugin

# Fixed Device ID parsing code in hpijs's dj9xxvip.c (bug #510926).
%patch16 -p1 -b .bad-low-ink-warning

# Fixed crash when using Preferences dialog (bug #557099).
%patch17 -p1 -b .preferences-crash

# Explicitly destroy tray icon on exit (bug #576282).
%patch18 -p1 -b .tray-icon-crash

# Mark SNMP quirks in PPD for HP OfficeJet Pro 8500 (bug #580604).
%patch19 -p1 -b .snmp-quirks

sed -i.duplex-constraints \
    -e 's,\(UIConstraints.* \*Duplex\),//\1,' \
    prnt/drv/hpcups.drv.in

%build
%configure \
        --enable-scan-build --enable-gui-build --enable-fax-build \
        --disable-foomatic-rip-hplip-install --enable-pp-build \
        --enable-qt4 --enable-hpcups-install --enable-cups-drv-install \
        --enable-hpijs-install --enable-udev-acl-rules \
        --disable-policykit

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
make install DESTDIR=%{buildroot}

# Remove unpackaged files
rm -rf  %{buildroot}%{_sysconfdir}/sane.d \
        %{buildroot}%{_docdir} \
        %{buildroot}%{_datadir}/hal/fdi \
        %{buildroot}%{_datadir}/hplip/pkservice.py \
        %{buildroot}%{_bindir}/hp-pkservice

rm -f   %{buildroot}%{_bindir}/foomatic-rip \
        %{buildroot}%{_libdir}/cups/filter/foomatic-rip \
        %{buildroot}%{_libdir}/*.la \
        %{buildroot}%{_libdir}/python*/site-packages/*.la \
        %{buildroot}%{_libdir}/libhpip.so \
        %{buildroot}%{_libdir}/sane/*.la \
        %{buildroot}%{_datadir}/cups/model/foomatic-ppds \
        %{buildroot}%{_datadir}/applications/hplip.desktop \
        %{buildroot}%{_datadir}/ppd/HP/*.ppd

mkdir -p %{buildroot}%{_datadir}/applications
sed -i -e '/^Categories=/d' hplip.desktop
desktop-file-install --vendor HP                                \
        --dir %{buildroot}%{_datadir}/applications              \
        --add-category System                                   \
        --add-category Settings                                 \
        --add-category HardwareSettings                         \
        --add-category Application                              \
        hplip.desktop

%{__mkdir_p} %{buildroot}%{_sysconfdir}/sane.d/dll.d
echo hpaio > %{buildroot}%{_sysconfdir}/sane.d/dll.d/hpaio

# Images in docdir should not be executable (bug #440552).
find doc/images -type f -exec chmod 644 {} \;

# Create an empty plugins directory to make sure it gets the right
# SELinux file context (bug #565875).
%{__mkdir_p} %{buildroot}%{_datadir}/hplip/prnt/plugins

# Remove files we don't want to package.
rm -f %{buildroot}%{_datadir}/hplip/hpaio.desc
rm -f %{buildroot}%{_datadir}/hplip/hplip-install
rm -rf %{buildroot}%{_datadir}/hplip/install.*
rm -f %{buildroot}%{_datadir}/hplip/hpijs.drv.in.template

# The systray applet doesn't work properly (displays icon as a
# window), so don't ship the launcher yet.
rm -f %{buildroot}%{_sysconfdir}/xdg/autostart/hplip-systray.desktop

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING doc/*
%{_bindir}/hp-align
%{_bindir}/hp-clean
%{_bindir}/hp-colorcal
%{_bindir}/hp-devicesettings
%{_bindir}/hp-fab
%{_bindir}/hp-faxsetup
%{_bindir}/hp-firmware
%{_bindir}/hp-info
%{_bindir}/hp-levels
%{_bindir}/hp-linefeedcal
%{_bindir}/hp-makecopies
%{_bindir}/hp-makeuri
%{_bindir}/hp-mkuri
%{_bindir}/hp-plugin
%{_bindir}/hp-pqdiag
%{_bindir}/hp-printsettings
%{_bindir}/hp-probe
%{_bindir}/hp-query
%{_bindir}/hp-scan
%{_bindir}/hp-sendfax
%{_bindir}/hp-setup
%{_bindir}/hp-testpage
%{_bindir}/hp-timedate
%{_bindir}/hp-unload
%{_bindir}/hp-wificonfig
# Note: this must be /usr/lib not %{_libdir}, since that's the
# CUPS serverbin directory.
/usr/lib/cups/backend/hp
/usr/lib/cups/backend/hpfax
# Files
%{_datadir}/hplip/align.py*
%{_datadir}/hplip/clean.py*
%{_datadir}/hplip/colorcal.py*
%{_datadir}/hplip/devicesettings.py*
%{_datadir}/hplip/fab.py*
%{_datadir}/hplip/fax
%{_datadir}/hplip/faxsetup.py*
%{_datadir}/hplip/firmware.py*
%{_datadir}/hplip/hpdio.py*
%{_datadir}/hplip/hpssd*
%{_datadir}/hplip/info.py*
%{_datadir}/hplip/__init__.py*
%{_datadir}/hplip/levels.py*
%{_datadir}/hplip/linefeedcal.py*
%{_datadir}/hplip/makecopies.py*
%{_datadir}/hplip/makeuri.py*
%{_datadir}/hplip/plugin.py*
%{_datadir}/hplip/pqdiag.py*
%{_datadir}/hplip/printsettings.py*
%{_datadir}/hplip/probe.py*
%{_datadir}/hplip/query.py*
%{_datadir}/hplip/scan.py*
%{_datadir}/hplip/sendfax.py*
%{_datadir}/hplip/setup.py*
%{_datadir}/hplip/testpage.py*
%{_datadir}/hplip/timedate.py*
%{_datadir}/hplip/unload.py*
%{_datadir}/hplip/wificonfig.py*
# Directories
%dir %{_datadir}/hplip/base
%attr(0644,root,root) %{_datadir}/hplip/base/*
%{_datadir}/hplip/copier
%{_datadir}/hplip/data/ldl
%{_datadir}/hplip/data/localization
%{_datadir}/hplip/data/pcl
%{_datadir}/hplip/data/ps
%{_datadir}/hplip/installer
%{_datadir}/hplip/pcard
%{_datadir}/hplip/prnt
%{_datadir}/hplip/prnt/plugins
%{_datadir}/hplip/scan
%{_localstatedir}/lib/hp

%files common
%defattr(-,root,root,-)
%{_sysconfdir}/udev/rules.d/*
%dir %{_sysconfdir}/hp
%config(noreplace) %{_sysconfdir}/hp/hplip.conf
%dir %{_datadir}/hplip
%dir %{_datadir}/hplip/data
%{_datadir}/hplip/data/models

%files libs
%defattr(-,root,root)
%{_libdir}/libhpip.so.*
%{_libdir}/libhpmud.so*
# Python extension
%{_libdir}/python*/site-packages/*

%files gui
%defattr(-,root,root,-)
%{_bindir}/hp-check
%{_bindir}/hp-print
%{_bindir}/hp-systray
%{_bindir}/hp-toolbox
%{_datadir}/applications/*.desktop
# Files
%{_datadir}/hplip/check.py*
%{_datadir}/hplip/print.py*
%{_datadir}/hplip/systray.py*
%{_datadir}/hplip/toolbox.py*
# Directories
%{_datadir}/hplip/data/images
%{_datadir}/hplip/ui4

%files -n hpijs
%defattr(-,root,root)
%{_bindir}/hpijs
%dir %{_datadir}/ppd/HP
%{_datadir}/ppd/HP/*.ppd.gz
%{_datadir}/cups/drv/*
# Note: this must be /usr/lib not %{_libdir}, since that's the
# CUPS serverbin directory.
/usr/lib/cups/filter/hpcac
/usr/lib/cups/filter/hpcups
/usr/lib/cups/filter/hpcupsfax
/usr/lib/cups/filter/hplipjs

%files -n libsane-hpaio
%defattr(-,root,root)
%{_libdir}/sane/libsane-*.so*
%config(noreplace) %{_sysconfdir}/sane.d/dll.d/hpaio

%pre
# No daemons any more.
/sbin/chkconfig --del hplip 2>/dev/null || true
if [ -x /etc/init.d/hplip ]; then
  /sbin/service hplip stop
fi

%post gui
/usr/bin/update-desktop-database &>/dev/null ||:

%postun gui
/usr/bin/update-desktop-database &>/dev/null ||:

%changelog
* Thu Jun 24 2010 Jiri Popelka <jpopelka@redhat.com> - 3.9.8-33
- Main package requires explicit version of hplip-libs (bug #601783).

* Wed Jun  9 2010 Tim Waugh <twaugh@redhat.com> - 3.9.8-32
- Mark SNMP quirks in PPD for HP OfficeJet Pro 8500 (bug #580604).

* Mon Jun 07 2010 Jiri Popelka <jpopelka@redhat.com> - 3.9.8-31
- hplip-gui requires libsane-hpaio (bug #591636).

* Fri Apr  9 2010 Tim Waugh <twaugh@redhat.com> - 3.9.8-30
- Explicitly destroy tray icon on exit (bug #576282).
- Fixed duplex handling in hpcups.drv (bug #557515).

* Wed Mar  3 2010 Tim Waugh <twaugh@redhat.com> - 3.9.8-29
- Set defattr in gui sub-package file manifest.
- Avoid mixed use of spaces and tabs.

* Thu Feb 25 2010 Jiri Popelka <jpopelka@redhat.com> - 3.9.8-28
- Fixed crash when using Preferences dialog (bug #557099).
- Ship %%{_datadir}/hplip/prnt/plugins directory (bug #565875).

* Thu Jan  7 2010 Tim Waugh <twaugh@redhat.com> - 3.9.8-27
- Do ship pkit module even though the PolicyKit mechanism is not
  shipped (bug #554847).

* Thu Jan  7 2010 Tim Waugh <twaugh@redhat.com> 3.9.8-26
- Rebuilt.

* Thu Jan  7 2010 Tim Waugh <twaugh@redhat.com> 3.9.8-25
- Retry when connecting to device fails (bug #552582).
- Don't ship PolicyKit mechanism (bug #552536).
- Don't run automake/autoconf etc as it causes build failures.
- Reverted fix for bug #533462 until bug #541604 is solved (bug #553220).

* Thu Nov 26 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-24
- Fixed Device ID parsing code in hpijs's dj9xxvip.c (bug #510926).

* Thu Nov 26 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-23
- Removed duplex constraints on page sizes with imageable areas larger
  than possible when duplexing (bug #541572).
- Fixed duplex reverse sides being horizontally flipped (bug #541604).

* Wed Nov 18 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-22
- Fixed duplex handling in hpcups.drv (bug #533462).

* Mon Nov  2 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-21
- Added 'requires proprietary plugin' to appropriate model names
  (bug #513283).

* Fri Oct 30 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-20
- Reverted retry patch until it can be tested some more.

* Thu Oct 29 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-19
- Retry when connecting to device fails (bug #528483).
- Avoid busy loop in hpcups when backend has exited (bug #525944).

* Wed Oct 28 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-18
- Set a printer-state-reason when there's a missing required plugin
  (bug #531330).

* Tue Sep 29 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-17
- Give up trying to print a job to a reconnected device (bug #515481).

* Wed Sep 23 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-16
- Enable parallel port support when configuring (bug #524979).

* Wed Sep 16 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-15
- Fixed hp-setup traceback when discovery page is skipped (bug #523685).

* Fri Aug 28 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-14
- Include missing base files.

* Fri Aug 28 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-13
- Use dll.d file instead of post scriptlet for hpaio (bug #519988).
- Fixed RequiresPageRegion patch (bug #518756).

* Thu Aug 27 2009 Tomas Mraz <tmraz@redhat.com> - 3.9.8-12
- rebuilt with new openssl

* Wed Aug 26 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-11
- Set RequiresPageRegion in hpcups PPDs (bug #518756).

* Tue Aug 25 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-10
- Removed never-used definition of BREAKPOINT in scan/sane/common.h
  in hope of fixing the build.

* Tue Aug 25 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-9
- New common sub-package for udev rules and config file (bug #516459).
- Don't install base/*.py with executable bit set.

* Mon Aug 24 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-8
- Fixed typos in page sizes (bug #515469).
- Build no longer requires libudev-devel.
- Fixed state reasons handling problems (bug #501338).

* Wed Aug 19 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-6
- Make sure to avoid handwritten asm.
- Don't use obsolete configure options.

* Wed Aug 19 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-5
- Use upstream udev rules instead of hal policy (bug #518172).
- Removed unnecessary dependency on PyQt as we only use PyQt4 now.

* Wed Aug 12 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-4
- Upstream patch to fix paper size order and LJColor device class
  color space.

* Wed Aug 12 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-3
- The python-reportlab dependency was in the wrong sub-package.

* Thu Aug  6 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-2
- Removed access_control.grant_group line from HAL fdi file.

* Wed Aug  5 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-1
- 3.9.8.

* Tue Aug  4 2009 Tim Waugh <twaugh@redhat.com> 3.9.6b-5
- Fix hpcups fax PPDs (bug #515356)

* Tue Jul 28 2009 Tim Waugh <twaugh@redhat.com> 3.9.6b-4
- Fixed ui-optional patch for qt4 code path (bug #500473).
- Fixed HWResolution for 'Normal' output from the hpcups driver
  (laundpad bug #405400).

* Mon Jul 27 2009 Tim Waugh <twaugh@redhat.com> 3.9.6b-2
- 3.9.6b.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Tim Waugh <twaugh@redhat.com> 3.9.2-8
- Use existing libusb-using routines to try fetching Device ID.

* Thu Jul 23 2009 Tim Waugh <twaugh@redhat.com> 3.9.2-7
- Error checking in the libudev device-id fallback code.

* Tue Jul 21 2009 Tim Waugh <twaugh@redhat.com> 3.9.2-6
- Fixed device-id reporting.

* Wed Jun 24 2009 Tim Waugh <twaugh@redhat.com> 3.9.2-5
- Set disc media for disc page sizes (bug #495672).

* Mon Mar  9 2009 Tim Waugh <twaugh@redhat.com> 3.9.2-4
- Ship libhpmud.so (bug #489059).
- Fixed no-root-config patch (bug #489055).

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Tim Waugh <twaugh@redhat.com> 3.9.2-2
- 3.9.2.  No longer need systray or quit patches.

* Tue Jan 27 2009 Tim Waugh <twaugh@redhat.com> 2.8.12-7
- Only ship compressed PPD files.

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> 2.8.12-6
- rebuild with new openssl

* Tue Jan 13 2009 Tim Waugh <twaugh@redhat.com> 2.8.12-5
- Fixed Quit menu item in device manager (bug #479751).

* Tue Jan 13 2009 Tim Waugh <twaugh@redhat.com> 2.8.12-4
- Prevent crash when DEVICE_URI/PRINTER environment variables are not
  set (bug #479808 comment 6).

* Tue Jan 13 2009 Tim Waugh <twaugh@redhat.com> 2.8.12-3
- Make --qt4 the default for the systray applet, so that it appears
  in the right place, again (bug #479751).
- Removed hal preprobe rules as they were causing breakage
  (bug #479648).

* Mon Jan 12 2009 Tim Waugh <twaugh@redhat.com> 2.8.12-2
- Don't write to system-wide configuration file (bug #479178).

* Tue Dec 23 2008 Tim Waugh <twaugh@redhat.com> 2.8.12-1
- 2.8.12.

* Thu Dec 11 2008 Tim Waugh <twaugh@redhat.com> 2.8.10-2
- Rediff libsane patch.

* Thu Dec 11 2008 Tim Waugh <twaugh@redhat.com> 2.8.10-1
- 2.8.10.  No longer need gzip-n or quiet patches.

* Thu Dec 11 2008 Tim Waugh <twaugh@redhat.com> 2.8.7-5
- Prevent backend crash when D-Bus not running (bug #474362).

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.8.7-4
- Rebuild for Python 2.6

* Tue Oct 21 2008 Tim Waugh <twaugh@redhat.com> 2.8.7-3
- Ship PPDs in the correct location (bug #343841).

* Fri Sep 26 2008 Tim Waugh <twaugh@redhat.com> 2.8.7-2
- Moved Python extension into libs sub-package (bug #461236).

* Mon Aug  4 2008 Tim Waugh <twaugh@redhat.com> 2.8.7-1
- 2.8.7.
- Avoid hard-coded rpaths.
- New libs sub-package (bug #444016).

* Thu Jul 31 2008 Tim Waugh <twaugh@redhat.com>
- Move libhpip.so* to the main package to avoid libsane-hpaio
  depending on hpijs (bug #457440).

* Thu Jul 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.8.6b-2
- fix license tag

* Mon Jul 28 2008 Tim Waugh <twaugh@redhat.com> 2.8.6b-1
- 2.8.6b.

* Mon Jun 23 2008 Tim Waugh <twaugh@redhat.com> 2.8.6-1
- 2.8.6.  No longer need libm patch.

* Fri Jun  6 2008 Tim Waugh <twaugh@redhat.com> 2.8.5-2
- Make --qt4 the default for the systray applet, so that it appears
  in the right place.  Requires PyQt4.

* Tue Jun  3 2008 Tim Waugh <twaugh@redhat.com> 2.8.5-1
- 2.8.5.
- Configure with --enable-dbus.  Build requires dbus-devel.
- Fix chmod 644 line.
- Ship hp-systray in the gui sub-package, but don't ship the desktop
  launcher yet as the systray applet is quite broken.
- Don't run autoconf.

* Tue May 13 2008 Tim Waugh <twaugh@redhat.com> 2.8.2-3
- Move installer directory to main package (bug #446171).

* Fri Apr  4 2008 Tim Waugh <twaugh@redhat.com> 2.8.2-2
- Update hplip.fdi for Fedora 9: info.bus -> info.subsystem.
- Images in docdir should not be executable (bug #440552).

* Tue Mar  4 2008 Tim Waugh <twaugh@redhat.com> 2.8.2-1
- 2.8.2.  No longer need alloc, unload-traceback or media-empty patches.
- Ship cupsddk driver.  The hpijs sub-package now requires cupsddk-drivers.

* Tue Mar  4 2008 Tim Waugh <twaugh@redhat.com> 2.7.12-6
- Fixed marker-supply-low strings.

* Wed Feb 13 2008 Tim Waugh <twaugh@redhat.com> 2.7.12-5
- Rebuild for GCC 4.3.

* Fri Jan 25 2008 Tim Waugh <twaugh@redhat.com> 2.7.12-4
- The hpijs compression module doesn't allocate enough memory (bug #428536).

* Wed Jan 23 2008 Tim Waugh <twaugh@redhat.com> 2.7.12-3
- Really grant the ACL for the lp group (bug #424331).

* Fri Jan 18 2008 Tim Waugh <twaugh@redhat.com> 2.7.12-2
- Ship installer directory (bug #428246).
- Avoid multilib conflict (bug #341531).
- The hpijs sub-package requires net-snmp (bug #376641).

* Fri Jan 18 2008 Tim Waugh <twaugh@redhat.com> 2.7.12-1
- 2.7.12.  No longer need ljdot4 patch.

* Fri Jan  4 2008 Tim Waugh <twaugh@redhat.com> 2.7.10-2
- Don't ship udev rules; instead, grant an ACL for group lp (bug #424331).

* Fri Dec 07 2007 Release Engineering <rel-eng at fedoraproject dot org> - 2.7.10-2
- Rebuild for deps

* Mon Oct 22 2007 Tim Waugh <twaugh@redhat.com> 2.7.10-1
- 2.7.10.

* Fri Oct 12 2007 Tim Waugh <twaugh@redhat.com> 2.7.9-3
- Applied patch to fix remnants of CVE-2007-5208 (bug #329111).

* Tue Oct  9 2007 Tim Waugh <twaugh@redhat.com> 2.7.9-2
- Use raw instead of 1284.4 communication for LJ4000 series (bug #249191).
- Build requires openssl-devel.

* Wed Oct  3 2007 Tim Waugh <twaugh@redhat.com> 2.7.9-1
- 2.7.9.
- Adjusted udev rules to be less permissive.  We use ConsoleKit to add
  ACLs to the device nodes, so world-writable device nodes can be avoided.

* Tue Sep 25 2007 Tim Waugh <twaugh@redhat.com> 2.7.7-5
- Prevent hpfax trying to load configuration files as user lp.

* Thu Sep  6 2007 Tim Waugh <twaugh@redhat.com> 2.7.7-4
- Reverted udev rules change.
- Ship a HAL FDI file to get correct access control on the USB device
  nodes (bug #251470).
- Make libsane-hpaio requires the main hplip package, needed for
  libhpip.so (bug #280281).

* Thu Aug 30 2007 Tim Waugh <twaugh@redhat.com> 2.7.7-3
- Updated udev rules to allow scanning by console user.

* Wed Aug 29 2007 Tim Waugh <twaugh@redhat.com> 2.7.7-2
- Better buildroot tag.
- More specific license tag.

* Fri Aug  3 2007 Tim Waugh <twaugh@redhat.com> 2.7.7-1
- 2.7.7.

* Mon Jul 23 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-10
- Move libhpmud to hpijs package (bug #248978).

* Fri Jul 20 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-9
- Remove hplip service on upgrade.
- Updated selinux-policy conflict for bug #249014.
- Fixed the udev rules file (bug #248740, bug #249025).

* Tue Jul 17 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-8
- Fixed hp-toolbox desktop file (bug #248560).

* Mon Jul 16 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-7
- Low ink is a warning condition, not an error.

* Wed Jul 11 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-6
- Add hp-check back, but in the gui sub-package.
- Show the HP Toolbox menu entry again.

* Mon Jul  9 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-5
- Read system config when run as root (bug #242974).

* Mon Jul  9 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-4
- Moved reportlab requirement to gui sub-package (bug #189030).
- Patchlevel 1.

* Sat Jul  7 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-3
- Fixed pre scriptlet (bug #247349, bug #247322).

* Fri Jul  6 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-2
- Main package requires python-reportlab for hp-sendfax (bug #189030).
- Explicitly enable scanning.
- Main package requires python-imaging for hp-scan (bug #247210).

* Mon Jul  2 2007 Tim Waugh <twaugh@redhat.com>
- Updated selinux-policy conflict for bug #246257.

* Fri Jun 29 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-1
- 2.7.6.

* Thu Jun 28 2007 Tim Waugh <twaugh@redhat.com> 1.7.4a-3
- Another go at avoiding AVC messages on boot (bug #244205).

* Thu Jun 14 2007 Tim Waugh <twaugh@redhat.com> 1.7.4a-2
- Don't try to write a /root/.hplip.conf file when running as a CUPS
  backend (bug #244205).

* Wed Jun 13 2007 Tim Waugh <twaugh@redhat.com> 1.7.4a-1
- Don't put the version in the desktop file; let desktop-file-install do it.
- 1.7.4a.  No longer need marker-supply or faxing-with-low-supplies
  patches.  Cheetah and cherrypy directories no longer shipped in source
  tarball.

* Mon Jun 11 2007 Tim Waugh <twaugh@redhat.com>
- Don't ship hp-check (bug #243273).
- Moved hp-setup back to the base package, and put code in
  utils.checkPyQtImport() to check for the gui sub-package as well as
  PyQt (bug #243273).

* Fri Jun  8 2007 Tim Waugh <twaugh@redhat.com>
- Moved hp-setup to the ui package (bug #243273).
- Prevent SELinux audit message from the CUPS backends (bug #241776)

* Thu May 10 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-10
- Prevent a traceback when unloading a photo card (bug #238617).

* Fri May  4 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-9
- When faxing, low ink/paper is not a problem (bug #238664).

* Tue Apr 17 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-8
- Update desktop database on %%postun as well (bug #236163).

* Mon Apr 16 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-7
- Some parts can run without GUI support after all (bug #236161).
- Added /sbin/service and /sbin/chkconfig requirements for the scriptlets
  (bug #236445).
- Fixed %%post scriptlet's condrestart logic (bug #236445).

* Fri Apr 13 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-6
- Fixed dangling symlinks (bug #236156).
- Move all fax bits to the gui package (bug #236161).
- Don't ship fax PPD and backend twice (bug #236092).
- Run update-desktop-database in the gui package's %%post scriptlet
  (bug #236163).
- Moved desktop-file-utils requirement to gui package (bug #236163).
- Bumped selinux-policy conflict version (bug #236092).

* Thu Apr  5 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-5
- Better media-empty-error state handling: always set the state.

* Wed Apr  4 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-4
- Clear the media-empty-error printer state.

* Wed Apr  4 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-3
- Fixed typo in marker-supply-low patch.

* Wed Apr  4 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-2
- Split out a gui sub-package (bug #193661).
- Build requires sane-backends-devel (bug #234813).

* Tue Apr  3 2007 Tim Waugh <twaugh@redhat.com>
- Change 'Hidden' to 'NoDisplay' in the desktop file, and use the System
  category instead of Utility (bug #170762).
- Link libsane-hpaio against libsane (bug #234813).

* Fri Mar 30 2007 Tim Waugh <twaugh@redhat.com>
- Use marker-supply-low IPP message.

* Wed Mar  1 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-1
- 1.7.2.

* Wed Feb 14 2007 Tim Waugh <twaugh@redhat.com> 1.7.1-1
- 1.7.1.

* Wed Jan 10 2007 Tim Waugh <twaugh@redhat.com> 1.6.12-1
- 1.6.12.  No longer need broken-conf, loop, out-of-paper or
  sane-debug patches.

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.6.10-7
- rebuild against python 2.5

* Wed Dec  6 2006 Tim Waugh <twaugh@redhat.com>
- Minor state fixes for out-of-paper patch.

* Thu Nov 23 2006 Tim Waugh <twaugh@redhat.com> 1.6.10-6
- Report out-of-paper and offline conditions in CUPS backend (bug #216477).

* Wed Nov  1 2006 Tim Waugh <twaugh@redhat.com> 1.6.10-5
- Fixed debugging patch.

* Wed Nov  1 2006 Tim Waugh <twaugh@redhat.com> 1.6.10-4
- Allow debugging of the SANE backend.

* Mon Oct 30 2006 Tim Waugh <twaugh@redhat.com> 1.6.10-3
- IPv6 support (bug #198377).  Local-only sockets are IPv4, and ought
  to be changed to unix domain sockets in future.

* Fri Oct 27 2006 Tim Waugh <twaugh@redhat.com> 1.6.10-2
- 1.6.10.  No longer need compile patch.
- Fixed default config file (bug #211072).
- Moved libhpip to hpijs sub-package (bug #212531).

* Fri Sep 29 2006 Tim Waugh <twaugh@redhat.com> 1.6.7-4
- Don't wake up every half a second (bug #204725).

* Mon Sep 25 2006 Tim Waugh <twaugh@redhat.com>
- Fixed package URL.

* Mon Aug 21 2006 Tim Waugh <twaugh@redhat.com> 1.6.7-3
- Don't look up username in PWDB in the fax backend (removed redundant code).

* Mon Aug  7 2006 Tim Waugh <twaugh@redhat.com> 1.6.7-2
- 1.6.7.
- Conflict with selinux-policy < 2.3.4 to make sure new port numbers are
  known about (bug #201357).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - (none):1.6.6a-3.1
- rebuild

* Tue Jul  4 2006 Tim Waugh <twaugh@redhat.com> 1.6.6a-3
- libhpip should link against libm (bug #197599).

* Wed Jun 28 2006 Tim Waugh <twaugh@redhat.com> 1.6.6a-2
- 1.6.6a.

* Mon Jun 26 2006 Tim Waugh <twaugh@redhat.com>
- Patchlevel 1.
- Fixed libsane-hpaio %%post scriptlet (bug #196663).

* Fri Jun 16 2006 Tim Waugh <twaugh@redhat.com> 1.6.6-2
- 1.6.6.

* Mon Jun 12 2006 Tim Waugh <twaugh@redhat.com> 0.9.11-6
- Build requires autoconf (bug #194682).

* Fri May 26 2006 Tim Waugh <twaugh@redhat.com> 0.9.11-5
- Include doc files (bug #192790).

* Mon May 15 2006 Tim Waugh <twaugh@redhat.com> 0.9.11-4
- Patchlevel 2.

* Wed May 10 2006 Tim Waugh <twaugh@redhat.com> 0.9.11-3
- Move hpijs to 0.9.11 too.

* Wed May 10 2006 Tim Waugh <twaugh@redhat.com> 0.9.11-2
- 0.9.11.
- Keep hpijs at 0.9.8 for now.

* Fri Apr 21 2006 Tim Waugh <twaugh@redhat.com> 0.9.10-6
- Patchlevel 2.

* Wed Apr 19 2006 Tim Waugh <twaugh@redhat.com>
- Don't package COPYING twice (bug #189162).

* Tue Apr 18 2006 Tim Waugh <twaugh@redhat.com> 0.9.10-5
- Patchlevel 1.
- Fixed another case-sensitive match.
- Require hpijs sub-package (bug #189140).
- Don't package unneeded files (bug #189162).
- Put fax PPD in the right place (bug #186213).

* Tue Apr  4 2006 Tim Waugh <twaugh@redhat.com> 0.9.10-4
- Use case-insensitive matching.  0.9.8 gave all-uppercase in some
  situations.
- Last known working hpijs comes from 0.9.8, so use that.

* Tue Mar 28 2006 Tim Waugh <twaugh@redhat.com> 0.9.10-3
- Always use /usr/lib/cups/backend.

* Tue Mar 28 2006 Tim Waugh <twaugh@redhat.com> 0.9.10-2
- 0.9.10.
- Ship PPDs.

* Fri Mar 24 2006 Tim Waugh <twaugh@redhat.com> 0.9.9-7
- Include hpfax.
- Build requires libusb-devel.

* Thu Mar 23 2006 Tim Waugh <twaugh@redhat.com> 0.9.9-6
- CUPS backend directory is always in /usr/lib.

* Mon Mar 13 2006 Tim Waugh <twaugh@redhat.com> 0.9.9-4
- Quieten hpssd on startup.

* Sat Mar 11 2006 Tim Waugh <twaugh@redhat.com> 0.9.9-3
- Patchlevel 1.

* Thu Mar  9 2006 Tim Waugh <twaugh@redhat.com> 0.9.9-2
- 0.9.9.  No longer need quiet or 0.9.8-4 patches.

* Wed Mar 01 2006 Karsten Hopp <karsten@redhat.de> 0.9.8-6
- Buildrequires: desktop-file-utils

* Mon Feb 27 2006 Tim Waugh <twaugh@redhat.com> 0.9.8-5
- Patchlevel 4.

* Tue Feb 14 2006 Tim Waugh <twaugh@redhat.com> 0.9.8-4
- Added Obsoletes: hpoj tags back in (bug #181476).

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - (none):0.9.8-3.1
- bump again for double-long bug on ppc(64)

* Tue Feb  7 2006 Tim Waugh <twaugh@redhat.com> 0.9.8-3
- Patchlevel 3.

* Fri Feb  3 2006 Tim Waugh <twaugh@redhat.com> 0.9.8-2
- Patchlevel 2.

* Thu Feb  2 2006 Tim Waugh <twaugh@redhat.com> 0.9.8-1
- 0.9.8.
- No longer need initscript patch.
- Don't package hpfax yet.

* Wed Jan 18 2006 Tim Waugh <twaugh@redhat.com> 0.9.7-8
- Don't package PPD files.

* Thu Jan  5 2006 Tim Waugh <twaugh@redhat.com> 0.9.7-7
- Fix initscript (bug #176966).

* Mon Jan  2 2006 Tim Waugh <twaugh@redhat.com> 0.9.7-6
- Rebuild.

* Fri Dec 23 2005 Tim Waugh <twaugh@redhat.com> 0.9.7-5
- Rebuild.

* Wed Dec 21 2005 Tim Waugh <twaugh@redhat.com> 0.9.7-4
- Build requires python-devel, libjpeg-devel (bug #176317).

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Dec  7 2005 Tim Waugh <twaugh@redhat.com> 0.9.7-3
- Use upstream patch 0.9.7-2.
- No longer need lpgetstatus or compile patches.

* Fri Nov 25 2005 Tim Waugh <twaugh@redhat.com> 0.9.7-2
- Prevent LPGETSTATUS overrunning format buffer.

* Thu Nov 24 2005 Tim Waugh <twaugh@redhat.com> 0.9.7-1
- 0.9.7.

* Fri Nov 18 2005 Tim Waugh <twaugh@redhat.com> 0.9.6-7
- Fix compilation.

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> 0.9.6-6
- rebuilt against new openssl

* Mon Nov  7 2005 Tim Waugh <twaugh@redhat.com> 0.9.6-5
- Rebuilt.

* Wed Oct 26 2005 Tim Waugh <twaugh@redhat.com> 0.9.6-4
- Ship initscript in %%{_sysconfdir}/rc.d/init.d.

* Fri Oct 14 2005 Tim Waugh <twaugh@redhat.com>
- Install the desktop file with Hidden=True (bug #170762).

* Fri Oct 14 2005 Tim Waugh <twaugh@redhat.com> 0.9.6-3
- Don't install desktop file (bug #170762).
- Quieten the hpssd daemon at startup (bug #170762).

* Wed Oct 12 2005 Tim Waugh <twaugh@redhat.com> 0.9.6-2
- 0.9.6.

* Tue Sep 20 2005 Tim Waugh <twaugh@redhat.com> 0.9.5-3
- Apply upstream patch to fix scanning in LaserJets and parallel InkJets.

* Mon Sep 19 2005 Tim Waugh <twaugh@redhat.com> 0.9.5-2
- 0.9.5.
- No longer need condrestart patch.
- Fix compile errors.

* Tue Jul 26 2005 Tim Waugh <twaugh@redhat.com> 0.9.4-3
- Fix condrestart in the initscript.

* Mon Jul 25 2005 Tim Waugh <twaugh@redhat.com> 0.9.4-2
- Use 'condrestart' not 'restart' in %%post scriptlet.

* Fri Jul 22 2005 Tim Waugh <twaugh@redhat.com> 0.9.4-1
- forward-decl patch not needed.
- 0.9.4.

* Fri Jul  1 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-8
- Removed Obsoletes: hpoj tags (bug #162222).

* Thu Jun 30 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-7
- Rebuild to get Python modules precompiled.

* Wed Jun 22 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-6
- For libsane-hpaio ExcludeArch: s390 s390x, because it requires
  sane-backends.

* Wed Jun 15 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-5
- Use static IP ports (for SELinux policy).

* Tue Jun 14 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-4
- Conflicts: hpijs from before this package provided it.
- Conflicts: system-config-printer < 0.6.132 (i.e. before HPLIP support
  was added)

* Thu Jun  9 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-3
- Added Obsoletes: for xojpanel and hpoj-devel (but we don't actually package
  devel files yet).

* Thu Jun  9 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-2
- Add 'hpaio' to SANE config file, not 'hpoj' (bug #159954).

* Thu Jun  9 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-1
- Use /usr/share/applications for putting desktop files in (bug #159932).
- Requires PyQt (bug #159932).

* Tue Jun  7 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-0.1
- Initial package, based on Mandriva spec file.
