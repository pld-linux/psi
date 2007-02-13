#
# Conditional build:
%bcond_without	home_etc		# Disable the HOME_ETC patch
#
Summary:	PSI - Jabber client
Summary(de.UTF-8):	PSI - ein Instant Messaging Client-Programm für das Jabber
Summary(pl.UTF-8):	PSI - klient Jabbera
Name:		psi
Version:	0.10
Release:	2
License:	GPL v2
Group:		Applications/Communications
Source0:	http://dl.sourceforge.net/psi/%{name}-%{version}.tar.bz2
# Source0-md5:	f0fd4ccf077f7b24e236f71c22649b7b
Source1:	%{name}-richlistview.cpp
Source2:	%{name}-richlistview.h
Source3:	%{name}-roster-rich.README
Source4:	%{name}-indicator.png
Source10:	%{name}-lang-%{version}.tar.bz2
# Source10-md5:	cc949f271e204aec96b9cf90d3e88f0f

#	from PLD
Patch0:		%{name}-certs.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-home_etc.patch
Patch3:		%{name}-qca_nolink_fix.patch
Patch4:		%{name}-fix_configure_for_ksh.patch
#	from jpc
Patch10:	%{name}-customos.patch
#	from SKaZi
Patch20:	%{name}-status_indicator-add.patch
Patch21:	%{name}-no_online_status-mod.patch
Patch22:	%{name}-status_history-add.patch
Patch23:	%{name}-icon_buttons_big_return-mod.patch
Patch24:	%{name}-roster-rich.patch
Patch25:	%{name}-icondef.xml_status_indicator.patch
Patch26:	%{name}-settoggles-fix.patch
Patch27:	%{name}-empty_group-fix.patch
#	from Hawk
Patch30:	%{name}-appearance-mod.patch
URL:		http://psi-im.org/
BuildRequires:	cyrus-sasl-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel >= 0.9.7c
BuildRequires:	qca-devel >= 1.0
BuildRequires:	qmake
BuildRequires:	qt-devel >= 3.3.2-5
BuildRequires:	qt-linguist
Requires:	qt-plugin-qca-tls >= 1:1.0
Conflicts:	qt-plugin-ssl = 1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PSI is a communicator for the Jabber open messaging system. It is
based on the Qt library. It supports SSL encrypted connections. The
default behaviour for SSL was changed so that it looks for SSL
certificates in $DATADIR/certs or in ~/.psi/certs.

%description -l de.UTF-8
Psi ist ein Instant Messaging (IM) Client-Programm für das Jabber
(XMPP) Protokoll, welches das Qt Toolkit nutzt.

%description -l pl.UTF-8
PSI jest komunikatorem dla otwartego systemu wiadomości Jabber. Został
stworzony w oparciu o bibliotekę Qt. PSI wspiera połączenia szyfrowane
SSL. W stosunku do domyślnego zachowania komunikatora została
wprowadzona zmiana, która powoduje że certyfikaty SSL są poszukiwane w
katalogu $DATADIR/certs lub ~/.psi/certs.

%package -n qt-designer-psiwidgets
Summary:	Psi widgets collection for Qt Designer
Summary(pl.UTF-8):	Kolekcja widgetów Psi do wykorzystania w Projektancie Qt
License:	GPL v2
Group:		X11/Development/Libraries

%description -n qt-designer-psiwidgets
This is a package of widgets, that are used in Psi You may be
interested in it, if you want to develop custom dialogs, or hack
existing ones.

%description -n qt-designer-psiwidgets -l pl.UTF-8
Pakiet ten zawiera wtyczkę dla programu Qt Designer będącą zbiorem
widgetów użytych w programie Psi. Może się przydać tym, którzy
chcieliby napisać własne okna dialogowe albo poprawić obecne.

%prep
%setup -q
#	PLD
%patch0 -p1
%patch1 -p1
%{?with_home_etc:%patch2 -p1}
%patch3 -p1
%patch4 -p0
#	jpc
%patch10 -p1
#	SKaZi
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
#	Hawk
%patch30 -p1

%{__perl} -pi -e "s,/usr/local/share/psi,%{_datadir}/psi,g" src/common.cpp
%{__perl} -pi -e 's/CONFIG \+= debug//g' src/src.pro

cp %{SOURCE1} src/richlistview.cpp
cp %{SOURCE2} src/richlistview.h
cp %{SOURCE3} README.rich-roster
cp %{SOURCE4} indicator.png
tar -jxf %{SOURCE10}

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
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}} \
	$RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/designer

install psi.desktop $RPM_BUILD_ROOT%{_desktopdir}
install iconsets/system/default/icon_48.png $RPM_BUILD_ROOT%{_pixmapsdir}/psi.png
install indicator.png $RPM_BUILD_ROOT%{_datadir}/psi/iconsets/roster/default/indicator.png
install libpsi/psiwidgets/*.so $RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/designer
install *.qm $RPM_BUILD_ROOT%{_datadir}/psi

rm -rf $RPM_BUILD_ROOT%{_datadir}/psi/designer
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/COPYING $RPM_BUILD_ROOT%{_datadir}/%{name}/README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README README.rich-roster TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/psi
%{_datadir}/psi/certs
%{_datadir}/psi/iconsets
%{_datadir}/psi/sound
%lang(bg) %{_datadir}/psi/psi_bg.qm
%lang(eo) %{_datadir}/psi/psi_eo.qm
%lang(es) %{_datadir}/psi/psi_es.qm
%lang(fr) %{_datadir}/psi/psi_fr.qm
%lang(hu) %{_datadir}/psi/psi_hu.qm
%lang(mk) %{_datadir}/psi/psi_mk.qm
%lang(nl) %{_datadir}/psi/psi_nl.qm
%lang(pl) %{_datadir}/psi/psi_pl.qm
%lang(pt_BR) %{_datadir}/psi/psi_pt_BR.qm
%lang(sk) %{_datadir}/psi/psi_sk.qm
%lang(sl) %{_datadir}/psi/psi_sl.qm
%lang(vi) %{_datadir}/psi/psi_vi.qm
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png

%files -n qt-designer-psiwidgets
%defattr(644,root,root,755)
%doc libpsi/psiwidgets/README
%attr(755,root,root) %{_libdir}/qt/plugins-mt/designer/libpsiwidgets.so
