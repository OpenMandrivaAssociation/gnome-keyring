%define lib_major 0
%define lib_name %mklibname %{name} %{lib_major}

Summary: Keyring and password manager for the GNOME desktop
Name: gnome-keyring
Version: 2.19.6.1
Release: %mkrel 2
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/gnome-keyring/%{name}-%{version}.tar.bz2
URL: http://www.gnome.org/
License: GPL/LGPL
Group: Networking/Remote access
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: gtk2-devel >= 2.4.0
BuildRequires: libgcrypt-devel
BuildRequires: libhal-devel
BuildRequires: pam-devel
BuildRequires: perl-XML-Parser

%description
gnome-keyring is a program that keep password and other secrets for
users. It is run as a damon in the session, similar to ssh-agent, and
other applications can locate it by an environment variable.
 
The program can manage several keyrings, each with its own master
password, and there is also a session keyring which is never stored to
disk, but forgotten when the session ends.

%package -n %{lib_name}
Group: System/Libraries
Summary: Library for integration with the gnome keyring system
Requires: %{name} >= %{version}-%{release}

%description -n %{lib_name}
The library libgnome-keyring is used by applications to integrate with
the gnome keyring system. However, at this point the library hasn't been
tested and used enought to consider the API to be publically
exposed. Therefore use of libgnome-keyring is at the moment limited to
internal use in the gnome desktop. However, we hope that the
gnome-keyring API will turn out useful and good, so that later it
can be made public for any application to use.


%package -n %{lib_name}-devel
Group: Development/C
Summary: Library for integration with the gnome keyring system
Requires: %{lib_name} = %{version}
Provides: lib%{name}-devel = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{lib_name}-devel
The library libgnome-keyring is used by applications to integrate with
the gnome keyring system. However, at this point the library hasn't been
tested and used enought to consider the API to be publically
exposed. Therefore use of libgnome-keyring is at the moment limited to
internal use in the gnome desktop. However, we hope that the
gnome-keyring API will turn out useful and good, so that later it
can be made public for any application to use.


%prep
%setup -q

%build
%configure2_5x

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std install-pam PAM_DEST_DIR=/%_lib/security
rm -f %buildroot%_libdir/pam_gnome_keyring.*

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc README NEWS TODO COPYING
%{_bindir}/gnome-keyring-daemon
%_libexecdir/gnome-keyring-ask
/%_lib/security/pam_gnome_keyring*.so

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/libgnome-keyring.so.%{lib_major}*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc doc/*.txt COPYING.LIB ChangeLog
%{_libdir}/libgnome-keyring.so
%attr(644,root,root) %{_libdir}/libgnome-keyring.la
%dir %{_includedir}/gnome-keyring-1/
%{_includedir}/gnome-keyring-1/*.h
%{_libdir}/pkgconfig/gnome-keyring-1.pc
%_datadir/gtk-doc/html/*
