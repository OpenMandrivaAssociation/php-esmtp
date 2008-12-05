%define modname esmtp
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A34_%{modname}.ini

Summary:	ESMTP client extension for PHP
Name:		php-%{modname}
Version:	0.3.1
Release:	%mkrel 17
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/esmtp
Source0:	esmtp-%{version}.tar.bz2
Patch0:		esmtp-0.3.1-compile_fix.diff
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
