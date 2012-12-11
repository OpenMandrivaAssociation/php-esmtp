%define modname esmtp
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A34_%{modname}.ini

Summary:	ESMTP client extension for PHP
Name:		php-%{modname}
Version:	0.3.1
Release:	%mkrel 36
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/esmtp
Source0:	esmtp-%{version}.tar.bz2
Patch0:		esmtp-0.3.1-compile_fix.diff
Patch1:		esmtp-0.3.1-php53.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	libesmtp-devel >= 1.0.3r1-1mdk
BuildRequires:	openssl-devel
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Esmtp is a wrapper for SMTP client library based on the libESMTP library. You
can use it to send messages using internal SASL, and external/openssl SSL
support.

%prep

%setup -q -n esmtp-%{version}
%patch0 -p0
%patch1 -p0

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc tests CREDITS NOTES TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-36mdv2012.0
+ Revision: 795430
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-35
+ Revision: 761220
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-34
+ Revision: 696413
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-33
+ Revision: 695386
- rebuilt for php-5.3.7

* Thu Apr 28 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-32
+ Revision: 659892
- P1: fix unresolved symbols from upstream svn

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-31
+ Revision: 646629
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-30mdv2011.0
+ Revision: 629784
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-29mdv2011.0
+ Revision: 628095
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-28mdv2011.0
+ Revision: 600478
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-27mdv2011.0
+ Revision: 588760
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-26mdv2010.1
+ Revision: 514533
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-25mdv2010.1
+ Revision: 485354
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-24mdv2010.1
+ Revision: 468160
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-23mdv2010.0
+ Revision: 451265
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1:0.3.1-22mdv2010.0
+ Revision: 397514
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-21mdv2010.0
+ Revision: 376985
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-20mdv2009.1
+ Revision: 346420
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-19mdv2009.1
+ Revision: 341723
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-18mdv2009.1
+ Revision: 321720
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-17mdv2009.1
+ Revision: 310263
- rebuilt against php-5.2.7

  + Michael Scherer <misc@mandriva.org>
    - fix typo in summary

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-16mdv2009.0
+ Revision: 238390
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-15mdv2009.0
+ Revision: 200198
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-14mdv2008.1
+ Revision: 162220
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-13mdv2008.1
+ Revision: 107618
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-12mdv2008.0
+ Revision: 77538
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-11mdv2008.0
+ Revision: 39492
- use distro conditional -fstack-protector

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-10mdv2008.0
+ Revision: 21326
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.3.1-9mdv2007.0
+ Revision: 117580
- rebuilt against new upstream version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-8mdv2007.1
+ Revision: 78155
- fix deps
- bunzip patches
- rebuilt for php-5.2.0
- Import php-esmtp

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-6
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-5mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0.3.1-4mdk
- rebuilt for php-5.1.3

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-3mdk
- rebuilt against php-5.1.2

* Wed Nov 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-2mdk
- rebuilt against php-5.1.1

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-1mdk
- rebuilt against php-5.1.0
- fix versioning

* Sun Oct 02 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_0.3.1-0.RC1.1mdk
- rebuilt against php-5.1.0RC1

* Wed Sep 07 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.5_0.3.1-1mdk
- rebuilt against php-5.0.5 (Major security fixes)

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_0.3.1-1mdk
- rename the package

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_0.3.1-1mdk
- 5.0.4

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_0.3.1-2mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_0.3.1-1mdk
- initial Mandrakelinux package

* Sat Jan 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.3.1-2mdk
- rebuild due to hardened-php-0.2.6
- cleanups

* Sat Jan 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_0.3.1-1mdk
- initial mandrake package
- added P0

