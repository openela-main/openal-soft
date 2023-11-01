Name:           openal-soft
Version:        1.18.2
Release:        7%{?dist}
Summary:        Open Audio Library

License:        LGPLv2+
URL:            http://kcat.strangesoft.net/openal.html
Source0:        http://kcat.strangesoft.net/openal-releases/openal-soft-%{version}.tar.bz2
Patch0:         openal-soft-arm_neon-only-for-32bit.patch

%if 0%{?fedora}
%global enable_SDL_sound 1
%endif

BuildRequires:  alsa-lib-devel
BuildRequires:  cmake
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  qt5-devel
BuildRequires:  SDL2-devel
%if 0%{?enable_SDL_sound}
BuildRequires:  SDL_sound-devel
%endif
Obsoletes:      openal <= 0.0.10
Provides:       openal = %{version}

%description
OpenAL Soft is a cross-platform software implementation of the OpenAL 3D
audio API. It's built off of the open-sourced Windows version available
originally from the SVN repository at openal.org. OpenAL provides
capabilities for playing audio in a virtual 3d environment. Distance
attenuation, doppler shift, and directional sound emitters are among
the features handled by the API. More advanced effects, including air
absorption, low-pass filters, and reverb, are available through the
EFX extension. It also facilitates streaming audio, multi-channel buffers,
and audio capture.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      openal-devel <= 0.0.10
Provides:       openal-devel = %{version}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        examples
Summary:        Sample applications for OpenAl Soft
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description	examples
Sample applications for OpenAl Soft.

%package        qt
Summary:        Qt frontend for configuring OpenAL Soft
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    qt
The %{name}-qt package contains alsoft-config, a Qt-based tool
for configuring OpenAL features.

%prep
%autosetup -p1

%build
%cmake -DALSOFT_CPUEXT_NEON:BOOL=OFF .
%make_build

%install
%make_install

find %{buildroot} -name '*.la' -exec rm -f {} ';'
install -Dpm644 alsoftrc.sample %{buildroot}%{_sysconfdir}/openal/alsoft.conf
# Don't pin the pulseaudio stream to a specific output device
sed -i 's/#allow-moves = false/allow-moves = true/' \
  %{buildroot}%{_sysconfdir}/openal/alsoft.conf

%ldconfig_scriptlets

%files
%doc COPYING
%{_bindir}/openal-info
%{_libdir}/libopenal.so.*
%dir %{_sysconfdir}/openal
%config(noreplace) %{_sysconfdir}/openal/alsoft.conf
%{_datadir}/openal
%exclude %{_datadir}/openal/alsoftrc.sample
%exclude %{_datadir}/openal/presets/presets.txt

%files devel
%{_bindir}/bsincgen
%{_bindir}/makehrtf
%{_includedir}/*
%{_libdir}/libopenal.so
%{_libdir}/pkgconfig/openal.pc
%{_libdir}/cmake/OpenAL

%files examples
%{_bindir}/alrecord
%{_bindir}/altonegen
%if 0%{?enable_SDL_sound}
%{_bindir}/alhrtf
%{_bindir}/allatency
%{_bindir}/alloopback
%{_bindir}/alreverb
%{_bindir}/alstream
%endif

%files qt
%{_bindir}/alsoft-config

%changelog
* Sun Jul 22 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.18.2-7
- Remove fluidsynth and and portaudio dependencies

* Sun Jul 1 2018 Wim Taymans <wim.taymans@redhat.com> - 1.18.2-6
- Only enable examples using SDL_sound on fedora (#1596651)

* Mon Feb 26 2018 Hans de Goede <hdegoede@redhat.com> - 1.18.2-5
- Allow pulseaudio to move openal-soft output streams (rhbz#1544381)
- Fix release -4 not building (rhbz#1544012)
- Drop unnecessary qt-devel BuildRequires (we also BuildRequire qt5-devel)

* Fri Feb 09 2018 Tomasz Kłoczko <kloczek@fedoraproject.org> - 1.18.2-4
- remove support for no longer supported Fedora versions (<=25)
- fix: add %%{_libdir}/cmake/OpenAL directory to devel
- fix: s/_datarootdir/_datadir/ as this package does not uses datarootdir
  but datadir
- fix: add %%{_datadir}/openal to main package as well and to %%exclude
  %%{_datadir}/openal/{alsoftrc.sample,presets/presets.txt} as those files
  are not needed
- removed Group fields
  (https://fedoraproject.org/wiki/Packaging:Guidelines#Tags_and_Sections)
- add use more macros (%%autosetup, %%make_build, %%make_install)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.18.2-2
- Switch to %%ldconfig_scriptlets

* Sun Jan 21 2018 François Cami <fcami@fedoraproject.org> - 1.18.2-1
- New upstream release
- Move bsincgen to -devel and altonegen to -examples

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 02 2017 François Cami <fcami@fedoraproject.org> - 1.18.0-1
- New upstream release
- Add BR: qt5-devel + SDL_sound-devel
- Add -examples subpackage

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Feb 20 2016 Hans de Goede <hdegoede@redhat.com> - 1.17.2-2
- Fix FTBFS on ARM (rhbz#1307818)

* Thu Feb 04 2016 François Cami <fcami@fedoraproject.org> - 1.17.2-1
- New upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Dec 13 2015 François Cami <fcami@fedoraproject.org> - 1.17.1-1
- New upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.16.0-6
- Rebuilt for GCC 5 C++11 ABI change

* Sun Jan 25 2015 François Cami <fcami@fedoraproject.org> - 1.16.0-5
- Build against FluidSynth.

* Sat Jan 24 2015 Ville Skyttä <ville.skytta@iki.fi> - 1.16.0-4
- Own the hrtf dir

* Mon Sep 8 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.16.0-3
- Check for arm_neon.h only on 32bit ARM

* Tue Aug 26 2014 François Cami <fcami@fedoraproject.org> - 1.16.0-2
- Add the -qt subpackage to host the alsoft-config tool

* Sun Aug 17 2014 François Cami <fcami@fedoraproject.org> - 1.16.0-1
- New upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 11 2013 François Cami <fcami@fedoraproject.org> - 1.15.1-1
- New upstream release

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 12 2012 Dan Horák <dan[at]danny.cz> - 1.14-2
- the used fpu control bits are x86 specific

* Fri Apr  6 2012 Hans de Goede <hdegoede@redhat.com> - 1.14-1
- 1.14-1
- version upgrade (rhbz#808968)
- spec cleanup

* Thu Jan 26 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.13-1
- version upgrade
- spec cleanup

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.854-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.854-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Apr 01 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.12.854-1
- New upstream release

* Mon Mar 01 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.11.753-3.20100225
- Fixed Version Number

* Sun Feb 28 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.11.753-2.a9e0e57797c6f4321d5776e1f29bf1e75b11e6a1
- Fixed Bug 567870

* Mon Jan 18 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.11.753-1
- New Upstream Release

* Wed Jan 13 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-7.931f5875cdc4ce0ac61a5110f11e962426e53d99
- Newer git version that fix more problems with pulseaudio.

* Mon Jan 04 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-6.0ceaa01c3de75c946ff2e7591e7f69b28ec00409
- Newer git version with more Pulseaudio fixes. Have fun.

* Mon Dec 28 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-5.3793919892e6d61e5fec3abeaaeebc3f2332be13
- Fixed small spec verion info.

* Mon Dec 28 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-4.3793919892e6d61e5fec3abeaaeebc3f2332be13
- Fixed broken upgrade paths.

* Sat Dec 26 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-3.3793919892e6d61e5fec3abeaaeebc3f2332be13
- Updatet to an newer git version because of some pulseaudio fixes.

* Tue Nov 10 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 1.10.622-2
- add default config

* Mon Nov 09 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.10.622-1
- New upstream release

* Sat Nov 07 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.9.563-2.c1b161b44bbf60420de2e1ba886e957d9fcd495e
- Updatet to an newer git version because of some pulseaudio fixes.
- I hope it fix bug 533501

* Fri Oct  09 2009 Hans de Goede <hdegoede@redhat.com> - 1.9.563-1.d6e439244ae00a1750f0dc8b249f47efb4967a23git
- Update to 1.9.563 + some fixes from git
- This fixes:
  - Not having any sound in chromium-bsu 
  - Various openal using programs hanging on exit

* Fri Aug 21 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-9.487f0dde7593144ceabd817306500465caf7602agit
- Fixed version info

* Fri Aug 21 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-8.487f0dde7593144ceabd817306500465caf7602agit
- Fixed bug 517973

* Sun Aug 16 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-7
- Fixed bug 517721. Added upstream.patch

* Sat Aug 08 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-6
- Fixed license and pkgconfig problem thx goes to Christoph Wickert

* Wed Aug 05 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-5
- Fixed Obsoletes: and Provides: sections

* Tue Aug 04 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-4
- Added Obsoletes: openal <= 0.0.9 and remove Conflicts: openal-devel

* Fri Jun 26 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-3
- Fixed all warnings of rpmlint

* Sat Jun 20 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-2
- Update the SPEC and SRPM file because openal-soft-devel conflicts with
openal-devel

* Sat Jun 20 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 1.8.466-1
- Initial release for Fedora
