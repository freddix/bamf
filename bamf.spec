Summary:	Application Matching Framework
Name:		bamf
Version:	0.5.0
Release:	1
License:	GPL v3/LGPL v3
Group:		Libraries
Source0:	https://launchpad.net/bamf/0.5/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	0d039bcbfc7da874fefa09703e3cf4e6
Patch0:		fix-legacy-window-test.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	gtk+3-devel
BuildRequires:	libgtop-devel
BuildRequires:	libtool
BuildRequires:	libwnck-devel
BuildRequires:	pkg-config
BuildRequires:	vala-vapigen
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Removes the headache of applications matching into a simple DBus
daemon and c wrapper library.

%package libs
Summary:	BAMF library
Group:		Libraries

%description libs
BAMF library.

%package devel
Summary:	Header files for BAMF library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This is the package containing the header files for BAMF library.

%package apidocs
Summary:	BAMF API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
BAMF API documentation.

%prep
%setup -q
%patch0 -p0

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' 		\
    -i -e '/SHAMROCK.*/d' configure.ac

%build
%{__libtoolize}
%{__gtkdocize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules	\
	--disable-static	\
	--enable-webapps=no	\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
# libexecdir hardcoded
%dir %{_libdir}/bamf
%attr(755,root,root) %{_libdir}/bamf/bamfdaemon
%{_datadir}/dbus-1/services/org.ayatana.bamf.service

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libbamf3.so.2
%attr(755,root,root) %{_libdir}/libbamf3.so.*.*.*
%{_libdir}/girepository-1.0/Bamf-3.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbamf3.so
%{_includedir}/libbamf3
%{_pkgconfigdir}/libbamf3.pc
%{_datadir}/gir-1.0/Bamf-3.gir
%{_datadir}/vala/vapi/libbamf3.vapi

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libbamf

