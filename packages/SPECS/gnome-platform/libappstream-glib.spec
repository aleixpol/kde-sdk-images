Summary:   Library for AppStream metadata
Name:      libappstream-glib
Version:   0.3.4
Release:   1%{?dist}
License:   LGPLv2+
URL:       http://people.freedesktop.org/~hughsient/appstream-glib/
Source0:   http://people.freedesktop.org/~hughsient/appstream-glib/releases/appstream-glib-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
BuildRequires: glib2-dev
BuildRequires: gobject-introspection-dev
BuildRequires: libsoup-dev
BuildRequires: gdk-pixbuf2-dev
BuildRequires: gtk3-dev

# for the builder component
BuildRequires: fontconfig-dev
BuildRequires: freetype-dev
BuildRequires: pango-dev

%description
This library provides GObjects and helper methods to make it easy to read and
write AppStream metadata. It also provides a simple DOM implementation that
makes it easy to edit nodes and convert to and from the standardized XML
representation.

%package dev
Summary: GLib Libraries and headers for appstream-glib
Requires: %{name}%{?_isa} = %{version}-%{release}

%description dev
GLib headers and libraries for appstream-glib.

%package builder
Summary: Library and command line tools for building AppStream metadata
Requires: %{name}%{?_isa} = %{version}-%{release}

%description builder
This library and command line tool is used for building AppStream metadata
from a directory of packages.

%package builder-dev
Summary: GLib Libraries and headers for appstream-builder
Requires: %{name}-builder%{?_isa} = %{version}-%{release}

%description builder-dev
GLib headers and libraries for appstream-builder.

%prep
%setup -q -n appstream-glib-%{version}

%build
%configure \
        --disable-gtk-doc \
        --disable-dep11 \
        --disable-static \
        --disable-silent-rules \
        --disable-dependency-tracking

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%__rm -f %{buildroot}%{_libdir}/libappstream-glib*.la
%__rm -f %{buildroot}%{_libdir}/libappstream-builder*.la
%__rm -f %{buildroot}%{_libdir}/asb-plugins/*.la

%find_lang appstream-glib

%post -p /sbin/ldconfig
%post builder -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%postun builder -p /sbin/ldconfig

%files -f appstream-glib.lang
%doc README.md AUTHORS NEWS COPYING
%{_libdir}/libappstream-glib.so.7*
%{_libdir}/girepository-1.0/*.typelib
%{_bindir}/appstream-util
%{_bindir}/appdata-validate
%dir %{_datadir}/bash-completion/completions/
%{_datadir}/bash-completion/completions/appstream-util

%files dev
%{_libdir}/libappstream-glib.so
%{_libdir}/pkgconfig/appstream-glib.pc
%dir %{_includedir}/libappstream-glib
%{_includedir}/libappstream-glib/*.h
%{_datadir}/gtk-doc/html/appstream-glib
%{_datadir}/gir-1.0/AppStreamGlib-1.0.gir
%{_datadir}/aclocal/*.m4
%{_datadir}/installed-tests/appstream-glib/*.test

%files builder
%doc COPYING
%{_bindir}/appstream-builder
%{_datadir}/bash-completion/completions/appstream-builder
%{_libdir}/asb-plugins/*.so
%{_libdir}/libappstream-builder.so.7*

%files builder-dev
%doc COPYING
%{_libdir}/libappstream-builder.so
%{_libdir}/pkgconfig/appstream-builder.pc
%dir %{_includedir}/libappstream-builder
%{_includedir}/libappstream-builder/*.h
%{_datadir}/gir-1.0/AppStreamBuilder-1.0.gir

%changelog
* Mon Mar  9 2015 Alexander Larsson <alexl@redhat.com> - 0.3.4-1
- Initial version
