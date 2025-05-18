Summary:	ISpell spell checker library
Summary(pl.UTF-8):	Biblioteka sprawdzania pisowni ISpell
Name:		bc-ispell
Version:	0
%define	gitref	05574fe160222c3d0b6283c1433c9b087271fad1
%define	snap	20231108
Release:	0.%{snap}.1
License:	LGPL v2+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/bcunit/tags
Source0:	https://gitlab.linphone.org/BC/public/external/ispell/-/archive/%{gitref}/ispell-%{snap}.tar.bz2
# Source0-md5:	0a56f85ccfbfffad109d98e38ab27063
Patch0:		ispell-config.patch
Patch1:		ispell-cmake.patch
URL:		https://gitlab.linphone.org/BC/public/external/ispell
BuildRequires:	cmake >= 3.16
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ISpell spell checker library.

%description -l pl.UTF-8
Biblioteka sprawdzania pisowni ISpell.

%package devel
Summary:	Header files for ISpell library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ISpell
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for ISpell library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ISpell.

%prep
%setup -q -n ispell-%{gitref}
%patch -P0 -p1
%patch -P1 -p1

%{__sed} -i -e 's,/lib/,/%{_lib}/,' local.h.linux

%build
%cmake -B build \
	-DENABLE_BCUNIT_AUTOMATED=ON \
	-DENABLE_BCUNIT_BASIC=ON \
	-DENABLE_BCUNIT_CONSOLE=ON \
	-DENABLE_BCUNIT_CURSES=ON \
	-DENABLE_BCUNIT_DOC=ON \
	-DENABLE_BCUNIT_EXAMPLES=ON

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ispell

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_includedir}/ISpell
cp -p config.h defhash.h ispell.h libispell.h local.h $RPM_BUILD_ROOT%{_includedir}/ISpell

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES README WISHES
%attr(755,root,root) %{_libdir}/libISpell.so
# for dictionaries, shared with ispell
%dir %{_libdir}/ispell

%files devel
%defattr(644,root,root,755)
%{_includedir}/ISpell
%{_datadir}/cmake/ISpell
