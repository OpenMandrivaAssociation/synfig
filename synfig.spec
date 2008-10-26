%define major		0
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Name:		synfig
Summary:	Vector-based 2D animation renderer
Version:	0.61.09
Release:	%mkrel 1
Source0:	http://downloads.sourceforge.net/synfig/%{name}-%{version}.tar.gz
URL:		http://www.synfig.org
License:	GPLv2+
Group:		Graphics
BuildRequires:	etl
BuildRequires:	libxml++-devel
BuildRequires:	sigc++2.0-devel
BuildRequires:	libltdl-devel
BuildRequires:	gettext
BuildRequires:	cvs
BuildRequires:	png-devel
BuildRequires:	mng-devel
BuildRequires:	jpeg-devel
BuildRequires:	freetype2-devel
BuildRequires:	fontconfig-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	imagemagick-devel
Requires:	libdv-apps
Requires:	imagemagick
Requires:	ffmpeg
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
synfig is a vector based 2D animation renderer. It is designed to be
capable of producing feature-film quality animation.

This package contains the command-line renderer. For the GUI animation
editor, please install synfigstudio.

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
synfig is a vector based 2D animation renderer. It is designed to be
capable of producing feature-film quality animation.

This package contains the shared library provided by synfig.

%package -n %{develname}
Summary:	Development headers and libraries for %{name}
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
synfig is a vector based 2D animation renderer. It is designed to be
capable of producing feature-film quality animation.

This package contains the development files for the shared library
provided by synfig.

%prep
%setup -q

%build
# These two fix for the split of libMagick in recent releases - AdamW
sed -i -e 's.Magick,OptimizeImageTransparency.MagickCore,OptimizeImageTransparency.g' configure.ac
sed -i -e 's,MagickLib::,MagickCore::,g' src/modules/mod_magickpp/trgt_magickpp.cpp

autoreconf
CXXFLAGS='-I /usr/include/ImageMagick' CFLAGS='-I /usr/include/ImageMagick' CPPFLAGS='-I /usr/include/ImageMagick' %configure2_5x
%make
								
%install
rm -rf %{buildroot}
%makeinstall_std
%find_lang %{name}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS README NEWS TODO
%{_sysconfdir}/%{name}_modules.cfg
%{_bindir}/%{name}
%{_bindir}/%{name}-config
%{_libdir}/%{name}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/%{name}-*
%{_libdir}/lib*.so
%{_libdir}/lib*.*a
%{_libdir}/pkgconfig/%{name}.pc

