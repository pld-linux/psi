# 
# Conditional build:
%bcond_with	customos	# enables OS identification changing ~/.psi/custom-os
#
Summary:	PSI - Jabber client
Summary(pl):	PSI - klient Jabbera
Name:		psi
Version:	0.9.1
Release:	0.99
License:	GPL
Group:		Applications/Communications
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
# Source0-md5:	7057b61518e1b1ebd732a95c265a3b76
Source1:	%{name}-langpack-%{version}.tar.bz2
# Source1-md5:	77f5d5544758c846839932fc9b5e9996
Patch0:		%{name}-certs.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-home_etc.patch
Patch3:		%{name}-customos.patch
URL:		http://psi.affinix.com/
BuildRequires:	qt-devel >= 3.1.2
Requires:	qt-plugin-qca-tls >= 1:1.0
Conflicts:	qt-plugin-ssl = 1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%{?with_customos:%patch3 -p1}

%{__perl} -pi -e "s/QString PROG_VERSION = \"0.9.1\";/QString PROG_VERSION = \"0.9.1-%{release}\";/g" src/common.cpp
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

QTDIR=%{_prefix} \
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install psi.desktop $RPM_BUILD_ROOT%{_desktopdir}
install iconsets/system/default/icon_48.png $RPM_BUILD_ROOT%{_pixmapsdir}/psi.png
install lang/*.qm $RPM_BUILD_ROOT%{_datadir}/psi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/psi
%{_datadir}/psi/COPYING
%{_datadir}/psi/README
%{_datadir}/psi/certs
%{_datadir}/psi/iconsets
%{_datadir}/psi/sound
%lang(ca) %{_datadir}/psi/psi_ca.qm
%lang(cs) %{_datadir}/psi/psi_cs.qm
%lang(de) %{_datadir}/psi/psi_de.qm
%lang(es) %{_datadir}/psi/psi_es.qm
%lang(el) %{_datadir}/psi/psi_el.qm
%lang(fr) %{_datadir}/psi/psi_fr.qm
%lang(it) %{_datadir}/psi/psi_it.qm
%lang(mk) %{_datadir}/psi/psi_mk.qm
%lang(nl) %{_datadir}/psi/psi_nl.qm
%lang(pl) %{_datadir}/psi/psi_pl.qm
%lang(se) %{_datadir}/psi/psi_se.qm
%lang(sk) %{_datadir}/psi/psi_sk.qm
%lang(zh) %{_datadir}/psi/psi_zh.qm
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
