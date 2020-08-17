#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library

Summary:	GXml - GObject API that wraps around libxml2
Summary(pl.UTF-8):	GXml - API GObject obudowujące libxml2
Name:		gxml
Version:	0.20.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gxml/0.20/%{name}-%{version}.tar.xz
# Source0-md5:	6ee8f2e8f555a76de87cc293dee2106a
URL:		https://wiki.gnome.org/GXml
BuildRequires:	gettext-tools >= 0.18.1
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gobject-introspection-devel >= 1.32.0
BuildRequires:	libgee-devel >= 0.18.0
BuildRequires:	libxml2-devel >= 1:2.7
BuildRequires:	meson
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.21
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.34.7
%{?with_apidocs:BuildRequires:	valadoc >= 0.30}
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	glib2 >= 1:2.32.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GXml is a GObject API that wraps around libxml2.

%description -l pl.UTF-8
GXml to API GObject obudowujące libxml2.

%package devel
Summary:	Header files for GXml library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GXml
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.32.0
Requires:	libgee-devel >= 0.18.0
Requires:	libxml2-devel >= 1:2.7

%description devel
Header files for GXml library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GXml.

%package static
Summary:	Static GXml library
Summary(pl.UTF-8):	Statyczna biblioteka GXml
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GXml library.

%description static -l pl.UTF-8
Statyczna biblioteka GXml.

%package -n vala-gxml
Summary:	Vala API for GXml library
Summary(pl.UTF-8):	API języka Vala dla biblioteki GXml
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.34.7
Requires:	vala-libgee >= 0.18.0
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description -n vala-gxml
Vala API for GXml library.

%description -n vala-gxml -l pl.UTF-8
API języka Vala dla biblioteki GXml.

%package apidocs
Summary:	API documentation for GXml library
Summary(pl.UTF-8):	Dokumentacja API biblioteki GXml
Group:		Documentation

%description apidocs
API documentation for GXml library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GXml.

%prep
%setup -q

%build
%if %{with static_libs}
%meson build-static \
	--default-library=static \
	-Ddocs=false

%ninja_build -C build-static
%endif

%meson build \
	--default-library=shared \
	%{!?with_apidocs:-Ddocs=false}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%ninja_install -C build-static
%endif

%ninja_install -C build

%find_lang GXml-0.20

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f GXml-0.20.lang
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README
%attr(755,root,root) %{_libdir}/libgxml-0.20.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgxml-0.20.so.2
%{_libdir}/girepository-1.0/GXml-0.20.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgxml-0.20.so
%{_includedir}/gxml-0.20
%{_datadir}/gir-1.0/GXml-0.20.gir
%{_pkgconfigdir}/gxml-0.20.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgxml-0.20.a
%endif

%files -n vala-gxml
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gxml-0.20.deps
%{_datadir}/vala/vapi/gxml-0.20.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_datadir}/devhelp/books/GXml-0.20
%endif
