Summary:	PSI Jabber client
Summary(pl):	PSI - klient Jabbera
Name:		psi
Version:	0.8.7
Release:	0.1
License:	GPL
Group:		Applications/Communications
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/psi/%{name}-%{version}.tar.bz2
Source2:	%{name}.desktop
# Translation files ftom http://psi.sourceforge.net/
Source3:	%{name}_cz.ts
Source4:	%{name}_de.ts
Source5:	%{name}_es.ts
Source6:	%{name}_fr.ts
Source7:	%{name}_mk.ts
Source8:	%{name}_nl.ts
Source9:	%{name}_pl.ts
Source10:	%{name}_ru.ts
Patch0:		%{name}-include.patch
Patch1:		%{name}-plugin.patch
Patch2:		%{name}-certs.patch
URL:		http://psi.affinix.com/
BuildRequires:	qt-devel >= 3.0.5
%{?!_without_qssl:BuildRequires: openssl-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
%{?!_without_qssl:Requires: openssl}
%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
PSI is communicator for Jabber open messaging system. It is based on QT
library. It supports SSL encrypted connections. Default behaviour for
SSL was changed so it looks for SSL certificates in $DATADIR/certs or in
~/.psi/certs.

%description -l pl
PSI jest komunikatorem dla otwartego systemu wiadomo¶ci Jabber. Zosta³
stworzony w oparciu o bibliotekê QT. PSI wspiera po³±czenia szyfrowane SSL.
W stosunku do domy¶lnego zachowania komunikatora zosta³a wprowadzona zmiana,
która powoduje ¿e certyfikaty SSL poszukiwane s± w katalogu $DATADIR/certs
lub ~/.psi/certs.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1 -b .wiget
%patch2 -p1

%build
QTDIR=%{_prefix}
export QTDIR
QMAKESPEC=%{_datadir}/qt/mkspecs/linux-g++
export QMAKESPEC

./configure --prefix %{_prefix} --libdir %{_datadir}/psi --qtdir $QTDIR
make

cp %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} \
	%{SOURCE8} %{SOURCE9} %{SOURCE10} src
lrelease src/psi.pro

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_applnkdir}/Network/Communications \
	$RPM_BUILD_ROOT%{_libdir}/psi

make install INSTALL_ROOT=$RPM_BUILD_ROOT


install %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/Network/Communications

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/psi
%{_libdir}/psi
%{_applnkdir}/Network/Communications/%{name}.desktop
