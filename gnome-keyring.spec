%define url_ver	%(echo %{version}|cut -d. -f1,2)

%define api	3

Summary:	Keyring and password manager for the GNOME desktop
Name:		gnome-keyring
Version:	3.6.3
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		Networking/Remote access
URL:		http://www.gnome.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:	glib2.0-common
BuildRequires:	gtk-doc
BuildRequires:	libtasn1-tools
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(dbus-1) >= 1.0
BuildRequires:	pkgconfig(gck-1) >= 3.3.4
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0
BuildRequires:	pkgconfig(libtasn1)

#gw for keyring management GUI
Suggests:	seahorse

%description
gnome-keyring is a program that keep password and other secrets for
users. It is run as a damon in the session, similar to ssh-agent, and
other applications can locate it by an environment variable.
 
The program can manage several keyrings, each with its own master
password, and there is also a session keyring which is never stored to
disk, but forgotten when the session ends.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--with-pam-dir=/%{_lib}/security \
	--disable-static \
	--enable-pam \
	--disable-schemas-compile

%make LIBS='-lgmodule-2.0 -lglib-2.0'

%install
%makeinstall_std

#we don't want these
find %{buildroot} -name "*.la" -exec rm -rf {} \;

%find_lang %{name} %{name}.lang

%files -f %{name}.lang
%doc README NEWS
%{_sysconfdir}/xdg/autostart/%{name}-gpg.desktop
%{_sysconfdir}/xdg/autostart/%{name}-pkcs11.desktop
%{_sysconfdir}/xdg/autostart/%{name}-secrets.desktop
%{_sysconfdir}/xdg/autostart/%{name}-ssh.desktop
%{_sysconfdir}/pkcs11/modules/%{name}.module
%{_bindir}/%{name}
%{_bindir}/%{name}-%{api}
%attr(755,root,root) %{_bindir}/%{name}-daemon
%{_libdir}/%{name}
%{_libdir}/pkcs11
/%{_lib}/security/pam_gnome_keyring*.so
%{_datadir}/dbus-1/services/org.gnome.keyring.service
%{_datadir}/dbus-1/services/org.freedesktop.secrets.service
%{_datadir}/GConf/gsettings/*.convert
%{_datadir}/glib-2.0/schemas/*.gschema.xml



%changelog
* Fri Sep 28 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.0-1
- update to 3.6.0

* Wed May 02 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.4.1-1
+ Revision: 794901
- p0 applied upstream
- new version 3.4.1
- adapted spec for split out gcr pkg

* Sun Mar 25 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 3.2.2-3
+ Revision: 786696
- patch0: fix WARNING: gnome-keyring:: no socket to connect to - patch from debian

* Wed Feb 15 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.2.2-2
+ Revision: 774406
- added fix for glib-2.0 build error
- added missing BR
- added fix for gmodule-2.0 build error
- rebuild for ffi5

* Thu Nov 17 2011 Matthew Dawkins <mattydaw@mandriva.org> 3.2.2-1
+ Revision: 731371
- new version 3.2.2
  dropped old patches
  sync'd spec with mga for major pkg changes before 3.3.x
  cleaned up spec

* Thu May 26 2011 GÃ¶tz Waschk <waschk@mandriva.org> 3.0.3-1
+ Revision: 679200
- new version

  + Nicolas LÃ©cureuil <nlecureuil@mandriva.com>
    - Clean spec file for rpm5

* Fri May 20 2011 Funda Wang <fwang@mandriva.org> 3.0.2-1
+ Revision: 676283
- new version 3.0.2

* Tue Apr 26 2011 Funda Wang <fwang@mandriva.org> 3.0.1-1
+ Revision: 659204
- disable test
- build with gtk2
- update to new version 3.0.1

* Fri Apr 08 2011 Funda Wang <fwang@mandriva.org> 3.0.0-1
+ Revision: 651946
- new version 3.0.0

* Tue Oct 26 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.32.1-1mdv2011.0
+ Revision: 589431
- update to new version 2.32.1

* Tue Sep 28 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.32.0-1mdv2011.0
+ Revision: 581610
- update to new version 2.32.0

* Mon Sep 13 2010 Funda Wang <fwang@mandriva.org> 2.31.92-3mdv2011.0
+ Revision: 577877
- tans1-tools is only a buildtime dep

* Mon Sep 13 2010 Funda Wang <fwang@mandriva.org> 2.31.92-2mdv2011.0
+ Revision: 577873
- simplify BRs
- add requires on libtasn1-tools

* Mon Sep 13 2010 Funda Wang <fwang@mandriva.org> 2.31.92-1mdv2011.0
+ Revision: 577852
- patch0 and patch4 merged upstream
- new version 2.31.92

* Wed Sep 01 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.31.91-2mdv2011.0
+ Revision: 575045
- fix ssh key unlocking

* Tue Aug 31 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.31.91-1mdv2011.0
+ Revision: 574621
- new version
- drop patch 0
- fix build
- update file list

* Fri Jul 30 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.31.4-1mdv2011.0
+ Revision: 563400
- new version
- update file list

* Wed Jul 21 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.30.3-2mdv2011.0
+ Revision: 556309
- suggest seahorse for key management (bug #60198)

* Sun Jul 11 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.30.3-1mdv2011.0
+ Revision: 550876
- new version
- drop patch 4

* Mon May 03 2010 Frederic Crozat <fcrozat@mandriva.com> 2.30.1-3mdv2010.1
+ Revision: 541735
- Patch4 (GIT): add missing service file (GNOME bug #611002)

* Wed Apr 28 2010 Christophe Fergeau <cfergeau@mandriva.com> 2.30.1-2mdv2010.1
+ Revision: 540342
- rebuild so that shared libraries are properly stripped again

* Mon Apr 26 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.30.1-1mdv2010.1
+ Revision: 539333
- update to new version 2.30.1

* Tue Mar 30 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.30.0-1mdv2010.1
+ Revision: 529758
- update to new version 2.30.0

* Wed Mar 10 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.29.92-1mdv2010.1
+ Revision: 517379
- update to new version 2.29.92

* Tue Feb 09 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.29.90-1mdv2010.1
+ Revision: 502597
- update to new version 2.29.90

* Mon Jan 11 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.29.5-1mdv2010.1
+ Revision: 489815
- update to new version 2.29.5

* Wed Dec 23 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.29.4-2mdv2010.1
+ Revision: 481853
- add Fedora patches to make the keyring exit on session end

* Mon Dec 21 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.29.4-1mdv2010.1
+ Revision: 480982
- new version
- update build deps
- update file list
- conflict with old library packages

* Mon Dec 14 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.28.2-1mdv2010.1
+ Revision: 478590
- new version
- regenerate libtool

* Fri Nov 06 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.28.1-1mdv2010.1
+ Revision: 460930
- new version
- drop patch

* Mon Oct 05 2009 Frederic Crozat <fcrozat@mandriva.com> 2.28.0-3mdv2010.0
+ Revision: 454049
- Patch1 (vuntz): fix 10s timeout at logout (GNOME bug #595698)

* Wed Sep 30 2009 Frederic Crozat <fcrozat@mandriva.com> 2.28.0-2mdv2010.0
+ Revision: 451795
- Disable ACL prompts, they are more confusing than anything

* Mon Sep 21 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.28.0-1mdv2010.0
+ Revision: 446733
- update to new version 2.28.0
- update build deps

* Mon Sep 14 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.27.92-1mdv2010.0
+ Revision: 439071
- new version
- fix linking

* Mon Aug 10 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.27.90-1mdv2010.0
+ Revision: 414391
- update to new version 2.27.90

* Mon Jul 27 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.27.5-1mdv2010.0
+ Revision: 400788
- update to new version 2.27.5

* Mon Jul 13 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.27.4-1mdv2010.0
+ Revision: 395678
- update to new version 2.27.4

* Mon Jun 29 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.26.3-1mdv2010.0
+ Revision: 390726
- update to new version 2.26.3

* Tue Apr 14 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.26.1-1mdv2009.1
+ Revision: 366983
- new version
- drop patch

* Thu Apr 02 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.26.0-2mdv2009.1
+ Revision: 363504
- fix hanging ssh-agent (upstream bug #575247)
- remove all build workarounds
- spec fixes

* Sat Mar 14 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.26.0-1mdv2009.1
+ Revision: 355139
- new version
- update build deps

* Mon Mar 02 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.92-1mdv2009.1
+ Revision: 347290
- update to new version 2.25.92

* Sat Feb 14 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.91-1mdv2009.1
+ Revision: 340324
- update to new version 2.25.91

* Mon Feb 02 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.90-1mdv2009.1
+ Revision: 336659
- new version
- drop patch
- update file list

  + Funda Wang <fwang@mandriva.org>
    - drop static lib
    - use system libtool
    - Partial fix linkage

* Tue Jan 20 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.5-1mdv2009.1
+ Revision: 331621
- new version
- disable --no-undefined
- update file list

* Fri Jan 09 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.4.2-1mdv2009.1
+ Revision: 327381
- update to new version 2.25.4.2

* Tue Jan 06 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.4.1-1mdv2009.1
+ Revision: 325242
- update to new version 2.25.4.1

* Mon Jan 05 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.4-1mdv2009.1
+ Revision: 324946
- update to new version 2.25.4

* Thu Dec 18 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.2-1mdv2009.1
+ Revision: 315883
- new version
- update file list

* Tue Nov 04 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.1-1mdv2009.1
+ Revision: 299938
- update to new version 2.25.1

* Sun Oct 19 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.24.1-1mdv2009.1
+ Revision: 295218
- update to new version 2.24.1

* Sun Sep 21 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.24.0-1mdv2009.0
+ Revision: 286289
- fix build deps
- new version

* Mon Sep 08 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.92-1mdv2009.0
+ Revision: 282460
- new version

* Wed Sep 03 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.91-1mdv2009.0
+ Revision: 279783
- new version
- drop patch

* Tue Aug 19 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.90-1mdv2009.0
+ Revision: 273785
- fix build deps
- new version
- fix build
- update file list

* Mon Aug 04 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.6-1mdv2009.0
+ Revision: 262939
- new version

* Tue Jul 22 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.5-1mdv2009.0
+ Revision: 240069
- new version
- update file list

* Mon Jun 30 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.22.3-1mdv2009.0
+ Revision: 230367
- new version
- update license

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue May 27 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.22.2-1mdv2009.0
+ Revision: 211558
- new version

* Wed Apr 09 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.22.1-1mdv2009.0
+ Revision: 192453
- new version
- drop patch

* Wed Apr 02 2008 Frederic Crozat <fcrozat@mandriva.com> 2.22.0-2mdv2008.1
+ Revision: 191700
- Patch0 (SVN): fix daemon startup through dbus (GNOME bug #522253)

* Sun Mar 09 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.22.0-1mdv2008.1
+ Revision: 183037
- new version

* Mon Feb 25 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.92-1mdv2008.1
+ Revision: 174579
- new version

* Tue Feb 12 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.91-1mdv2008.1
+ Revision: 165742
- new version

* Mon Jan 28 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.90-1mdv2008.1
+ Revision: 159441
- new version

* Fri Jan 18 2008 Frederic Crozat <fcrozat@mandriva.com> 2.21.5-2mdv2008.1
+ Revision: 154728
- Fix the way pam module is installed and don't install .la file for it

* Mon Jan 14 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.5-1mdv2008.1
+ Revision: 151325
- new version
- add gconf schema

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Mon Dec 17 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.4-1mdv2008.1
+ Revision: 130172
- new version
- update file list

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Dec 05 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.3.2-1mdv2008.1
+ Revision: 115659
- new version

* Wed Dec 05 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.3.1-1mdv2008.1
+ Revision: 115621
- new version
- update file list

* Mon Dec 03 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.3-1mdv2008.1
+ Revision: 114601
- new version
- drop patch
- update buildrequires
- update file list

* Mon Dec 03 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.20.2-2mdv2008.1
+ Revision: 114531
- fix environment in the pam module

* Sun Nov 25 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.20.2-1mdv2008.1
+ Revision: 111863
- new version

* Mon Oct 15 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.20.1-1mdv2008.1
+ Revision: 98576
- new version
- update file list

* Wed Sep 19 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.20.0-1mdv2008.0
+ Revision: 90415
- new version
- new version

* Sun Aug 26 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.91-1mdv2008.0
+ Revision: 71579
- new version

* Tue Aug 14 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.90-1mdv2008.0
+ Revision: 62967
- new version
- new devel name

* Mon Jul 30 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.6.1-2mdv2008.0
+ Revision: 56619
- fix buildrequires

* Mon Jul 30 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.6.1-1mdv2008.0
+ Revision: 56586
- new version
- fix installation
- new version
- add pam module

* Sat Jul 07 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.5-1mdv2008.0
+ Revision: 49369
- new version

* Mon Jun 18 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.4.1-1mdv2008.0
+ Revision: 40993
- new version

* Sun Jun 17 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.4-1mdv2008.0
+ Revision: 40610
- new version
- update file list

* Wed Jun 06 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.2-2mdv2008.0
+ Revision: 36055
- fix buildrequires
- new version

* Tue Apr 17 2007 GÃ¶tz Waschk <waschk@mandriva.org> 0.8.1-1mdv2008.0
+ Revision: 13824
- new version


* Mon Mar 12 2007 GÃ¶tz Waschk <waschk@mandriva.org> 0.8-1mdv2007.1
+ Revision: 142014
- new version

* Fri Feb 23 2007 GÃ¶tz Waschk <waschk@mandriva.org> 0.7.92-1mdv2007.1
+ Revision: 125183
- new version

* Mon Feb 12 2007 GÃ¶tz Waschk <waschk@mandriva.org> 0.7.91-1mdv2007.1
+ Revision: 120040
- new version

* Fri Jan 05 2007 GÃ¶tz Waschk <waschk@mandriva.org> 0.7.3-2mdv2007.1
+ Revision: 104390
- bot rebuild
- new version

* Mon Dec 18 2006 GÃ¶tz Waschk <waschk@mandriva.org> 0.7.2-1mdv2007.1
+ Revision: 98508
- new version

* Tue Nov 28 2006 GÃ¶tz Waschk <waschk@mandriva.org> 0.7.1-2mdv2007.1
+ Revision: 87929
- spec fix
- new version

* Mon Nov 27 2006 GÃ¶tz Waschk <waschk@mandriva.org> 0.6.0-1mdv2007.1
+ Revision: 87705
- Import gnome-keyring

* Tue Sep 05 2006 GÃ¶tz Waschk <waschk@mandriva.org> 0.6.0-1mdv2007.0
- New release 0.6.0

* Tue Aug 22 2006 Frederic Crozat <fcrozat@mandriva.com> 0.5.2-1mdv2007.0
- Release 0.5.2

* Thu Jun 15 2006 Götz Waschk <waschk@mandriva.org> 0.5.1-2mdv2007.0
- fix buildrequires

* Tue Jun 13 2006 Götz Waschk <waschk@mandriva.org> 0.5.1-1mdv2007.0
- update file list
- New release 0.5.1

* Mon Mar 13 2006 GÃ¶tz Waschk <waschk@mandriva.org> 0.4.9-1mdk
- New release 0.4.9

* Tue Feb 28 2006 GÃ¶tz Waschk <waschk@mandriva.org> 0.4.8-1mdk
- New release 0.4.8

* Mon Feb 13 2006 GÃ¶tz Waschk <waschk@mandriva.org> 0.4.7-1mdk
- New release 0.4.7
- use mkrel

* Wed Nov 16 2005 GÃ¶tz Waschk <waschk@mandriva.org> 0.4.6-1mdk
- New release 0.4.6

* Wed Oct 12 2005 GÃ¶tz Waschk <waschk@mandriva.org> 0.4.5-1mdk
- New release 0.4.5

* Fri Sep 02 2005 GÃ¶tz Waschk <waschk@mandriva.org> 0.4.3-2mdk
- rebuild to remove glitz dep

* Thu Aug 25 2005 GÃ¶tz Waschk <waschk@mandriva.org> 0.4.3-1mdk
- New release 0.4.3

* Mon Mar 07 2005 Götz Waschk <waschk@linux-mandrake.com> 0.4.2-1mdk
- reenable libtoolize
- New release 0.4.2

* Tue Jan 11 2005 Goetz Waschk <waschk@linux-mandrake.com> 0.4.1-1mdk
- New release 0.4.1

* Tue Oct 19 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 0.4.0-1mdk
- New release 0.4.0

* Tue Apr 20 2004 Götz Waschk <waschk@linux-mandrake.com> 0.2.1-1mdk
- new version

* Tue Apr 06 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 0.2.0-1mdk
- initial package (from Götz Waschk)

