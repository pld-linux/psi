Summary:	PSI - Jabber client
Summary(pl):	PSI - klient Jabbera
Name:		psi
Version:	0.9.3
Release:	0.1
License:	GPL
Group:		Applications/Communications
Source0:	http://osdn.dl.sourceforge.net/psi/%{name}-%{version}.tar.bz2
# Source0-md5:	d20f3bb530235a246bc2d92308089744
Source1:	%{name}-richlistview.cpp
Source2:	%{name}-richlistview.h
Source3:	%{name}-roster-rich.README
Source4:	%{name}-indicator.png
Source10:	%{name}_ee.qm
# Source10-md5:	9747ae62d0401b65ccea3531bdc148e0
Source11:	%{name}_es.qm
# Source11-md5:	125353103949ff1de2bc31b6bcfdf489
Source12:	%{name}_fr.qm
# Source12-md5:	2109223681611cd89b1a348bb87ab143
Source13:	%{name}_mk.qm
# Source13-md5:	2fbdee2069447e31982fffed14bbd5fa
Source14:	%{name}_nl.qm
# Source14-md5:	31048975699e64f9e6dc4213714b0e0d
Source15:	%{name}_pl.qm
# Source15-md5:	fbafd2e4002eb84c728cd9e701e73e0c
Source16:	%{name}_ru.qm
# Source16-md5:	1b82151552f658e9b94ed6bb4537628d
Source17:	%{name}_vi.qm
# Source17-md5:	4d66fd44e634f2d5a7118c2c149c6614
Source18:	%{name}_zh.qm
# Source18-md5:	76dc27b07962e8e61b57f53e7c5b2a0d
#	from PLD
Patch0:		%{name}-certs.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-home_etc.patch
Patch3:		%{name}-timestamps.patch
#	from jpc
Patch10:	%{name}-customos.patch
#	from SKaZi
Patch20:        %{name}-status_indicator-add.patch
Patch21:        %{name}-no_online_status-mod.patch
Patch22:	%{name}-no_default_status_text-mod.patch
Patch23:        %{name}-status_history-add.patch
Patch24:	%{name}-offline_status-add.patch
Patch25:        %{name}-icon_buttons_big_return-mod.patch
Patch26:        %{name}-nicechats-mod.patch
Patch27:        %{name}-roster-rich.patch
Patch28:        %{name}-icondef.xml_status_indicator.patch
Patch29:        %{name}-settoggles-fix.patch
Patch30:        %{name}-wrong_mainwin_pos_gnome-fix.patch
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
%setup -q
#	PLD
%patch0 -p1
%patch1 -p1
%patch2 -p1
#	jpc
%patch10 -p1
#	SKaZi
#%patch20 -p1
%patch21 -p1
#%patch22 -p1
%patch23 -p1
#%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
#%patch28 -p1
%patch29 -p1
%patch30 -p1

%{__perl} -pi -e "s/QString PROG_VERSION = \"0.9.3\";/QString PROG_VERSION = \"0.9.3-%{release}\";/g" src/common.cpp
# %{__perl} -pi -e "s,/usr/local/share/psi,%{_datadir}/psi,g" src/common.cpp
# %{__perl} -pi -e 's/CONFIG \+= debug//g' src/src.pro

cp %{SOURCE1} src/richlistview.cpp
cp %{SOURCE2} src/richlistview.h
cp %{SOURCE3} README.rich-roster
cp %{SOURCE4} indicator.png

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

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

install psi.desktop $RPM_BUILD_ROOT%{_desktopdir}
install iconsets/system/default/icon_48.png $RPM_BUILD_ROOT%{_pixmapsdir}/psi.png
install iconsets/roster/stellar-icq/online.png $RPM_BUILD_ROOT%{_pixmapsdir}/psi-stellar.png
install indicator.png $RPM_BUILD_ROOT%{_datadir}/psi/iconsets/roster/default/indicator.png

for i in %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16} %{SOURCE17} %{SOURCE18}; do
	install $i $RPM_BUILD_ROOT%{_datadir}/psi/
done

#rm -rf $RPM_BUILD_ROOT%{_datadir}/psi/designer
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
%lang(et) %{_datadir}/psi/psi_ee.qm
%lang(es) %{_datadir}/psi/psi_es.qm
%lang(fr) %{_datadir}/psi/psi_fr.qm
%lang(mk) %{_datadir}/psi/psi_mk.qm
%lang(nl) %{_datadir}/psi/psi_nl.qm
%lang(pl) %{_datadir}/psi/psi_pl.qm
%lang(ru) %{_datadir}/psi/psi_ru.qm
%lang(vi) %{_datadir}/psi/psi_vi.qm
%lang(zh) %{_datadir}/psi/psi_zh.qm
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
