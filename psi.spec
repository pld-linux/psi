#
%define         snap 20040302
#
Summary:	PSI - Jabber client
Summary(pl):	PSI - klient Jabbera
Name:		psi
Version:	0.9.2
Release:	0.%{snap}.1
License:	GPL
Group:		Applications/Communications
Source0:	%{name}-snap-%{snap}.tar.bz2
# Source0-md5:	9ca1783f59c7ad3362eff81f6e808e9e
Patch0:		%{name}-certs.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-home_etc.patch
Patch3:		%{name}-customos.patch
Patch4:		%{name}-status_indicator-add.patch
Patch5:		%{name}-no_default_status_text-mod.patch
Patch6:		%{name}-no_online_status-mod.patch
Patch7:		%{name}-status_history-add.patch
Patch8:		%{name}-offline_status-add.patch
URL:		http://psi.affinix.com/
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel >= 0.9.7c
BuildRequires:	qt-devel >= 3.1.2
Requires:	qt-plugin-qca-tls >= 1:1.1
Conflicts:	qt-plugin-ssl = 1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PSI is a communicator for the Jabber open messaging system. It is
based on the QT library. It supports SSL encrypted connections. The
default behaviour for SSL was changed so that it looks for SSL
certificates in $DATADIR/certs or in ~/.psi/certs.

This is a development version (CVS).

%description -l pl
PSI jest komunikatorem dla otwartego systemu wiadomo¶ci Jabber. Zosta³
stworzony w oparciu o bibliotekê QT. PSI wspiera po³±czenia szyfrowane
SSL. W stosunku do domy¶lnego zachowania komunikatora zosta³a
wprowadzona zmiana, która powoduje ¿e certyfikaty SSL s± poszukiwane w
katalogu $DATADIR/certs lub ~/.psi/certs.

Jest to wersja rozwojowa (CVS).

%package -n qt-plugin-qca-tls
Summary:	Qt Cryptographic Architecture (QCA) SSL/TLS plugin
Summary(pl):	Wtyczka SSL/TLS dla Qt Cryptographic Architecture (QCA)
Version:	1.1
Epoch:		1
License:	GPL v2
Group:		Libraries

%define         _plugindir %{_libdir}/qt/plugins-mt/crypto

%description -n qt-plugin-qca-tls
A plugin to provide SSL/TLS capability to programs that utilize the Qt
Cryptographic Architecture (QCA).

This is a development version (CVS).

%description -n qt-plugin-qca-tls -l pl
Wtyczka pozwalaj±ca wykorzystaæ mo¿liwo¶ci SSL/TLS w programach
korzystaj±cych z Qt Cryptographic Architecture (QCA).

Jest to wersja rozwojowa (CVS).

%prep
%setup -q -c %{name}-%{version}
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p0

%{__perl} -pi -e "s/QString PROG_VERSION = \"0.9.1-CVS\";/QString PROG_VERSION = \"0.9.2-%{snap}\";/g" psi/src/common.cpp
%{__perl} -pi -e "s,/usr/local/share/psi,%{_datadir}/psi,g" psi/src/common.cpp
%{__perl} -pi -e 's/CONFIG \+= debug//g' psi/src/src.pro

%build
cd psi
export QTDIR=%{_prefix}
./configure \
	--prefix=%{_prefix}

qmake psi.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_LINK="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcflags}" \
	QMAKE_RPATH=

lrelease lang/*.ts

%{__make}

cd ..
cd qca/plugins/qca-tls

./configure

qmake qca-tls.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_LINK="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcflags}" \
	QMAKE_RPATH=

%{__make}

cd ../../..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

export QTDIR=%{_prefix}

cd psi
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
cd ..

cd qca/plugins/qca-tls
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
cd ../../..

install psi/psi.desktop $RPM_BUILD_ROOT%{_desktopdir}
install psi/iconsets/system/default/icon_48.png $RPM_BUILD_ROOT%{_pixmapsdir}/psi.png
install psi/iconsets/roster/stellar-icq/online.png $RPM_BUILD_ROOT%{_pixmapsdir}/psi-stellar.png
install psi/lang/*.qm $RPM_BUILD_ROOT%{_datadir}/psi

rm $RPM_BUILD_ROOT%{_datadir}/psi/COPYING $RPM_BUILD_ROOT%{_datadir}/psi/README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc psi/README psi/TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/psi
%{_datadir}/psi/designer
%{_datadir}/psi/certs
%{_datadir}/psi/iconsets
%{_datadir}/psi/sound
%lang(ar) %{_datadir}/psi/psi_ar.qm
%lang(ca) %{_datadir}/psi/psi_ca.qm
%lang(cs) %{_datadir}/psi/psi_cs.qm
%lang(da) %{_datadir}/psi/psi_da.qm
%lang(de) %{_datadir}/psi/psi_de.qm
%lang(el) %{_datadir}/psi/psi_el.qm
%lang(eo) %{_datadir}/psi/psi_eo.qm
%lang(es) %{_datadir}/psi/psi_es.qm
%lang(fi) %{_datadir}/psi/psi_fi.qm
%lang(fr) %{_datadir}/psi/psi_fr.qm
%lang(it) %{_datadir}/psi/psi_it.qm
%lang(jp) %{_datadir}/psi/psi_jp.qm
%lang(mk) %{_datadir}/psi/psi_mk.qm
%lang(nl) %{_datadir}/psi/psi_nl.qm
%lang(pl) %{_datadir}/psi/psi_pl.qm
%lang(ptbr) %{_datadir}/psi/psi_ptbr.qm
%lang(pt) %{_datadir}/psi/psi_pt.qm
%lang(ru) %{_datadir}/psi/psi_ru.qm
%lang(se) %{_datadir}/psi/psi_se.qm
%lang(sk) %{_datadir}/psi/psi_sk.qm
%lang(sr) %{_datadir}/psi/psi_sr.qm
%lang(zh) %{_datadir}/psi/psi_zh.qm
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png

%files -n qt-plugin-qca-tls
%defattr(644,root,root,755)
%doc qca/plugins/qca-tls/README
%dir %{_plugindir}
%attr(755,root,root) %{_plugindir}/*.so
