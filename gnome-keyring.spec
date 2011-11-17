%define lib_major_gck	0
%define lib_major_gcr	1
%define lib_api_gck	1
%define lib_api_gcr	3

%define libname		%mklibname gcr %{lib_api_gcr} %{lib_major_gcr}
%define libnamegck 	%mklibname gck %{lib_api_gck} %{lib_major_gck}
%define libnamedev 	%mklibname -d gcr 
%define oldlibname 	%mklibname %{name} 0
%define olddevname 	%mklibname -d %{name}

%define url_ver	%(echo %{version}|cut -d. -f1,2)

Summary:	Keyring and password manager for the GNOME desktop
Name:		gnome-keyring
Version:	3.2.2
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		Networking/Remote access
URL:		http://www.gnome.org/
Source0:	http://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	pkgconfig(dbus-1) >= 1.0
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0) >= 2.25.0
BuildRequires:	pkgconfig(gmodule-no-export-2.0)
BuildRequires:	pkgconfig(gobject-2.0) >= 2.8.0
BuildRequires:	pkgconfig(gthread-2.0) >= 2.8.0
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0
BuildRequires:	pkgconfig(libtasn1) >= 0.3.4
BuildRequires:	pkgconfig(p11-kit-1)
BuildRequires:	pkgconfig(gnome-keyring-1) >= 3.0.3
BuildRequires:	libgcrypt-devel
BuildRequires:	libtasn1-tools
BuildRequires:	pam-devel
BuildRequires:	intltool
BuildRequires:	gtk-doc
#gw for keyring management GUI
Suggests:	seahorse

%description
gnome-keyring is a program that keep password and other secrets for
users. It is run as a damon in the session, similar to ssh-agent, and
other applications can locate it by an environment variable.
 
The program can manage several keyrings, each with its own master
password, and there is also a session keyring which is never stored to
disk, but forgotten when the session ends.

%package -n %{libname}
Group:		System/Libraries
Summary:	Library for integration with the gnome keyring system
Conflicts:	%{oldlibname} < 2.29.4
Obsoletes:	%{_lib}gcr-3_0 < 3.1.4
Obsoletes:	%{_lib}gcr-3_1 < 3.1.91

%description -n %{libname}
The library libgnome-keyring is used by applications to integrate with
the gnome keyring system. However, at this point the library hasn't been
tested and used enought to consider the API to be publically
exposed. Therefore use of libgnome-keyring is at the moment limited to
internal use in the gnome desktop. However, we hope that the
gnome-keyring API will turn out useful and good, so that later it
can be made public for any application to use.

%package -n %{libnamegck}
Group:		System/Libraries
Summary:	Library for integration with the gnome keyring system

%description -n %{libnamegck}
The library libgnome-keyring is used by applications to integrate with
the gnome keyring system. However, at this point the library hasn't been
tested and used enought to consider the API to be publically
exposed. Therefore use of libgnome-keyring is at the moment limited to
internal use in the gnome desktop. However, we hope that the
gnome-keyring API will turn out useful and good, so that later it
can be made public for any application to use.

%package -n %{libnamedev}
Group:		Development/C
Summary:	Library for integration with the gnome keyring system
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libnamegck} = %{version}-%{release}
Provides:	libgcr-devel = %{version}-%{release}
Conflicts:	%{olddevname} < 2.29.4

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
%apply_patches

%build
%configure2_5x \
	--with-pam-dir=/%{_lib}/security \
	--disable-static \
	--enable-pam \
	--disable-update-mime \
	--disable-schemas-compile

%make

%install
rm -rf %{buildroot}
%makeinstall_std

#we don't want these
find %{buildroot} -name "*.la" -exec rm -rf {} \;

%find_lang %{name}

%files -f %{name}.lang
%doc README NEWS
%{_sysconfdir}/xdg/autostart/%{name}-gpg.desktop
%{_sysconfdir}/xdg/autostart/%{name}-pkcs11.desktop
%{_sysconfdir}/xdg/autostart/%{name}-secrets.desktop
%{_sysconfdir}/xdg/autostart/%{name}-ssh.desktop
%{_sysconfdir}/pkcs11/modules/%{name}-module
%{_bindir}/%{name}
%{_bindir}/%{name}-%{lib_api_gcr}
%attr(755,root,root) %{_bindir}/%{name}-daemon
%{_bindir}/gcr-viewer
%{_libdir}/%{name}
%{_libdir}/pkcs11
%{_libdir}/%{name}-prompt-%{lib_api_gcr}
%{_libdir}/libmock-test-module.so
%{_libexecdir}/%{name}-prompt
%{_datadir}/%{name}-%{lib_api_gcr}
/%{_lib}/security/pam_gnome_keyring*.so
%{_datadir}/dbus-1/services/org.gnome.keyring.service
%{_datadir}/dbus-1/services/org.freedesktop.secrets.service
%{_datadir}/gcr-%{lib_api_gcr}
%{_datadir}/GConf/gsettings/*.convert
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/applications/%{name}-prompt.desktop
%{_datadir}/applications/gcr-viewer.desktop
%{_datadir}/icons/hicolor/*/apps/gcr-key*.png
%{_datadir}/mime/packages/*.xml

%files -n %{libnamegck}
%{_libdir}/libgck-%{lib_api_gck}.so.%{lib_major_gck}*

%files -n %{libname}
%{_libdir}/libgcr-%{lib_api_gcr}.so.%{lib_major_gcr}*

%files -n %{libnamedev}
%{_libdir}/libgck-%{lib_api_gck}.so
%{_libdir}/libgcr-%{lib_api_gcr}.so
%{_includedir}/gck-%{lib_api_gck}
%{_includedir}/gcr-%{lib_api_gcr}
%{_libdir}/pkgconfig/gck-%{lib_api_gck}.pc
%{_libdir}/pkgconfig/gcr-%{lib_api_gcr}.pc
%doc %{_datadir}/gtk-doc/html/*

