#
# Conditional build:
# _with_addons		- enables additional GUI features
#
Summary:	PSI - Jabber client
Summary(pl):	PSI - klient Jabbera
Name:		psi
Version:	0.9
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
# Source0-md5:	bf3aaa7fa8a1efdff9f96fa718366aa8
Source2:	%{name}.desktop
Patch0:		%{name}-paths.patch
Patch1:		%{name}-certs.patch
Patch2:		%{name}-additional_features.patch
URL:		http://psi.affinix.com/
BuildRequires:	qt-devel >= 3.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	qt-plugin-ssl = 1.0

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
%{?_with_addons:%patch2 -p1}
perl -pi -e "s/QString PROG_VERSION = \"0.9\";/QString PROG_VERSION = \"0.9-%{release}\";/g" src/common.cpp
perl -pi -e "s,/usr/local/share/psi,/usr/share/psi,g" src/common.cpp

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

lrelease psi.pro

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_libdir}/psi \
	$RPM_BUILD_ROOT%{_datadir}/psi/translations

# ugly workaround: they ignore INSTALL_ROOT!
perl -pi -e 's#(\.\./)+#/#g' Makefile

QTDIR=%{_prefix} %{__make} install INSTALL_ROOT=$RPM_BUILD_ROOT

install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
cp lang/*.qm $RPM_BUILD_ROOT%{_datadir}/psi/translations

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
%lang(ar) %{_datadir}/psi/translations/psi_ar.qm
%lang(da) %{_datadir}/psi/translations/psi_da.qm
%lang(cs) %{_datadir}/psi/translations/psi_cs.qm
%lang(de) %{_datadir}/psi/translations/psi_de.qm
%lang(es) %{_datadir}/psi/translations/psi_es.qm
%lang(fi) %{_datadir}/psi/translations/psi_fi.qm
%lang(fr) %{_datadir}/psi/translations/psi_fr.qm
%lang(ja) %{_datadir}/psi/translations/psi_jp.qm
%lang(mk) %{_datadir}/psi/translations/psi_mk.qm
%lang(nl) %{_datadir}/psi/translations/psi_nl.qm
%lang(pl) %{_datadir}/psi/translations/psi_pl.qm
%lang(ru) %{_datadir}/psi/translations/psi_ru.qm
%lang(sr) %{_datadir}/psi/translations/psi_sr.qm
%lang(it) %{_datadir}/psi/translations/psi_it.qm
%lang(pt) %{_datadir}/psi/translations/psi_pt.qm
%lang(pt_BR) %{_datadir}/psi/translations/psi_ptbr.qm
%lang(se) %{_datadir}/psi/translations/psi_se.qm
%lang(zh) %{_datadir}/psi/translations/psi_zh.qm

%{_libdir}/psi
%{_desktopdir}/psi.desktop
