%define 	_qssl_version	1.0

Summary:	PSI Jabber client
Summary(pl):	PSI - klient Jabbera
Name:		psi
Version:	0.8.6
Release:	2
License:	GPL
Group:		Applications/Communications
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/psi/%{name}-%{version}.tar.bz2
Source1:        ftp://ftp.sourceforge.net/pub/sourceforge/psi/qssl-%{_qssl_version}.tar.bz2
Patch0:		%{name}-pld.patch
Patch1:		%{name}-qssl.patch
Patch2:		%{name}-plugin.patch
URL:		http://psi.affinix.com/
BuildRequires:	qt-devel >= 3.0.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
PSI Jabber client.

%description -l pl
PSI - klient Jabbera.

%prep
%setup -q

%build
QTDIR=%{_prefix}
export QTDIR
QMAKESPEC=%{_datadir}/qt/mkspecs/linux-g++
export QMAKESPEC

cd src
qmake psi.pro
%patch0 -p0
%patch2 -p0
%{__make}

bzip2 -dc %{SOURCE1}|tar x
cd qssl-%{_qssl_version}
qmake qssl.pro
%patch1 -p2
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d {$RPM_BUILD_ROOT%{_bindir},$RPM_BUILD_ROOT%{_datadir}/psi/{image,iconsets,sound}}
install -d $RPM_BUILD_ROOT%{_libdir}
install src/psi $RPM_BUILD_ROOT%{_bindir}/

install image/*.png %{buildroot}%{_datadir}/psi/image
cp -r iconsets/* %{buildroot}%{_datadir}/psi/iconsets
install sound/* %{buildroot}%{_datadir}/psi/sound
install qssl-%{_qssl_version}/libqssl.so %{buildroot}%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%attr(644,root,root) %{_datadir}/*
%attr(644,root,root) %{_libdir}/*
#%{_applnkdir}/Network/Communications/*.desktop
#%{_pixmapsdir}/*/*/apps/*.png
#%{_datadir}/apps/%{name}/msg.wav
#%{_datadir}/apps/%{name}/images/*
