#
# Conditional build:
# _with_addons		- enables additional GUI features
# _with_customos	- enables OS identification changing ~/.psi/custom-os
# _with_pld		- enables PLD Linux identification
#
Summary:	PSI - Jabber client
Summary(pl):	PSI - klient Jabbera
Name:		psi
Version:	0.9.1
Release:	0.1
License:	GPL
Group:		Applications/Communications
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
# Source0-md5:	7057b61518e1b1ebd732a95c265a3b76
Source1:	http://beta.jabberpl.org/komunikatory/psi/psi_pl.qm
# Source1-md5:	4ffe9c032a4ebf35cb6943187b560f9c
Source2:	%{name}.desktop
#Patch0:		%{name}-paths.patch
#Patch1:		%{name}-certs.patch
#Patch2:		%{name}-additional_features.patch
#Patch3:		%{name}-pld.patch
#Patch4:		%{name}-home_etc.patch
#Patch5:		%{name}-customos.patch
Patch0:		%{name}-certs.patch
Patch1:		%{name}-desktop.patch
URL:		http://psi.affinix.com/
BuildRequires:	qt-devel >= 3.1.2
Requires:	qt-plugin-qca-tls >= 20031208
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	qt-plugin-ssl = 1.0

%description
PSI is a communicator for the Jabber open messaging system. It is
based on the QT library. It supports SSL encrypted connections. The
default behaviour for SSL was changed so that it looks for SSL
certificates in $DATADIR/certs or in ~/.psi/certs.

%description -l pl
PSI jest komunikatorem dla otwartego systemu wiadomo¶ci Jabber. Zosta³
stworzony w oparciu o bibliotekê QT. PSI wspiera po³±czenia szyfrowane
SSL. W stosunku do domy¶lnego zachowania komunikatora zosta³a
wprowadzona zmiana, która powoduje ¿e certyfikaty SSL s± poszukiwane w
katalogu $DATADIR/certs lub ~/.psi/certs.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1
#%{?_with_addons:%patch2 -p1}
#%if %{undefined _with_pld} && %{defined _with_customos}
#%patch5 -p1
#%else
#%patch3 -p1
#%endif
#%patch4 -p1
%{__perl} -pi -e "s/QString PROG_VERSION = \"0.9.1\";/QString PROG_VERSION = \"0.9.1-%{release}\";/g" src/common.cpp
%{__perl} -pi -e "s,/usr/local/share/psi,%{_datadir}/psi,g" src/common.cpp
%{__perl} -pi -e 's/CONFIG \+= debug//g' src/src.pro

%build
QTDIR=%{_prefix}
export QTDIR

./configure \
	--prefix=%{_prefix} \
	--qtdir=$QTDIR

qmake psi.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_LINK="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcflags}" \
	QMAKE_RPATH=

%{__make}

# lrelease psi.pro

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_libdir}/psi,%{_datadir}/psi/translations,%{_pixmapsdir}}

# ugly workaround: they ignore INSTALL_ROOT!
perl -pi -e 's#(\.\./)+#/#g' Makefile

QTDIR=%{_prefix} %{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/%{name}/
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
# cp lang/*.qm $RPM_BUILD_ROOT%{_datadir}/psi/translations

rm -f $RPM_BUILD_ROOT%{_datadir}/psi/certs/*.pem

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/psi
%dir %{_datadir}/psi/translations
%{_datadir}/psi/README
%{_datadir}/psi/COPYING
%{_datadir}/psi/certs
%{_datadir}/psi/iconsets
#%{_datadir}/psi/image
%{_datadir}/psi/sound
#%lang(ar) %{_datadir}/psi/translations/psi_ar.qm
#%lang(da) %{_datadir}/psi/translations/psi_da.qm
#%lang(cs) %{_datadir}/psi/translations/psi_cs.qm
#%lang(de) %{_datadir}/psi/translations/psi_de.qm
#%lang(es) %{_datadir}/psi/translations/psi_es.qm
#%lang(fi) %{_datadir}/psi/translations/psi_fi.qm
#%lang(fr) %{_datadir}/psi/translations/psi_fr.qm
#%lang(ja) %{_datadir}/psi/translations/psi_jp.qm
#%lang(mk) %{_datadir}/psi/translations/psi_mk.qm
#%lang(nl) %{_datadir}/psi/translations/psi_nl.qm
#%lang(pl) %{_datadir}/psi/translations/psi_pl.qm
#%lang(ru) %{_datadir}/psi/translations/psi_ru.qm
#%lang(sr) %{_datadir}/psi/translations/psi_sr.qm
#%lang(it) %{_datadir}/psi/translations/psi_it.qm
#%lang(pt) %{_datadir}/psi/translations/psi_pt.qm
#%lang(pt_BR) %{_datadir}/psi/translations/psi_ptbr.qm
#%lang(sv) %{_datadir}/psi/translations/psi_se.qm
#%lang(zh) %{_datadir}/psi/translations/psi_zh.qm
#
%{_libdir}/psi
%{_desktopdir}/psi.desktop
#%{_pixmapsdir}/*.png
