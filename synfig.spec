%define	major		0
%define	libname		%mklibname %{name} %{major}
%define	develname	%mklibname %{name} -d
%define debug_package	%{nil}

Name:		synfig
Summary:	Vector-based 2D animation renderer
Version:	0.64.0
Release:	2
License:	GPLv3
Group:		Graphics
URL:		http://www.synfig.org
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source100:	%{name}.rpmlintrc
Patch0:		%{name}-0.63.05-cflags.patch
# Pulfer's patch from the enemy distro.Sflo
Patch1:		synfig-0.64.0-libpng1.6.patch
BuildRequires:	cvs
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext-devel
BuildRequires:	jpeg-devel
BuildRequires:	libltdl-devel
BuildRequires:	pkgconfig(libmng)
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(ETL) >= 0.4.16
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(ImageMagick)
BuildRequires:	pkgconfig(GraphicsMagick++)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libxml++-2.6)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(sigc++-2.0)
BuildRequires:	automake
# Clang knows what  the linker is? Sflo.
BuildRequires:	gcc-c++, gcc, gcc-cpp

Requires:	libdv-apps
Requires:	imagemagick
Requires:	x11-font-cursor-misc
Requires:	x11-font-misc
Requires:	ffmpeg

%description
synfig is a vector based 2D animation renderer. It is designed to be capable
of producing feature-film quality animation.
This package contains the command-line renderer. For the GUI animation editor,
please install synfigstudio.

%files -f %{name}.lang
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%config(noreplace) %{_sysconfdir}/%{name}_modules.cfg
%{_bindir}/%{name}
%{_libdir}/%{name}

#-----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
synfig is a vector based 2D animation renderer. It is designed to be capable
of producing feature-film quality animation.
This package contains the shared library provided by synfig.

%files -n %{libname}
%doc COPYING ChangeLog NEWS
%{_libdir}/lib*.so.%{major}*

#-----------------------------------------------------------------------------

%package -n %{develname}
Summary:	Development headers and libraries for %{name}
Group:		Development/C++
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n %{develname}
synfig is a vector based 2D animation renderer. It is designed to be capable
of producing feature-film quality animation.
This package contains the development files for the shared library provided
by synfig.

%files -n %{develname}
%doc COPYING ChangeLog NEWS
%{_bindir}/%{name}-config
%{_includedir}/%{name}-*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc

#-----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1
%patch1 -p0

%build
export CC=gcc
export CXX=g++
# These two fix for the split of libMagick in recent releases - AdamW
sed -i -e 's|Magick,OptimizeImageTransparency|MagickCore,OptimizeImageTransparency|g' configure.ac
sed -i -e 's|MagickLib::|MagickCore::|g' src/modules/mod_magickpp/trgt_magickpp.cpp

autoreconf -fiv
CXXFLAGS='-I /usr/include/ImageMagick' CFLAGS='-I /usr/include/ImageMagick' CPPFLAGS='-I /usr/include/ImageMagick'
%configure2_5x \
	--disable-static \
	--with-imagemagick
%make


%install
%makeinstall_std

%find_lang %{name}
