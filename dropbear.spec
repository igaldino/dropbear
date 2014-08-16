%global _hardened_build 1

Name:              dropbear
Version:           2014.65
Release:           2%{?dist}
Summary:           A lightweight SSH server and client
License:           MIT
URL:               http://matt.ucc.asn.au/dropbear/dropbear.html
Source0:           http://matt.ucc.asn.au/%{name}/releases/%{name}-%{version}.tar.bz2
Source1:           dropbear.service
Source2:           dropbear-keygen.service
BuildRequires:     libtomcrypt-devel
BuildRequires:     libtommath-devel
BuildRequires:     pam-devel
BuildRequires:     systemd
BuildRequires:     zlib-devel
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
# For triggerun
Requires(post):    systemd-sysv

%description
Dropbear is a relatively small SSH server and client. Dropbear
is particularly useful for "embedded"-type Linux (or other Unix)
systems, such as wireless routers.

%prep
%setup -q
iconv -f iso-8859-1 -t utf-8 -o CHANGES{.utf8,}
mv CHANGES{.utf8,}

%build
%configure --enable-pam --disable-bundled-libtom
%make_build

%install
%make_install
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_unitdir}
install -pm644 %{S:1} %{buildroot}%{_unitdir}/%{name}.service
install -pm644 %{S:2} %{buildroot}%{_unitdir}/dropbear-keygen.service

%post
%systemd_post %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%preun
%systemd_preun %{name}.service

%triggerun -- dropbear < 0.55-2
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply dropbear
# to migrate them to systemd targets
systemd-sysv-convert --save dropbear >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
chkconfig --del dropbear >/dev/null 2>&1 || :
systemctl try-restart dropbear.service >/dev/null 2>&1 || :

%files
%doc CHANGES LICENSE README TODO
%dir %{_sysconfdir}/dropbear
%{_unitdir}/dropbear*
%{_bindir}/dropbearkey
%{_bindir}/dropbearconvert
%{_bindir}/dbclient
%{_sbindir}/dropbear
%{_mandir}/man1/*.1*
%{_mandir}/man8/*.8*

%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.65-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 08 2014 Christopher Meng <rpm@cicku.me> - 2014.65-1
- Update to 2014.65

* Mon Jul 28 2014 Christopher Meng <rpm@cicku.me> - 2014.64-1
- Update to 2014.64

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 19 2014 Christopher Meng <rpm@cicku.me> - 2014.63-1
- Update to 2014.63

* Wed Dec 04 2013 Christopher Meng <rpm@cicku.me> - 2013.62-1
- Update to 2013.62

* Mon Oct 07 2013 Christopher Meng <rpm@cicku.me> - 2013.59-1
- New version.
- Adapt the version tag to match the actual one.
- Add systemd BR(BZ#992141).
- Unbundle libtom libraries(BZ#992141).
- Add AArch64 support(BZ#925278).
- SPEC cleanup.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Christopher Meng <rpm@cicku.me> - 0.58-4
- Cleanup systemd unit files.

* Thu May 16 2013 Christopher Meng <rpm@cicku.me> - 0.58-3
- Rebuilt.

* Thu May 16 2013 Christopher Meng <rpm@cicku.me> - 0.58-2
- Force PIE build for security issue.

* Wed May 08 2013 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.58-1
- new version

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.55-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.55-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 22 2012 Jon Ciesla <limburgher@gmail.com> - 0.55-3
- Enable pam support, fix unit file.

* Fri Apr 20 2012 Jon Ciesla <limburgher@gmail.com> - 0.55-2
- Migrate to systemd, BZ 770251.

* Sun Apr 01 2012 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.55-1
- new version 2012.55

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.52-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Apr 19 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.52-1
- New version 0.5.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.50-3
- Autorebuild for GCC 4.3

* Thu Jan 10 2008 Lennert Buytenhek <buytenh@wantstofly.org> - 0.50-2
- Incorporate changes from Fedora package review:
  - Use full URL for Source0.
  - Ship dropbear.init with mode 0644 in the SRPM.
  - Convert CHANGES to utf-8 in %%setup, as the version shipped with
    dropbear 0.50 isn't utf-8 clean (it's in iso-8859-1.)
  - Add a reload entry to the init script, and don't enable the
    service by default.

* Mon Jan  7 2008 Lennert Buytenhek <buytenh@wantstofly.org> - 0.50-1
- Update to 0.50.
- Add init script.

* Fri Aug  3 2007 Lennert Buytenhek <buytenh@wantstofly.org> - 0.49-1
- Initial packaging.
