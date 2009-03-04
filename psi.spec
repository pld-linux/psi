Summary:	PSI - Jabber client
Summary(de.UTF-8):	PSI - ein Instant Messaging Client-Programm für Jabber
Summary(pl.UTF-8):	PSI - klient Jabbera
Name:		psi
Version:	0.12
Release:	4
License:	GPL v2
Group:		Applications/Communications
Source0:	http://dl.sourceforge.net/psi/%{name}-%{version}.tar.bz2
# Source0-md5:	47b654c944ef8766b860fe0645615d18
Patch0:		%{name}-fix_configure_for_ksh.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-home_etc.patch
Patch3:		%{name}-customos.patch
Patch4:		%{name}-no_online_offline_status.patch
Patch5:		%{name}-icon_buttons_big_return-mod.patch
Patch6:		%{name}-empty_group-fix.patch
Patch7:		%{name}-appearance-mod.patch
# http://machekku.uaznia.net/xmpp/psi/patches/
Patch8:		%{name}-machekku-avatars_in_tooltip.patch
Patch9:		%{name}-qt4.5.patch
URL:		http://psi-im.org/
BuildRequires:	Qt3Support-devel
BuildRequires:	QtCore-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtXml-devel
BuildRequires:	aspell-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel >= 0.9.7c
BuildRequires:	qca-devel >= 2.0.0
BuildRequires:	qt4-build >= 4.3.3-3
BuildRequires:	qt4-qmake >= 4.3.3-3
#BuildRequires:	QtDBus-devel >= 4.3.3-3
BuildRequires:	which
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xorg-proto-scrnsaverproto-devel
BuildRequires:	zlib-devel
Requires:	qt4-plugin-qca-ossl
Suggests:	gpgme >= 1.0.0
Obsoletes:	qt-designer-psiwidgets
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PSI is a communicator for the Jabber open messaging system. It is
based on the Qt library. It supports SSL encrypted connections. The
default behaviour for SSL was changed so that it looks for SSL
certificates in $DATADIR/certs or in ~/.psi/certs.

%description -l de.UTF-8
Psi ist ein Instant Messaging (IM) Client-Programm für das
Jabber-Protokoll (XMPP), welches das Qt Toolkit nutzt.

%description -l pl.UTF-8
PSI jest komunikatorem dla otwartego systemu wiadomości Jabber.
Został stworzony w oparciu o bibliotekę Qt. PSI wspiera połączenia
szyfrowane SSL. W stosunku do domyślnego zachowania komunikatora
została wprowadzona zmiana, która powoduje że certyfikaty SSL są
poszukiwane w katalogu $DATADIR/certs lub ~/.psi/certs.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%{?with_home_etc:%patch2 -p1}
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p0

rm -rf third-party

%build
./configure \
	--prefix=%{_prefix} \
	--datadir=%{_datadir}

qmake-qt4
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

export QTDIR=%{_libdir}/qt4

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL README
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/psi
%{_datadir}/psi/certs
%{_datadir}/psi/iconsets
%{_datadir}/psi/sound
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/*.png
