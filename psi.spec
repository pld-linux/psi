#
# Conditional build:
%bcond_with	square_timestamps	# this is how they used to be
#
%define		_ver	2004-12-23
Summary:	PSI - Jabber client
Summary(pl):	PSI - klient Jabbera
Name:		psi
Version:	0.9.3
Release:	cvs.0.1
Epoch:		0
License:	GPL
Group:		Applications/Communications
Source0:	http://psi.affinix.com/files/cvs/%{name}-cvs-%{_ver}.tar.bz2	
# Source0-md5:	9c41fce07e8f7b5cea16ab9f5c825d23
Source1:	%{name}-richlistview.cpp
Source2:	%{name}-richlistview.h
Source3:	%{name}-roster-rich.README
Source4:	%{name}-indicator.png
Source10:	%{name}_de.qm
# Source10-md5:	c9799f489966a288b2f477ad4ea49ecf
Source11:	%{name}_fi.qm
# Source11-md5:	b203c264862d1dd9feaa0884b137c300
Source12:	%{name}_fr.qm
# Source12-md5:	f5029a111460a57d18e2d6f44975f9a8
Source13:	%{name}_nl.qm
# Source13-md5:	52927ee59a2a7fd9f94db154dde97451
Source14:	%{name}_pl.qm
# Source14-md5:	c0f39f92cf458d57e9dca7e28b943948
Source15:	%{name}_sk.qm
# Source15-md5: 539b37a7b94a07fce2a217e4197ede09
Source16:	%{name}_sw.qm
# Source16-md5:	49d98283f443a2d5e6473c5cf19e7690
Source17:	%{name}_zh.qm
# Source17-md5: 5b6245e14bcef3dc2c78c83bf61d719f
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
BuildRequires:	qca-devel
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

%description -l pl
PSI jest komunikatorem dla otwartego systemu wiadomo¶ci Jabber. Zosta³
stworzony w oparciu o bibliotekê Qt. PSI wspiera po³±czenia szyfrowane
SSL. W stosunku do domy¶lnego zachowania komunikatora zosta³a
wprowadzona zmiana, która powoduje ¿e certyfikaty SSL s± poszukiwane w
katalogu $DATADIR/certs lub ~/.psi/certs.

%prep
%setup -q -c %{name}-cvs-%{_ver}
cd %{name}-cvs-%{_ver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
#%patch4 -p1
#%patch5 -p1
#%patch6 -p1
%patch7 -p1
#%patch8 -p1
%patch9 -p1
#%patch10 -p1
%patch11 -p1
%patch12 -p1
%{?with_square_timestamps:%patch13 -p2}
%{__perl} -pi -e "s/QString PROG_VERSION = \"0.9.2\";/QString PROG_VERSION = \"0.9.2-%{release}\";/g" src/common.cpp
# %{__perl} -pi -e "s,/usr/local/share/psi,%{_datadir}/psi,g" src/common.cpp
# %{__perl} -pi -e 's/CONFIG \+= debug//g' src/src.pro

cp %{SOURCE1} src/richlistview.cpp
cp %{SOURCE2} src/richlistview.h
cp %{SOURCE3} README.rich-roster
cp %{SOURCE4} indicator.png

%build
export QTDIR=%{_prefix}
cd %{name}-cvs-%{_ver}
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
cd %{name}-cvs-%{_ver}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

install psi.desktop $RPM_BUILD_ROOT%{_desktopdir}
install iconsets/system/default/icon_48.png $RPM_BUILD_ROOT%{_pixmapsdir}/psi.png
install iconsets/roster/stellar-icq/online.png $RPM_BUILD_ROOT%{_pixmapsdir}/psi-stellar.png
install indicator.png $RPM_BUILD_ROOT%{_datadir}/psi/iconsets/roster/default/indicator.png

for i in %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16} %{SOURCE17}; do
	install $i $RPM_BUILD_ROOT%{_datadir}/psi/
done

#rm -rf $RPM_BUILD_ROOT%{_datadir}/psi/designer
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/COPYING $RPM_BUILD_ROOT%{_datadir}/%{name}/README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/psi
%{_datadir}/psi/certs
%{_datadir}/psi/iconsets
%{_datadir}/psi/sound
%lang(de) %{_datadir}/psi/psi_de.qm
%lang(fi) %{_datadir}/psi/psi_fi.qm
%lang(fr) %{_datadir}/psi/psi_fr.qm
%lang(nl) %{_datadir}/psi/psi_nl.qm
%lang(pl) %{_datadir}/psi/psi_pl.qm
%lang(sk) %{_datadir}/psi/psi_sk.qm
%lang(sw) %{_datadir}/psi/psi_sw.qm
%lang(zh) %{_datadir}/psi/psi_zh.qm
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
