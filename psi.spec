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
Patch0:		%{name}-include.patch
Patch1:		%{name}-qssl-include.patch
Patch2:		%{name}-plugin.patch
Patch3:		%{name}-test.patch
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
%setup -q -a 1
%patch0 -p1
%patch1 -p1
%patch3 -p1

%build
QTDIR=%{_prefix}
export QTDIR
QMAKESPEC=%{_datadir}/qt/mkspecs/linux-g++
export QMAKESPEC

cd src
qmake psi.pro
patch -p0 < %{PATCH0}

%if %{?_without_qssl:0}%{?!_without_qssl:1}
patch -p0 < %{PATCH2}
%endif

%{__make}

%if %{?_without_qssl:0}%{?!_without_qssl:1}
bzip2 -dc %{SOURCE1}|tar x
cd qssl-%{_qssl_version}
qmake qssl.pro
patch -p0 < %{PATCH1}
%{__make}

%endif
%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/psi/{image,iconsets,sound}}
%if %{?_without_qssl:0}%{?!_without_qssl:1}
install -d $RPM_BUILD_ROOT%{_libdir}
%endif
install src/psi $RPM_BUILD_ROOT%{_bindir}/

install image/*.png %{buildroot}%{_datadir}/psi/image
cp -r iconsets/* %{buildroot}%{_datadir}/psi/iconsets
install sound/* %{buildroot}%{_datadir}/psi/sound

%if %{?_without_qssl:0}%{?!_without_qssl:1}
install src/qssl-%{_qssl_version}/libqssl.so %{buildroot}%{_libdir}
%endif
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/*
%{?!_without_qssl:%{_libdir}/*}
#%{_applnkdir}/Network/Communications/*.desktop
#%{_pixmapsdir}/*/*/apps/*.png
#%{_datadir}/apps/%{name}/msg.wav
#%{_datadir}/apps/%{name}/images/*
