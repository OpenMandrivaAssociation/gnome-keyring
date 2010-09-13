%define lib_major 0
%define libname %mklibname gcr %{lib_major}
%define libnamedev %mklibname -d gcr
%define oldlibname %mklibname %name 0
%define olddevname %mklibname -d %name

Summary: Keyring and password manager for the GNOME desktop
Name: gnome-keyring
Version: 2.31.92
Release: %mkrel 1
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/gnome-keyring/%{name}-%{version}.tar.bz2
#gw fix ssh key unlocking
#https://bugzilla.gnome.org/show_bug.cgi?id=627815
Patch0: gnome-keyring-fix-ssh-key-unlock.patch
# Fedora patches that make the daemon exit on logout
# https://bugzilla.gnome.org/show_bug.cgi?id=598494
Patch2: gnome-keyring-2.29.4-die-on-session-exit.patch
Patch3: gnome-keyring-2.28.1-nopass.patch 
#gw revert this
#https://bugzilla.gnome.org/show_bug.cgi?id=628384
Patch4: gnome-keyring-fix-pam-detection-on-apple.patch
URL: http://www.gnome.org/
License: GPLv2+ and LGPLv2+
Group: Networking/Remote access
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: gtk2-devel >= 2.4.0
BuildRequires: libGConf2-devel
BuildRequires: libgcrypt-devel
BuildRequires: libtasn1-devel
BuildRequires: eggdbus-devel
BuildRequires: pam-devel
BuildRequires: libtasn1-tools
BuildRequires: intltool
BuildRequires: gtk-doc
BuildRequires: libtool
#gw for keyring management GUI
Suggests: seahorse

%description
gnome-keyring is a program that keep password and other secrets for
users. It is run as a damon in the session, similar to ssh-agent, and
other applications can locate it by an environment variable.
 
The program can manage several keyrings, each with its own master
password, and there is also a session keyring which is never stored to
disk, but forgotten when the session ends.

%package -n %{libname}
Group: System/Libraries
Summary: Library for integration with the gnome keyring system
Requires: %{name} >= %{version}-%{release}
Conflicts: %oldlibname < 2.29.4

%description -n %{libname}
The library libgnome-keyring is used by applications to integrate with
the gnome keyring system. However, at this point the library hasn't been
tested and used enought to consider the API to be publically
exposed. Therefore use of libgnome-keyring is at the moment limited to
internal use in the gnome desktop. However, we hope that the
gnome-keyring API will turn out useful and good, so that later it
can be made public for any application to use.


%package -n %{libnamedev}
Group: Development/C
Summary: Library for integration with the gnome keyring system
Requires: %{libname} = %{version}
Provides: libgcr-devel = %{version}-%{release}
Conflicts: %olddevname < 2.29.4

%description -n %{libnamedev}
The library libgnome-keyring is used by applications to integrate with
the gnome keyring system. However, at this point the library hasn't been
tested and used enought to consider the API to be publically
exposed. Therefore use of libgnome-keyring is at the moment limited to
internal use in the gnome desktop. However, we hope that the
gnome-keyring API will turn out useful and good, so that later it
can be made public for any application to use.


%prep
%setup -q
%patch2 -p1 -b .die-on-session-exit 
%patch3 -p1 -b .no-pass

%build
%configure2_5x --with-pam-dir=/%_lib/security --disable-static \
  --disable-acl-prompts --enable-pam
#gw for unstable cooker builds use:
#--enable-debug
#--enable-tests
#or even:
#--enable-valgrind
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
rm -f %buildroot/%_lib/security/{*.la,*.a} %buildroot%_libdir/*.a
%find_lang %{name}



%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc README NEWS
%_sysconfdir/xdg/autostart/gnome-keyring-gpg.desktop
%_sysconfdir/xdg/autostart/gnome-keyring-pkcs11.desktop
%_sysconfdir/xdg/autostart/gnome-keyring-secrets.desktop
%_sysconfdir/xdg/autostart/gnome-keyring-ssh.desktop
%{_bindir}/gnome-keyring
%{_bindir}/gnome-keyring-daemon
%_libdir/gnome-keyring/
%_libexecdir/gnome-keyring-prompt
%dir %_datadir/%name
%dir %_datadir/%name/introspect
%_datadir/%name/introspect/*.xml
%dir %_datadir/%name/ui/
%_datadir/%name/ui/*.ui
/%_lib/security/pam_gnome_keyring*.so
%_datadir/dbus-1/services/org.gnome.keyring.service
%_datadir/dbus-1/services/org.freedesktop.secrets.service
%_datadir/gcr
%_datadir/GConf/gsettings/*.convert
%_datadir/glib-2.0/schemas/*.gschema.xml

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libgp11.so.%{lib_major}*
%{_libdir}/libgcr.so.%{lib_major}*

%files -n %{libnamedev}
%defattr(-,root,root)
%doc COPYING.LIB ChangeLog
%{_libdir}/libgp11.so
%{_libdir}/libgcr.so
%attr(644,root,root) %{_libdir}/*.la
%{_includedir}/gp11/
%{_includedir}/gcr
%{_libdir}/pkgconfig/gp11-0.pc
%{_libdir}/pkgconfig/gcr-0.pc
%_datadir/gtk-doc/html/*
