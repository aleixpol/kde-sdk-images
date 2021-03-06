%global qt_module qtmultimedia

%define openal 1

Summary: Qt5 - Multimedia support
Name:    qt5-%{qt_module}
Version: 5.4.1
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base

BuildRequires: qt5-qtbase-dev
BuildRequires: qt5-qtdeclarative-dev

BuildRequires: pulseaudio-libs-dev
BuildRequires: gstreamer1-dev
BuildRequires: gstreamer1-plugins-base-dev
BuildRequires: alsa-lib-dev
BuildRequires: openal-soft-dev
#BuildRequires: xv-dev
#BuildRequires: gstreamer1-plugins-bad-free

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
The Qt Multimedia module provides a rich feature set that enables you to
easily take advantage of a platforms multimedia capabilites and hardware.
This ranges from the playback and recording of audio and video content to
the use of available devices like cameras and radios.

%package dev
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-dev%{?_isa}
Requires: qt5-qtdeclarative-dev%{?_isa}
%description dev
%{summary}.

%package doc
Summary: API documentation for %{name}
License: GFDL
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
BuildRequires: qt5-qttools-dev
BuildArch: noarch
%description doc
%{summary}.

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}

# do this... or CONFIG+=git_build below
# I've no idea really why this is needed, but without it, some private headers
# do not get created
#syncqt.pl -version %{version}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} .. \
  CONFIG+=git_build \
  GST_VERSION=%{gst}

make %{?_smp_mflags}
make %{?_smp_mflags} docs
popd


%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}
make install_docs INSTALL_ROOT=%{buildroot} -C %{_target_platform}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LGPL_EXCEPTION.txt LICENSE.LGPL*
%{_qt5_libdir}/libQt5Multimedia.so.5*
%{_qt5_libdir}/libQt5MultimediaQuick_p.so.5*
%{_qt5_libdir}/libQt5MultimediaWidgets.so.5*
#%{_qt5_libdir}/libqgsttools_p.so.1*
%if 0%{?openal}
%{_qt5_archdatadir}/qml/QtAudioEngine/
%endif
%{_qt5_archdatadir}/qml/QtMultimedia/
%{_qt5_plugindir}/audio/
%{_qt5_plugindir}/mediaservice/
%{_qt5_plugindir}/playlistformats/
%dir %{_qt5_libdir}/cmake/Qt5Multimedia/
%{_qt5_libdir}/cmake/Qt5Multimedia/Qt5Multimedia_*Plugin.cmake
%dir %{_qt5_libdir}/cmake/Qt5MultimediaWidgets/

%files dev
%{_qt5_headerdir}/QtMultimedia/
%{_qt5_headerdir}/QtMultimediaQuick_p/
%{_qt5_headerdir}/QtMultimediaWidgets/
%{_qt5_libdir}/libQt5Multimedia.so
%{_qt5_libdir}/libQt5Multimedia.prl
%{_qt5_libdir}/libQt5MultimediaQuick_p.so
%{_qt5_libdir}/libQt5MultimediaQuick_p.prl
%{_qt5_libdir}/libQt5MultimediaWidgets.so
%{_qt5_libdir}/libQt5MultimediaWidgets.prl
#%{_qt5_libdir}/libqgsttools_p.so
#%{_qt5_libdir}/libqgsttools_p.prl
%{_qt5_libdir}/cmake/Qt5Multimedia/Qt5MultimediaConfig*.cmake
%{_qt5_libdir}/cmake/Qt5MultimediaWidgets/Qt5MultimediaWidgetsConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5Multimedia.pc
%{_qt5_libdir}/pkgconfig/Qt5MultimediaQuick_p.pc
%{_qt5_libdir}/pkgconfig/Qt5MultimediaWidgets.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%files doc
%doc LICENSE.FDL
%{_qt5_docdir}/qtmultimedia.qch
%{_qt5_docdir}/qtmultimedia/
%{_qt5_docdir}/qtmultimediawidgets.qch
%{_qt5_docdir}/qtmultimediawidgets/

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Thu Apr 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-1
- Initial version (forked from Fedora)
