Summary:	PSI Jabber client
Summary(pl):	Klient Jabbera
Name:		psi
Version:	0.8.6
Release:	1
License:	GPL
Group:		Applications/Communications
#Source0:	http://psi.affinix.com/%{name}-%{version}.tar.bz2
Source0:	%{name}-%{version}.tar.bz2
Patch0:		%{name}.pld.patch
URL:		http://psi.affinix.com/
BuildRequires:	qt-devel >= 3.0.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
Kadu is client of Gadu-Gadu protocol. It's an IM for Linux and UN*X.
It's written for KDE.

%description -l pl
Kadu jest klientem protko³u Gadu-Gadu. Inaczej mówi±c, jest
komunikatorem dla Linuksa (oraz, przy niewielkim wysi³ku, innych
systemów UN*Xowych). Napisano go w oparciu o bibliotekê Qt i KDE,
przeznaczony jest wiêc dla tego ¶rodowiska.

%prep
%setup -q

%build
QTDIR=%{_prefix}
export QTDIR
QMAKESPEC=%{_datadir}/qt/mkspecs/linux-g++
export QMAKESPEC

cd src
qmake psi.pro
patch -p0 < %{PATCH0}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d {$RPM_BUILD_ROOT%{_bindir},$RPM_BUILD_ROOT%{_datadir}/psi/{image,iconsets,sound}}

install src/psi $RPM_BUILD_ROOT%{_bindir}/

install image/*.png %{buildroot}%{_datadir}/psi/image
cp -r iconsets/* %{buildroot}%{_datadir}/psi/iconsets
install sound/* %{buildroot}%{_datadir}/psi/sound

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%attr(644,root,root) %{_datadir}/*
#%{_applnkdir}/Network/Communications/*.desktop
#%{_pixmapsdir}/*/*/apps/*.png
#%{_datadir}/apps/%{name}/msg.wav
#%{_datadir}/apps/%{name}/images/*
