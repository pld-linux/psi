%define		snap 20051124
%define		_snap 2005-11-24
%define		_datasnap 2005-11-23
#
Summary:	PSI - Jabber client
Summary(de):    PSI - ein Instant Messaging Client-Programm für das Jabber
Summary(pl):	PSI - klient Jabbera
Name:		psi
Version:	0.10
Release:	0.%{snap}.1pedrito
License:	GPL
Group:		Applications/Communications
Source0:	http://www.radioemiter.pl/~pedrito/public/jabber/psi-pedrito/%{_snap}/%{name}-pedrito-%{_snap}.tar.bz2
# Source0-md5:	51ab430aa36354cdca415ebb7c49f2d6
Source1:	http://www.radioemiter.pl/~pedrito/public/jabber/psi-pedrito/%{_datasnap}/%{name}-pedrito-%{_datasnap}-data.tar.bz2
# Source1-md5:	1398b12cef53fb7c9934c83bd9a1609a
#Source2:	%{name}-snap-lang-20041209.tar.bz2
# Source2-md5:	38f0894bf1b557a36788213c56797e62
Source3:	http://michalj.alternatywa.info/psi/patches/emergency.png
# Source3-md5:	5fa629c5177a7b1c5090428e22b7ec30
Patch0:		%{name}-customos.patch
Patch1:		%{name}-desktop.patch
URL:		http://psi-pedrito.go.pl/
BuildRequires:	libstdc++-devel
BuildRequires:	cyrus-sasl-devel
BuildRequires:	openssl-devel >= 0.9.7c
BuildRequires:	qca-devel >= 1.0
BuildRequires:	qmake
BuildRequires:	qt-devel >= 3.3.2-5
BuildRequires:	qt-linguist
Requires:	qt-plugin-qca-tls >= 1:1.0
Conflicts:	qt-plugin-ssl = 1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir %{_libdir}/qt/plugins-mt/crypto

%description
Psi is a communicator for the Jabber open messaging system. It is
based on the Qt library. It supports SSL encrypted connections. The
default behaviour for SSL was changed so that it looks for SSL
certificates in $DATADIR/certs or in ~/.psi/certs.

This is a development version (CVS) with many additional patches. See:
http://www.pld-linux.org/Packages/Psi

%description -l de
Psi ist ein Instant Messaging (IM) Client-Programm für das Jabber
(XMPP) Protokoll, welches das Qt Toolkit nutzt.

%description -l pl
Psi jest komunikatorem dla otwartego systemu wiadomo¶ci Jabber. Zosta³
stworzony w oparciu o bibliotekê Qt. Psi wspiera po³±czenia szyfrowane
SSL. W stosunku do domy¶lnego zachowania komunikatora zosta³a
wprowadzona zmiana, która powoduje ¿e certyfikaty SSL s± poszukiwane w
katalogu $DATADIR/certs lub ~/.psi/certs.

Jest to wersja rozwojowa (CVS) z wieloma dodatkowymi ³atkami. Zobacz:
http://www.pld-linux.org/Packages/Psi

%package -n qt-designer-psiwidgets
Summary:	Psi widgets collection for Qt Designer
Summary(pl):	Kolekcja widgetów Psi do wykorzystania w Projektancie Qt
License:	GPL v2
Group:		X11/Development/Libraries

%description -n qt-designer-psiwidgets
This is a package of widgets, that are used in Psi You may be
interested in it, if you want to develop custom dialogs, or hack
existing ones.

%description -n qt-designer-psiwidgets -l pl
Pakiet ten zawiera wtyczke dla programu Qt Designer, bed±c± zbiorem
widgetów u¿ytych w programie Psi. Moze Ci siê przydaæ, jesli chcia³by¶
napisaæ w³asne okna dialogowe itp. albo poprawiæ obecne.

%prep
%setup -q -n %{name}-pedrito-%{_snap}
%patch0 -p1
#%patch1 -p0

%{__tar} jxf %{SOURCE1}
cd psi-pedrito-%{_datasnap}-data
cp -r * ..
cd ..

rm -rf `find . -type d -name CVS`

%build
export QTDIR=%{_prefix}

./configure \
	--prefix=%{_prefix}

qmake psi.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_LINK="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcflags}" \
	QMAKE_RPATH=

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

export QTDIR=%{_prefix}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/designer \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

install psi.desktop $RPM_BUILD_ROOT%{_desktopdir}
install iconsets/system/default/icon_48.png $RPM_BUILD_ROOT%{_pixmapsdir}/psi.png
install iconsets/roster/stellar-icq/online.png $RPM_BUILD_ROOT%{_pixmapsdir}/psi-stellar.png
install psi/lang/*.qm $RPM_BUILD_ROOT%{_datadir}/psi
install *.qm $RPM_BUILD_ROOT%{_datadir}/psi
install %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/psi/iconsets/system/default/
install libpsi/psiwidgets/*.so $RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/designer

rm -rf $RPM_BUILD_ROOT%{_datadir}/psi/COPYING $RPM_BUILD_ROOT%{_datadir}/psi/README
rm -rf $RPM_BUILD_ROOT%{_datadir}/psi/designer

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO ChangeLog psi-pedrito.txt
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
%defattr(644,root,root,755)
%doc libpsi/psiwidgets/README
%attr(755,root,root) %{_libdir}/qt/plugins-mt/designer/libpsiwidgets.so
