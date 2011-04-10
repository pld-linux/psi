#
# TODO: - check BRs
#
# NOTE:
#
# To generate source package use generate-tarball.sh script included to this spec as SourceX.
# Requires: git-core, subversion and sed >= 4.0
#
%define		ver	0.15
%define		rev	3784
%define		rel	0.%{rev}.1
#
Summary:	PSI - Jabber client
Summary(de.UTF-8):	PSI - ein Instant Messaging Client-Programm für Jabber
Summary(pl.UTF-8):	PSI - klient Jabbera
Name:		psi
Version:	%{ver}.%{rev}
Release:	%{rel}
License:	GPL v2+ / LGPL v2.1+
Group:		Applications/Communications
Source0:	%{name}-%{version}.tar.xz
# Source0-md5:	576c2b20cc0748dbf9cae02f7bb69391
Source1:	%{name}-lang.tar.bz2
# Source1-md5:	cf6d82f53f1f1600a49bb61ba81151bf
Source2:	generate-tarball.sh
Patch0:		%{name}-fix_configure_for_ksh.patch
Patch1:		%{name}-home_etc.patch
Patch2:		%{name}-customos.patch
Patch3:		%{name}-no_online_offline_status.patch
Patch4:		%{name}-icon_buttons_big_return-mod.patch
Patch5:		%{name}-empty_group-fix.patch
URL:		http://code.google.com/p/psi-dev/
BuildRequires:	Qt3Support-devel
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtXml-devel
BuildRequires:	aspell-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel >= 0.9.7c
BuildRequires:	qca-devel >= 2.0.0
BuildRequires:	qt4-build >= 4.4.0
BuildRequires:	qt4-linguist >= 4.4.0
BuildRequires:	qt4-qmake >= 4.4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	which
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xorg-proto-scrnsaverproto-devel
BuildRequires:	xz >= 1:4.999.7
BuildRequires:	zlib-devel
Requires:	gstreamer-v4l2
Requires:	gstreamer-video4linux
Requires:	qt4-plugin-qca-ossl
Suggests:	gpgme >= 1.0.0
Obsoletes:	qt-designer-psiwidgets
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PSI is a communicator for the Jabber open messaging system. It is
based on the Qt library. It supports SSL encrypted connections. The
default behaviour for SSL was changed so that it looks for SSL
certificates in $DATADIR/certs or in ~/.psi/certs.

Psi+ is a development branch of Psi IM Jabber client.

%description -l de.UTF-8
Psi ist ein Instant Messaging (IM) Client-Programm für das
Jabber-Protokoll (XMPP), welches das Qt Toolkit nutzt.

%description -l pl.UTF-8
PSI jest komunikatorem dla otwartego systemu wiadomości Jabber. Został
stworzony w oparciu o bibliotekę Qt. PSI wspiera połączenia szyfrowane
SSL. W stosunku do domyślnego zachowania komunikatora została
wprowadzona zmiana, która powoduje, że certyfikaty SSL są poszukiwane
w katalogu $DATADIR/certs lub ~/.psi/certs.

Psi+ jest rozwojową gałęzią komunikatora Psi IM Jabber.

%prep
%setup -q -a 1
%patch0 -p0
#%%{?with_home_etc:%patch1 -p1}
%patch2 -p1
#%%patch3 -p1
%patch4 -p1
%patch5 -p1

rm -rf third-party

%build
./configure \
	--prefix=%{_prefix} \
	--datadir=%{_datadir} \
	--libdir=%{_libdir} \
	--no-separate-debug-info

%{__make}

cd lang
lrelease-qt4 *.ts

%install
rm -rf $RPM_BUILD_ROOT

export QTDIR=%{_libdir}/qt4

install -d $RPM_BUILD_ROOT%{_libdir}/psi/plugins

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cp -a lang/*.qm $RPM_BUILD_ROOT%{_datadir}/psi/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/psi-plus
%dir %{_datadir}/psi
%lang(ar) %{_datadir}/psi/*_ar.qm
%lang(ca) %{_datadir}/psi/*_ca.qm
%lang(cs) %{_datadir}/psi/*_cs.qm
%lang(da) %{_datadir}/psi/*_da.qm
%lang(de) %{_datadir}/psi/*_de.qm
%lang(el) %{_datadir}/psi/*_el.qm
%lang(eo) %{_datadir}/psi/*_eo.qm
%lang(es) %{_datadir}/psi/*_es.qm
%lang(fi) %{_datadir}/psi/*_fi.qm
%lang(fr) %{_datadir}/psi/*_fr.qm
%lang(it) %{_datadir}/psi/*_it.qm
%lang(jp) %{_datadir}/psi/*_jp.qm
%lang(mk) %{_datadir}/psi/*_mk.qm
%lang(nl) %{_datadir}/psi/*_nl.qm
%lang(pl) %{_datadir}/psi/*_pl.qm
%lang(pt_BR) %{_datadir}/psi/*_ptbr.qm
%lang(pt) %{_datadir}/psi/*_pt.qm
%lang(ru) %{_datadir}/psi/*_ru.qm
%lang(se) %{_datadir}/psi/*_se.qm
%lang(sk) %{_datadir}/psi/*_sk.qm
%lang(sr) %{_datadir}/psi/*_sr.qm
%lang(uk) %{_datadir}/psi/*_uk.qm
%lang(zh) %{_datadir}/psi/*_zh.qm
%dir %{_libdir}/psi
%dir %{_libdir}/psi/plugins
%{_datadir}/psi/certs
%{_datadir}/psi/iconsets
%{_datadir}/psi/sound
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/*.png
