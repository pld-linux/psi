#
# Conditional build:
# _without_qssl 	Disable qssl support
#
Summary:	PSI - Jabber client
Summary(pl):	PSI - klient Jabbera
Name:		psi
Version:	0.8.7
Release:	3
License:	GPL
Group:		Applications/Communications
Source0:	http://heanet.dl.sourceforge.net/sourceforge/psi/%{name}-%{version}.tar.bz2
# Source0-md5:	4e18ea341dca70556d0dc1baf026ef86	
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
Source11:       %{name}_br.ts
Source12:	%{name}_fi.ts
Patch0:		%{name}-include.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-certs.patch
URL:		http://psi.affinix.com/
BuildRequires:	qt-devel >= 3.0.5
%{!?_without_qssl:BuildRequires:	qt-plugin-ssl-devel >= 1.0-2}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%{!?_without_qssl:%patch0 -p1}
%patch1 -p1
%patch2 -p1

%build
QTDIR=%{_prefix}
QMAKESPEC=%{_datadir}/qt/mkspecs/linux-g++
export QTDIR QMAKESPEC

./configure \
	--prefix %{_prefix} \
	--libdir %{_datadir}/psi \
	--qtdir $QTDIR
%{__make} \
	CXX=%{__cxx} LINK=%{__cxx} CXXFLAGS="-pipe -Wall %{rpmcflags} \
	-fno-exceptions -D_REENTRANT %{?debug:-DQT_NO_DEBUG} -DQT_THREAD_SUPPORT"

cd src
cp %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} \
	%{SOURCE9} %{SOURCE10}  %{SOURCE11}  %{SOURCE12} .
lrelease psi.pro
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_libdir}/psi \
	$RPM_BUILD_ROOT%{_datadir}/psi/translations

%{__make} install INSTALL_ROOT=$RPM_BUILD_ROOT

install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
rm -f src/tr.qm
cp src/*.qm $RPM_BUILD_ROOT%{_datadir}/psi/translations

rm -f $RPM_BUILD_ROOT%{_datadir}/psi/{certs/*.pem,{README,COPYING}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/psi
%dir %{_datadir}/psi/translations
%{_datadir}/psi/certs
%{_datadir}/psi/iconsets
%{_datadir}/psi/image
%{_datadir}/psi/sound
%lang(cs) %{_datadir}/psi/translations/psi_cz.qm
%lang(de) %{_datadir}/psi/translations/psi_de.qm
%lang(es) %{_datadir}/psi/translations/psi_es.qm
%lang(fr) %{_datadir}/psi/translations/psi_fr.qm
%lang(nl) %{_datadir}/psi/translations/psi_nl.qm
%lang(pl) %{_datadir}/psi/translations/psi_pl.qm
%lang(ru) %{_datadir}/psi/translations/psi_ru.qm
%lang(fi) %{_datadir}/psi/translations/psi_fi.qm
%lang(pt_BR) %{_datadir}/psi/translations/psi_br.qm
%lang(mk) %{_datadir}/psi/translations/psi_mk.qm
%{_libdir}/psi
%{_desktopdir}
