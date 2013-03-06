Summary:	Application Matching Framework
Name:		bamf
Version:	0.3.6
Release:	1
License:	GPL v3/LGPL v3
Group:		Libraries
Source0:	https://launchpad.net/bamf/0.3/0.3.6/+download/%{name}-%{version}.tar.gz
# Source0-md5:	56b0b0ac2d3f2a0401db268c78cc8527
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

%define		_libexecdir	%{_libdir}/bamf

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
# kill gnome common deps
sed -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.in

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-webapps=no	\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/bamfdaemon
%{_datadir}/dbus-1/services/org.ayatana.bamf.service

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libbamf3.so.0
%attr(755,root,root) %{_libdir}/libbamf3.so.*.*.*
%{_libdir}/girepository-1.0/Bamf-0.2.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbamf3.so
%{_includedir}/libbamf3
%{_pkgconfigdir}/libbamf3.pc
%{_datadir}/gir-1.0/Bamf-0.2.gir
%{_datadir}/vala/vapi/libbamf3.vapi

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libbamf

