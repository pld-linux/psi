%define		_rel test1
Summary:        PSI - Jabber client
Summary(pl):    PSI - klient Jabbera
Name:           psi
Version:        0.9.1
Release:        0.%{_rel}.1
License:        GPL
Group:          Applications/Communications
Source0:        http://psi.affinix.com/beta/%{name}-%{version}-%{_rel}.tar.bz2
# Source0-md5:	5822a69752d3450a21ad49b6d7137e0c
Patch0:         %{name}-certs.patch
Patch1:		%{name}-desktop.patch
URL:            http://psi.affinix.com/
BuildRequires:  qt-devel >= 3.1.2
Requires:	qt-plugin-qca-tls >= 20031208
BuildRoot:      %{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PSI is communicator for Jabber open messaging system. It is based on
QT library. It supports SSL encrypted connections. Default behaviour
for SSL was changed so it looks for SSL certificates in $DATADIR/certs
or in ~/.psi/certs.

%description -l pl
PSI jest komunikatorem dla otwartego systemu wiadomo¶ci Jabber. Zosta³
stworzony w oparciu o bibliotekê QT. PSI wspiera po³±czenia szyfrowane
SSL. W stosunku do domy¶lnego zachowania komunikatora zosta³a
wprowadzona zmiana, która powoduje ¿e certyfikaty SSL poszukiwane s± w
katalogu $DATADIR/certs lub ~/.psi/certs.

%prep
%setup  -qn %{name}-%{version}-%{_rel}
%patch0 -p1
%patch1 -p1

%{__perl} -pi -e "s/QString PROG_VERSION = \"0.9.1-%{_rel}\";/QString PROG_VERSION = \"0.9.1-%{release}\";/g" src/common.cpp
%{__perl} -pi -e "s,/usr/local/share/psi,%{_datadir}/psi,g" src/common.cpp
%{__perl} -pi -e 's/CONFIG \+= debug//g' src/src.pro

%build
export QTDIR=%{_prefix}
./configure \
        --prefix=%{_prefix} \
	--qtdir=%{_prefix}

qmake psi.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_LINK="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcflags}" \
	QMAKE_RPATH=

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

QTDIR=%{_prefix} %{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -c psi.desktop $RPM_BUILD_ROOT%{_desktopdir}
install -c iconsets/system/default/icon_48.png $RPM_BUILD_ROOT%{_pixmapsdir}/psi.png

#rm -f $RPM_BUILD_ROOT%{_datadir}/psi/certs/*.pem

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_bindir}/*
%{_datadir}/psi
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
