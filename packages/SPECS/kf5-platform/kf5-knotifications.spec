%global framework knotifications

Name:           kf5-%{framework}
Version:        5.9.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution with abstraction for system notifications

License:        LGPLv2+
URL:            http://www.kde.org

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{framework}-%{version}.tar.xz

BuildRequires:  libX11-dev

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  phonon-dev
BuildRequires:  qt5-qtbase-dev
BuildRequires:  qt5-qtx11extras-dev
BuildRequires:  qt5-qttools-dev
BuildRequires:  dbusmenu-qt5-dev

BuildRequires:  kf5-kwindowsystem-dev
BuildRequires:  kf5-kservice-dev
BuildRequires:  kf5-kconfig-dev
BuildRequires:  kf5-kiconthemes-dev
BuildRequires:  kf5-kcodecs-dev
BuildRequires:  kf5-kcoreaddons-dev

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 solution with abstraction for system
notifications.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kwindowsystem-dev
Requires:       qt5-qtbase-dev

%description    dev
The %{name}-dev package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang knotifications5_qt --with-qt --all-name

# We own the folder
mkdir -p %{buildroot}/%{_kf5_datadir}/knotifications5


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f knotifications5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5Notifications.so.*
%{_kf5_datadir}/kservicetypes5/knotificationplugin.desktop
%{_kf5_datadir}/knotifications5

%files dev
%{_kf5_includedir}/knotifications_version.h
%{_kf5_includedir}/KNotifications
%{_kf5_libdir}/libKF5Notifications.so
%{_kf5_libdir}/cmake/KF5Notifications
%{_kf5_datadir}/dbus-1/interfaces/*.xml
%{_kf5_archdatadir}/mkspecs/modules/qt_KNotifications.pri


%changelog
* Fri Apr 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- Initial version (forked from Fedora)
