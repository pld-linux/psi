# _without_qssl        - without ssl plugin
%define 	_qssl_version	1.0

Summary:	PSI Jabber client
Summary(pl):	PSI - klient Jabbera
Name:		psi
Version:	0.8.6
Release:	0.3
License:	GPL
Group:		Applications/Communications
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/psi/%{name}-%{version}.tar.bz2
Source1:        ftp://ftp.sourceforge.net/pub/sourceforge/psi/qssl-%{_qssl_version}.tar.bz2
Source2:	%{name}.desktop
Patch0:		%{name}-include.patch
Patch1:		%{name}-qssl-include.patch
Patch2:		%{name}-resourcesdir.patch
Patch3:		%{name}-plugin.patch
Patch4:		%{name}-certs.patch
URL:		http://psi.affinix.com/
BuildRequires:	qt-devel >= 3.0.5
%{?!_without_qssl:BuildRequires: openssl-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
%{?!_without_qssl:Requires: openssl}
%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
PSI Jabber client.

%description -l pl
PSI - klient Jabbera.

%prep
%setup -q -a 0
%if %{?_without_qssl:0}%{?!_without_qssl:1}
%setup -q -a 1
%endif
%patch0 -p1
%if %{?_without_qssl:0}%{?!_without_qssl:1}
%patch1 -p1
%endif
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
QTDIR=%{_prefix}
export QTDIR
QMAKESPEC=%{_datadir}/qt/mkspecs/linux-g++
export QMAKESPEC

cd src
qmake psi.pro
%{__make}

%if %{?_without_qssl:0}%{?!_without_qssl:1}
cd ../qssl-%{_qssl_version}
qmake qssl.pro
%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_datadir}/psi/{image,iconsets,sound} \
	$RPM_BUILD_ROOT%{_applnkdir}/Network/Communications

%if %{?_without_qssl:0}%{?!_without_qssl:1}
install -d $RPM_BUILD_ROOT%{_libdir}
%endif

install src/psi $RPM_BUILD_ROOT%{_bindir}/

install image/*.png $RPM_BUILD_ROOT%{_datadir}/psi/image
cp -r iconsets/* $RPM_BUILD_ROOT%{_datadir}/psi/iconsets
install sound/* $RPM_BUILD_ROOT%{_datadir}/psi/sound
install %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/Network/Communications

%if %{?_without_qssl:0}%{?!_without_qssl:1}
install qssl-%{_qssl_version}/libqssl.so %{buildroot}%{_libdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/*
%{?!_without_qssl:%{_libdir}/*}
%{_applnkdir}/Network/Communications/%{name}.desktop
