#
# Conditional build:
%bcond_with	apidocs		# API documentation [doesn't build up to 0.8.0 release]
%bcond_without	static_libs	# static library
#
Summary:	GXml - GObject API that wraps around libxml2
Summary(pl.UTF-8):	GXml - API GObject obudowujące libxml2
Name:		gxml
Version:	0.8.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gxml/0.8/%{name}-%{version}.tar.xz
# Source0-md5:	77af0fb4e1e178b60fc898b8beeaabfe
URL:		https://github.com/GNOME/gxml
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.11
BuildRequires:	gettext-tools >= 0.18.1
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gobject-introspection-devel >= 1.32.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libgee-devel >= 0.10.5
BuildRequires:	libtool >= 2:2
BuildRequires:	libxml2-devel >= 1:2.7
BuildRequires:	pkgconfig >= 1:0.21
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.26
%{?with_apidocs:BuildRequires:	valadoc >= 0.3.1}
BuildRequires:	yelp-tools
BuildRequires:	xz
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
Requires:	libgee-devel >= 0.10.5
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
Requires:	vala >= 2:0.26
Requires:	vala-libgee >= 0.10.5

%description -n vala-gxml
Vala API for GXml library.

%description -n vala-gxml -l pl.UTF-8
API języka Vala dla biblioteki GXml.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gi-system-install \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	%{?with_apidocs:--enable-docs --enable-gtk-docs --enable-valadoc}
# --enable-gir-docs --enable-devhelp-docs ???
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgxml-0.6.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc

%find_lang GXml

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f GXml.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libgxml-0.6.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgxml-0.6.so.8
%{_libdir}/girepository-1.0/GXml-0.6.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgxml-0.6.so
%{_includedir}/gxml-0.6
%{_datadir}/gir-1.0/GXml-0.6.gir
%{_pkgconfigdir}/gxml-0.6.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgxml-0.6.a
%endif

%files -n vala-gxml
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gxml-0.6.deps
%{_datadir}/vala/vapi/gxml-0.6.vapi
