%define lib_major 0
%define libname %mklibname %{name} %{lib_major}
%define libnamedev %mklibname -d %{name}

Summary: Keyring and password manager for the GNOME desktop
Name: gnome-keyring
Version: 2.28.2
Release: %mkrel 1
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/gnome-keyring/%{name}-%{version}.tar.bz2
Patch0: gnome-keyring-2.27.92-fix-linking.patch
URL: http://www.gnome.org/
License: GPLv2+ and LGPLv2+
Group: Networking/Remote access
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: gtk2-devel >= 2.4.0
BuildRequires: libGConf2-devel
BuildRequires: libgcrypt-devel
BuildRequires: libtasn1-devel
BuildRequires: dbus-glib-devel
BuildRequires: pam-devel
BuildRequires: libtasn1-tools
BuildRequires: intltool
BuildRequires: gtk-doc
BuildRequires: libtool

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
Provides: lib%{name}-devel = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Obsoletes: %mklibname -d %name 0

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
%patch0 -p1 -b .fix-linking

#needed by patch0
autoreconf -fi

%build
%configure2_5x --with-pam-dir=/%_lib/security --disable-static \
  --disable-schemas-install --disable-acl-prompts
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

%post
%post_install_gconf_schemas %name
%preun
%preun_uninstall_gconf_schemas %name


%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc README NEWS TODO COPYING
%_sysconfdir/xdg/autostart/gnome-keyring-daemon.desktop
%_sysconfdir/gconf/schemas/%name.schemas
%{_bindir}/gnome-keyring
%{_bindir}/gnome-keyring-daemon
%_libexecdir/gnome-keyring-ask
%_libdir/gnome-keyring/
/%_lib/security/pam_gnome_keyring*.so
%_datadir/dbus-1/services/org.gnome.keyring.service
%_datadir/gcr

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libgnome-keyring.so.%{lib_major}*
%{_libdir}/libgp11.so.%{lib_major}*
%{_libdir}/libgcr.so.%{lib_major}*

%files -n %{libnamedev}
%defattr(-,root,root)
%doc COPYING.LIB ChangeLog
%{_libdir}/libgnome-keyring.so
%{_libdir}/libgp11.so
%{_libdir}/libgcr.so
%attr(644,root,root) %{_libdir}/*.la
%dir %{_includedir}/gnome-keyring-1/
%{_includedir}/gnome-keyring-1/*.h
%{_includedir}/gp11/
%{_includedir}/gcr
%{_libdir}/pkgconfig/gnome-keyring-1.pc
%{_libdir}/pkgconfig/gp11-0.pc
%{_libdir}/pkgconfig/gcr-0.pc
%_datadir/gtk-doc/html/*
