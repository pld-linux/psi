#
# TODO:
# - fix:
#   - contact_icons_at_top.patch
#   - custom_settings_per_contact.patch
#
# Conditional build:
%bcond_without	external_patches	# only apply basic patches
					# WARNING: will remove many added features
#
%define		pre test2
%define         pld_rel 1
#
Summary:	PSI - Jabber client
Summary(pl):	PSI - klient Jabbera
Name:		psi
Version:	0.10
%define		rel %{pre}.%{pld_rel}%{?with_external_patches:patched}
Release:	0.%{rel}
License:	GPL
Group:		Applications/Communications
#Source0:	%{name}-snap-%{pre}.tar.bz2
Source0:	http://dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}-%{pre}.tar.bz2
# Source0-md5:	9f1e556e83a9927eb4ad2fefb5b224ef
Source1:	%{name}-richlistview.cpp
Source2:	%{name}-richlistview.h
Source3:	%{name}-roster-rich.README
Source4:	%{name}-indicator.png
Source5:	%{name}-lang-0.9.3.tar.bz2
# Source5-md5:	bb4f609553bb9f1c9b140294203f9ed9
#       from PLD
Patch0:		%{name}-certs.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-home_etc.patch
Patch3:		%{name}-nodebug.patch
#       from jpc
Patch10:	%{name}-customos.patch
#       from SKaZi (downlaoded on 2005-09-07 00:10)
Patch20:	%{name}-status_indicator-add.patch
Patch22:	%{name}-no_online_status-mod.patch
Patch23:	%{name}-status_history-add.patch
Patch24:	%{name}-icon_buttons_big_return-mod.patch
Patch25:	%{name}-nicechats-mod.patch
Patch26:	%{name}-roster-rich.patch
Patch27:	%{name}-icondef.xml_status_indicator.patch
Patch28:	%{name}-settoggles-fix.patch
Patch29:	%{name}-empty_group-fix.patch
#       from Remko Troncon:
# http://www.cs.kuleuven.ac.be/~remko/psi/rc/ (downloaded on 2005-09-07 00:15)
Patch100:	%{name}-adhoc_and_rc.patch
# http://www.cs.kuleuven.ac.be/~remko/psi/ (downloaded on 2005-02-02 22:00)
Patch101:	%{name}-rosteritems_iris.patch
Patch102:	%{name}-rosteritems_psi.patch
#       from Machekku:
# http://machekku.uaznia.net/jabber/psi/patches/ (downloaded on 2005-01-27 15:30)
Patch300:	%{name}-contact_icons_at_top.patch
Patch301:	%{name}-enable_thread_in_messages.patch
#	from Yves Goergen:
# http://home.unclassified.de/psi.php
Patch400:	%{name}-custom_settings_per_contact.patch
#	from Darcs repo:
Patch500:	%{name}-ui_about-includes.patch
URL:		http://psi.affinix.com/
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

%description -l pl
Psi jest komunikatorem dla otwartego systemu wiadomo�ci Jabber. Zosta�
stworzony w oparciu o bibliotek� Qt. Psi wspiera po��czenia szyfrowane
SSL. W stosunku do domy�lnego zachowania komunikatora zosta�a
wprowadzona zmiana, kt�ra powoduje �e certyfikaty SSL s� poszukiwane w
katalogu $DATADIR/certs lub ~/.psi/certs.

Jest to wersja rozwojowa (CVS) z wieloma dodatkowymi �atkami. Zobacz:
http://www.pld-linux.org/Packages/Psi

%package -n qt-designer-psiwidgets
Summary:	Psi widgets collection for Qt Designer
Summary(pl):	Kolekcja widget�w Psi do wykorzystania w Projektancie Qt
License:	GPL v2
Group:		X11/Development/Libraries

%description -n qt-designer-psiwidgets
This is a package of widgets, that are used in Psi You may be
interested in it, if you want to develop custom dialogs, or hack
existing ones.

%description -n qt-designer-psiwidgets -l pl
Pakiet ten zawiera wtyczke dla programu Qt Designer, bed�c� zbiorem
widget�w u�ytych w programie Psi. Moze Ci si� przyda�, jesli chcia�by�
napisa� w�asne okna dialogowe itp. albo poprawi� obecne.

%prep
%setup -q -n %{name}-%{version}-%{pre}
%setup -q -D -a 5 -n %{name}-%{version}-%{pre}
#       PLD:
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p2
#       jpc:
%patch10 -p1
%if %{with external_patches}
#       SKaZi:
%patch20 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
cp %{SOURCE1} src/richlistview.cpp
cp %{SOURCE2} src/richlistview.h
cp %{SOURCE3} README.rich-roster
#       Remko Troncon:
%patch100 -p2
cd iris
%patch101 -p0
cd ..
%patch102 -p0
#	from Machekku:
#patch300 -p2
%patch301 -p1
%endif
# 	from Yves:
#patch400 -p2
#	from Darcs:
%patch500 -p1

sed -i \
	's/QString PROG_VERSION = .*/QString PROG_VERSION = "PLD %{version}-%{rel}";/g' \
	src/common.cpp
sed -i \
	"s,/usr/local/share/psi,%{_datadir}/psi,g" \
	src/common.cpp

%build
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
install lang/*.qm $RPM_BUILD_ROOT%{_datadir}/psi
%if %{with external_patches}
install %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/psi/iconsets/roster/default/indicator.png
%endif
install libpsi/psiwidgets/*.so $RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/designer

rm -rf $RPM_BUILD_ROOT%{_datadir}/psi/COPYING $RPM_BUILD_ROOT%{_datadir}/psi/README
rm -rf $RPM_BUILD_ROOT%{_datadir}/psi/designer

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO %{?with_external_patches:README.rich-roster} ChangeLog
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/psi
%{_datadir}/psi/certs
%{_datadir}/psi/iconsets
%{_datadir}/psi/sound
%lang(cs) %{_datadir}/psi/psi_cs.qm
%lang(de) %{_datadir}/psi/psi_de.qm
%lang(el) %{_datadir}/psi/psi_el.qm
%lang(eo) %{_datadir}/psi/psi_eo.qm
%lang(es) %{_datadir}/psi/psi_es.qm
%lang(et) %{_datadir}/psi/psi_et.qm
%lang(fr) %{_datadir}/psi/psi_fr.qm
%lang(hr) %{_datadir}/psi/psi_hr.qm
%lang(mk) %{_datadir}/psi/psi_mk.qm
%lang(nl) %{_datadir}/psi/psi_nl.qm
%lang(pl) %{_datadir}/psi/psi_pl.qm
%lang(ptbr) %{_datadir}/psi/psi_pt_br_0.9.3b.qm
%lang(ru) %{_datadir}/psi/psi_ru.qm
%lang(sk) %{_datadir}/psi/psi_sk.qm
%lang(sl) %{_datadir}/psi/psi_sl.qm
%lang(sr) %{_datadir}/psi/psi_sr.qm
%lang(vi) %{_datadir}/psi/psi_vi.qm
%lang(zh) %{_datadir}/psi/psi_zh.qm
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png

%files -n qt-designer-psiwidgets
%defattr(644,root,root,755)
%doc libpsi/psiwidgets/README
%attr(755,root,root) %{_libdir}/qt/plugins-mt/designer/libpsiwidgets.so
