#
# Conditional build:
%bcond_without	apidocs		# Doxygen based API documentation
%bcond_without	static_libs	# static library

Summary:	Handler library for evdev events
Summary(pl.UTF-8):	Biblioteka obsługująca zdarzenia evdev
Name:		libevdev
Version:	1.13.3
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://www.freedesktop.org/software/libevdev/%{name}-%{version}.tar.xz
# Source0-md5:	57ee77b7d4c480747e693779bb92fb84
URL:		https://www.freedesktop.org/wiki/Software/libevdev/
BuildRequires:	check-devel >= 0.9.9
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.4
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Handler library for evdev events.

%description -l pl.UTF-8
Biblioteka obsługująca zdarzenia evdev.

%package devel
Summary:	Header files for libevdev library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libevdev
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libevdev library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libevdev.

%package static
Summary:	Static libevdev library
Summary(pl.UTF-8):	Statyczna biblioteka libevdev
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libevdev library.

%description static -l pl.UTF-8
Statyczna biblioteka libevdev.

%package apidocs
Summary:	libevdev API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libevdev
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libevdev library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libevdev.

%prep
%setup -q

%{__rm} -r doc/html

%build
%configure \
	PYTHON=%{__python3} \
	--disable-silent-rules \
	%{__enable_disable static_libs static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config, no external dependencies
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libevdev.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_bindir}/libevdev-tweak-device
%attr(755,root,root) %{_bindir}/mouse-dpi-tool
%attr(755,root,root) %{_bindir}/touchpad-edge-detector
%attr(755,root,root) %{_libdir}/libevdev.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevdev.so.2
%{_mandir}/man1/libevdev-tweak-device.1*
%{_mandir}/man1/mouse-dpi-tool.1*
%{_mandir}/man1/touchpad-edge-detector.1*


%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libevdev.so
%{_includedir}/libevdev-1.0
%{_pkgconfigdir}/libevdev.pc
%{_mandir}/man3/libevdev.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libevdev.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/{*.css,*.html,*.js,*.png,search}
%endif
