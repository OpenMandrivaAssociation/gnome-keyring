%define url_ver %(echo %{version}|cut -d. -f1,2)

%define api 3

Summary:	Keyring and password manager for the GNOME desktop
Name:		gnome-keyring
Version:	48.beta
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		Networking/Remote access
Url:		https://www.gnome.org/
Source0:	https://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
BuildRequires:	meson
BuildRequires:	intltool
BuildRequires:	glib2.0-common
BuildRequires:	gtk-doc
BuildRequires:	libtasn1-tools
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(dbus-1) >= 1.0
BuildRequires:	pkgconfig(gck-1) >= 3.3.4
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0
#BuildRequires:	pkgconfig(libcrypt)
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(libtasn1)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:	pkgconfig(gcr-3)
BuildRequires:	openssh-clients
BuildRequires:	xsltproc
BuildRequires:	docbook-style-xsl
Requires:	at-spi2-core
#gw for keyring management GUI
Recommends:	gcr
Recommends:	seahorse

%description
gnome-keyring is a program that keep password and other secrets for
users. It is run as a damon in the session, similar to ssh-agent, and
other applications can locate it by an environment variable.

The program can manage several keyrings, each with its own master
password, and there is also a session keyring which is never stored to
disk, but forgotten when the session ends.

%prep
%autosetup -p1

%build
%meson \
           -Dpam=true \
           -Dsystemd=enabled \
           -Dpkcs11-config=%{_datadir}/p11-kit/modules \
           -Dssh-agent=true

%meson_build

%install
%meson_install

%find_lang %{name} %{name}.lang

%post
%systemd_user_post gnome-keyring-daemon.service
 
%preun
%systemd_user_preun gnome-keyring-daemon.service

%files -f %{name}.lang
%doc README NEWS
%{_sysconfdir}/xdg/autostart/%{name}-pkcs11.desktop
%{_sysconfdir}/xdg/autostart/%{name}-secrets.desktop
%{_sysconfdir}/xdg/autostart/%{name}-ssh.desktop
#{_datadir}/p11-kit/modules/%{name}.module
%{_bindir}/%{name}
%{_bindir}/%{name}-%{api}
%attr(755,root,root) %{_bindir}/%{name}-daemon
%{_libdir}/%{name}
%{_libdir}/pkcs11
%{_libdir}/security/pam_gnome_keyring*.so
%{_datadir}/dbus-1/services/*.service
%{_datadir}/xdg-desktop-portal/portals/gnome-keyring.portal
%{_datadir}/GConf/gsettings/*.convert
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/p11-kit/modules/gnome-keyring.module
%{_mandir}/man1/*	
%{_userunitdir}/gnome-keyring-daemon.service
%{_userunitdir}/gnome-keyring-daemon.socket
