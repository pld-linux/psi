#
# Conditional build:
%bcond_with	square_timestamps	# this is how they used to be
#
%define		snap 20040611
#
Summary:	PSI - Jabber client
Summary(pl):	PSI - klient Jabbera
Name:		psi
Version:	0.9.3
Release:	0.%{snap}.1
License:	GPL
Group:		Applications/Communications
Source0:	%{name}-snap-%{snap}.tar.bz2
# Source0-md5:	966314d7558e3317bf0abc263a87c2b2
Source1:	%{name}-richlistview.cpp
Source2:	%{name}-richlistview.h
Source3:	%{name}-roster-rich.README
Source4:	%{name}-indicator.png
Patch0:		%{name}-certs.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-home_etc.patch
Patch3:		%{name}-customos.patch
Patch4:		%{name}-status_indicator-add.patch
Patch5:		%{name}-no_default_status_text-mod.patch
Patch6:		%{name}-no_online_status-mod.patch
Patch7:		%{name}-status_history-add.patch
Patch8:		%{name}-offline_status-add.patch
Patch9:		%{name}-icon_buttons_big_return-mod.patch
Patch10:	%{name}-nicechats-mod.patch
Patch11:	%{name}-roster-rich.patch
Patch12:	%{name}-icondef.xml_status_indicator.patch
Patch13:	%{name}-timestamps.patch
URL:		http://psi.affinix.com/
BuildRequires:	libstdc++-devel
BuildRequires:	cyrus-sasl-devel
BuildRequires:	openssl-devel >= 0.9.7c
BuildRequires:	qmake
BuildRequires:	qt-devel >= 3.3.2-5
BuildRequires:	qt-linguist
Requires:	qt-plugin-qca-tls >= 1:1.1
Conflicts:	qt-plugin-ssl = 1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir %{_libdir}/qt/plugins-mt/crypto

%description
PSI is a communicator for the Jabber open messaging system. It is
based on the QT library. It supports SSL encrypted connections. The
default behaviour for SSL was changed so that it looks for SSL
certificates in $DATADIR/certs or in ~/.psi/certs.

This is a development version (CVS) with SKaZi's patches.

%description -l pl
PSI jest komunikatorem dla otwartego systemu wiadomo¶ci Jabber. Zosta³
stworzony w oparciu o bibliotekê QT. PSI wspiera po³±czenia szyfrowane
SSL. W stosunku do domy¶lnego zachowania komunikatora zosta³a
wprowadzona zmiana, która powoduje ¿e certyfikaty SSL s± poszukiwane w
katalogu $DATADIR/certs lub ~/.psi/certs.

Jest to wersja rozwojowa (CVS) z ³atkami SKaZiego.

%package -n qt-designer-psiwidgets
Summary:	Psi widgets collection for Qt Designer
Summary(pl):	Kolekcja widgetów Psi do wykorzystania w Projektancie Qt
License:	GPL v2
Group:		X11/Development/Libraries

%description -n qt-designer-psiwidgets
This is a package of widgets, that are used in Psi You may be interested in it,
if you want to develop custom dialogs, or hack existing ones.

%description -n qt-designer-psiwidgets -l pl
Pakiet ten zawiera wtyczke dla programu Qt Designer, bed±c± zbiorem widgetów
u¿ytych w programie Psi. Moze Ci siê przydaæ, jesli chcia³by¶ na[pisaæ w³asne
okna dialogowe itp. albo poprawiæ obecne.

%package -n qt-plugin-qca-tls
Summary:	Qt Cryptographic Architecture (QCA) SSL/TLS plugin
Summary(pl):	Wtyczka SSL/TLS dla Qt Cryptographic Architecture (QCA)
Version:	1.1
Epoch:		1
License:	GPL v2
Group:		Libraries

%description -n qt-plugin-qca-tls
A plugin to provide SSL/TLS capability to programs that utilize the Qt
Cryptographic Architecture (QCA).	

This is a development version (CVS).

%description -n qt-plugin-qca-tls -l pl
Wtyczka pozwalaj±ca wykorzystaæ mo¿liwo¶ci SSL/TLS w programach
korzystaj±cych z Qt Cryptographic Architecture (QCA).

Jest to wersja rozwojowa (CVS).

%package -n qt-plugin-qca-sasl
Summary:	Qt Cryptographic Architecture (QCA) SASL plugin
Summary(pl):	Wtyczka SASL dla Qt Cryptographic Architecture (QCA)
Version:	1.0
License:	GPL v2
Group:		Libraries

%description -n qt-plugin-qca-sasl
A plugin to provide SASL capability to programs that utilize the Qt
Cryptographic Architecture (QCA).

This is a development version (CVS).

%description -n qt-plugin-qca-sasl -l pl
Wtyczka pozwalaj±ca wykorzystaæ mo¿liwo¶ci SASL w programach
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
%patch9 -p0
%patch10 -p0
%patch11 -p0
%patch12 -p0
%{?with_square_timestamps:%patch13 -p1}

sed -i \
	's/QString PROG_VERSION = .*/QString PROG_VERSION = "0.9.3-%{snap}";/g' \
	psi/src/common.cpp
sed -i \
	"s,/usr/local/share/psi,%{_datadir}/psi,g" \
	psi/src/common.cpp

cp %{SOURCE1} psi/src/richlistview.cpp
cp %{SOURCE2} psi/src/richlistview.h
cp %{SOURCE3} psi/README.rich-roster
cp %{SOURCE4} psi/indicator.png

%build
export QTDIR=%{_prefix}

cd psi
./configure \
	--prefix=%{_prefix}

qmake psi.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_LINK="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcflags}" \
	QMAKE_RPATH=

lrelease lang/*.ts

%{__make}

cd ../qca/plugins/qca-tls
./configure

qmake qca-tls.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_LINK="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcflags}" \
	QMAKE_RPATH=

%{__make}

cd ../qca-sasl

# This dir contains bad qcextra file, so prepare good one
sed -i \
	's,target.path=.*,target.path=%{_plugindir},' \
	qcextra

./configure

qmake qca-sasl.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_LINK="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcflags}" \
	QMAKE_RPATH=

%{__make}

cd ../../..

%install
rm -rf $RPM_BUILD_ROOT

export QTDIR=%{_prefix}

cd psi
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
cd ..

cd qca/plugins/qca-tls
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cd ../qca-sasl
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cd ../../..

install -d \
	$RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/designer \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

install psi/psi.desktop $RPM_BUILD_ROOT%{_desktopdir}
install psi/iconsets/system/default/icon_48.png $RPM_BUILD_ROOT%{_pixmapsdir}/psi.png
install psi/iconsets/roster/stellar-icq/online.png $RPM_BUILD_ROOT%{_pixmapsdir}/psi-stellar.png
install psi/lang/*.qm $RPM_BUILD_ROOT%{_datadir}/psi
install psi/indicator.png $RPM_BUILD_ROOT%{_datadir}/psi/iconsets/roster/default/indicator.png
install psi/libpsi/psiwidgets/*.so $RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/designer

rm $RPM_BUILD_ROOT%{_datadir}/psi/COPYING $RPM_BUILD_ROOT%{_datadir}/psi/README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc psi/README psi/TODO psi/README.rich-roster
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/psi
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

%files -n qt-designer-psiwidgets
%doc psi/libpsi/psiwidgets/README
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt/plugins-mt/designer/libpsiwidgets.so

%files -n qt-plugin-qca-tls
%defattr(644,root,root,755)
%doc qca/plugins/qca-tls/README
%attr(755,root,root) %{_plugindir}/libqca-tls.so

%files -n qt-plugin-qca-sasl
%defattr(644,root,root,755)
%doc qca/plugins/qca-sasl/README
%attr(755,root,root) %{_plugindir}/libqca-sasl.so
