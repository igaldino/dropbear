%global _hardened_build 1

Name:             dropbear
Version:          0.58
Release:          3%{?dist}
Summary:          A lightweight SSH server and client

Group:            Applications/Internet
License:          MIT
URL:              http://matt.ucc.asn.au/dropbear/dropbear.html
Source0:          http://matt.ucc.asn.au/%{name}/releases/%{name}-2013.58.tar.bz2
Source1:          dropbear.service
Source2:          dropbear-keygen.service

BuildRequires:    zlib-devel pam-devel
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
# For triggerun
Requires(post):   systemd-sysv

%description
Dropbear is a relatively small SSH server and client. Dropbear
is particularly useful for "embedded"-type Linux (or other Unix)
systems, such as wireless routers.

%prep
%setup -q -n %{name}-2013.58

# convert CHANGES to UTF-8
iconv -f iso-8859-1 -t utf-8 -o CHANGES{.utf8,}
mv CHANGES{.utf8,}

%build
%configure --enable-pam
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -d %{buildroot}%{_sysconfdir}/dropbear
install -d %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/dropbear.service
install -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/dropbear-keygen.service
install -d %{buildroot}%{_mandir}/man1
install -p -m 0644 dbclient.1 %{buildroot}%{_mandir}/man1/dbclient.1
install -d %{buildroot}%{_mandir}/man8
install -p -m 0644 dropbear.8 %{buildroot}%{_mandir}/man8/dropbear.8
install -p -m 0644 dropbearkey.8 %{buildroot}%{_mandir}/man8/dropbearkey.8

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart dropbear.service >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable dropbear.service > /dev/null 2>&1 || :
    /bin/systemctl stop dropbear.service > /dev/null 2>&1 || :
fi

%triggerun -- dropbear < 0.55-2
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply dropbear
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save dropbear >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del dropbear >/dev/null 2>&1 || :
/bin/systemctl try-restart dropbear.service >/dev/null 2>&1 || :

%files
%doc CHANGES LICENSE README TODO
%attr(0755,root,root) %dir %{_sysconfdir}/dropbear
%attr(0755,root,root) %{_unitdir}/dropbear*
%attr(0755,root,root) %{_bindir}/dropbearkey
%attr(0755,root,root) %{_bindir}/dropbearconvert
%attr(0755,root,root) %{_bindir}/dbclient
%attr(0755,root,root) %{_sbindir}/dropbear
%attr(0644,root,root) %{_mandir}/man1/dbclient.1*
%attr(0644,root,root) %{_mandir}/man8/dropbear.8*
%attr(0644,root,root) %{_mandir}/man8/dropbearkey.8*

%changelog
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

* Mon Apr 22 2012 Jon Ciesla <limburgher@gmail.com> - 0.55-3
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

* Mon Jan 10 2008 Lennert Buytenhek <buytenh@wantstofly.org> - 0.50-2
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
