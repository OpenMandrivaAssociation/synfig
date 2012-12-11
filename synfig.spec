%define major		0
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Name:		synfig
Summary:	Vector-based 2D animation renderer
Version:	0.63.05
Release:	3
License:	GPLv2+
Group:		Graphics
URL:		http://www.synfig.org
Source0:	http://downloads.sourceforge.net/synfig/%{name}-%{version}.tar.gz
Patch0:		synfig-0.63.05-cflags.patch
BuildRequires:	cvs
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext-devel
BuildRequires:	jpeg-devel
BuildRequires:	libltdl-devel
BuildRequires:	mng-devel
BuildRequires:	pkgconfig(ETL)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(ImageMagick)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libxml++-2.6)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(sigc++-2.0)
Requires:	libdv-apps
Requires:	imagemagick
Requires:	x11-font-cursor-misc
Requires:	x11-font-misc
Requires:	ffmpeg

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
sed -i -e 's|Magick,OptimizeImageTransparency|MagickCore,OptimizeImageTransparency|g' configure.ac
sed -i -e 's|MagickLib::|MagickCore::|g' src/modules/mod_magickpp/trgt_magickpp.cpp

autoreconf -fi
CXXFLAGS='-I /usr/include/ImageMagick' CFLAGS='-I /usr/include/ImageMagick' CPPFLAGS='-I /usr/include/ImageMagick'

%configure2_5x \
	--disable-static \
	--with-imagemagick
%make

%install
%makeinstall_std

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS README NEWS TODO
%config %{_sysconfdir}/%{name}_modules.cfg
%{_bindir}/%{name}
%{_libdir}/%{name}

%files -n %{libname}
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%{_bindir}/%{name}-config
%{_includedir}/%{name}-*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc


