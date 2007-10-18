# TODO:
# - fix configure so it works nicely with pdksh
#
Summary:	PSI - Jabber client
Summary(de.UTF-8):	PSI - ein Instant Messaging Client-Programm für Jabber
Summary(pl.UTF-8):	PSI - klient Jabbera
Name:		psi
Version:	0.11
Release:	0.1
License:	GPL v2
Group:		Applications/Communications
Source0:	http://dl.sourceforge.net/psi/%{name}-%{version}.tar.bz2
# Source0-md5:	6ccc81783eece7959140951289cf5310
URL:		http://psi-im.org/
BuildRequires:	Qt3Support-devel
BuildRequires:	QtCore-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtXml-devel
BuildRequires:	aspell-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel >= 0.9.7c
BuildRequires:	qca-devel >= 2.0.0
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
BuildRequires:	zlib-devel
Requires:	qt4-plugin-qca-ossl
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
rm -rf third-party

%build
export QTDIR=%{_libdir}/qt4

bash ./configure \
	--prefix=%{_prefix} \
		--datadir=%{_datadir}


%{_libdir}/qt4/bin/qmake psi.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_LINK="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcflags}" \
	QMAKE_RPATH=

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
