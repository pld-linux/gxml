#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library

Summary:	GXml - GObject API that wraps around libxml2
Summary(pl.UTF-8):	GXml - API GObject obudowujące libxml2
Name:		gxml
Version:	0.14.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gxml/0.14/%{name}-%{version}.tar.xz
# Source0-md5:	70577a8d4c6610ed8cfda9a24e54c3b0
Patch0:		%{name}-missing.patch
Patch1:		%{name}-normalize.patch
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
%if "%{_rpmversion}" >= "5"
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
%patch0 -p1
%patch1 -p1

# missing file (or missing in makefile rules)
install -d docs/valadoc/gtk-doc/gtk-doc/gxml/xml
cat >>docs/valadoc/gtk-doc/gtk-doc/gxml/xml/gtkdocentities.ent <<EOF
<!ENTITY package "gxml">
<!ENTITY package_bugreport "">
<!ENTITY package_name "gxml">
<!ENTITY package_string "gxml %{version}">
<!ENTITY package_tarname "gxml">
<!ENTITY package_url "">
<!ENTITY package_version "%{version}">
EOF

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_apidocs:--disable-docs} \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	gxmlgtkdocdir=%{_gtkdocdir}/gxml

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgxml-0.14.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc

# what a mess... gtk-doc XML intermediate files are installed to html dir...
%{__rm} -r $RPM_BUILD_ROOT%{_gtkdocdir}/gxml/*.{bottom,top,stamp,txt,types,xml}
cp -p docs/valadoc/gtk-doc/gtk-doc/gxml/html/* $RPM_BUILD_ROOT%{_gtkdocdir}/gxml

# similar to gtk-doc?
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/devhelp

# "GXml" gettext domain, "gxml" gnome help
%find_lang GXml --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f GXml.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libgxml-0.14.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgxml-0.14.so.14
%{_libdir}/girepository-1.0/GXml-0.14.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgxml-0.14.so
%{_includedir}/gxml-0.14
%{_datadir}/gir-1.0/GXml-0.14.gir
%{_pkgconfigdir}/gxml-0.14.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgxml-0.14.a
%endif

%files -n vala-gxml
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gxml-0.14.deps
%{_datadir}/vala/vapi/gxml-0.14.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gxml
%endif
