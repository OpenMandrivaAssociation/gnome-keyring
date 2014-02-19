%define url_ver	%(echo %{version}|cut -d. -f1,2)

%define api	3

Summary:	Keyring and password manager for the GNOME desktop
Name:		gnome-keyring
Version:	3.6.3
Release:	5
License:	GPLv2+ and LGPLv2+
Group:		Networking/Remote access
Url:		http://www.gnome.org/
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

%find_lang %{name} %{name}.lang

%files -f %{name}.lang
%doc README NEWS
%{_sysconfdir}/xdg/autostart/%{name}-gpg.desktop
%{_sysconfdir}/xdg/autostart/%{name}-pkcs11.desktop
%{_sysconfdir}/xdg/autostart/%{name}-secrets.desktop
%{_sysconfdir}/xdg/autostart/%{name}-ssh.desktop
%{_datadir}/pkcs11/modules/%{name}.module
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
