# --without-qssl 	Disable qssl support.

Summary:	PSI - Jabber client
Summary(pl):	PSI - klient Jabbera
Name:		psi
Version:	0.8.7
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/psi/%{name}-%{version}.tar.bz2
Source2:	%{name}.desktop
# Translation files ftom http://psi.sourceforge.net/
Source3:	%{name}_cz.ts
Source4:	%{name}_de.ts
Source5:	%{name}_es.ts
Source6:	%{name}_fr.ts
Source7:	%{name}_mk.ts
Source8:	%{name}_nl.ts
Source9:	%{name}_pl.ts
Source10:	%{name}_ru.ts
Patch0:		%{name}-include.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-certs.patch
URL:		http://psi.affinix.com/
BuildRequires:	qt-devel >= 3.0.5
%{!?_without_qssl:BuildRequires:	qt-plugin-ssl-devel >= 1.0-2}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_xprefix	%{_prefix}/X11R6
%define		_xdatadir	%{_xprefix}/share
%define		_xbindir	%{_xprefix}/bin

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
%setup  -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
QTDIR=%{_xprefix}
QMAKESPEC=%{_xdatadir}/qt/mkspecs/linux-g++
export QTDIR QMAKESPEC

./configure \
	--prefix %{_xprefix} \
	--libdir %{_xdatadir}/psi \
	--qtdir $QTDIR
%{__make} \
	CXX=%{__cxx} LINK=%{__cxx} CXXFLAGS="-pipe -Wall %{rpmcflags} \
	-fno-exceptions -D_REENTRANT %{?debug:-DQT_NO_DEBUG} -DQT_THREAD_SUPPORT"

cd src
cp %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} \
	%{SOURCE9} %{SOURCE10} .
lrelease psi.pro
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_applnkdir}/Network/Communications \
	$RPM_BUILD_ROOT%{_libdir}/psi \
	$RPM_BUILD_ROOT%{_xdatadir}/psi/translations

%{__make} install INSTALL_ROOT=$RPM_BUILD_ROOT

install %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/Network/Communications
rm -f src/tr.qm
cp src/*.qm $RPM_BUILD_ROOT%{_xdatadir}/psi/translations

rm -f $RPM_BUILD_ROOT%{_xdatadir}/psi/{certs/*.pem,{README,COPYING}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_xbindir}/*
%dir %{_xdatadir}/psi
%dir %{_xdatadir}/psi/translations
%{_xdatadir}/psi/certs
%{_xdatadir}/psi/iconsets
%{_xdatadir}/psi/image
%{_xdatadir}/psi/sound
%lang(cs) %{_xdatadir}/psi/translations/psi_cz.qm
%lang(de) %{_xdatadir}/psi/translations/psi_de.qm
%lang(es) %{_xdatadir}/psi/translations/psi_es.qm
%lang(fr) %{_xdatadir}/psi/translations/psi_fr.qm
%lang(nl) %{_xdatadir}/psi/translations/psi_nl.qm
%lang(pl) %{_xdatadir}/psi/translations/psi_pl.qm
%lang(ru) %{_xdatadir}/psi/translations/psi_ru.qm
%{_libdir}/psi
%{_applnkdir}/Network/Communications/%{name}.desktop
