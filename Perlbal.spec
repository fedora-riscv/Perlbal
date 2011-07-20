Name:           Perlbal
Version:        1.78
Release:        2%{?dist}
Summary:        Reverse-proxy load balancer and webserver
License:        GPL+ or Artistic
Group:          System Environment/Daemons
URL:            http://search.cpan.org/dist/Perlbal/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DO/DORMANDO/%{name}-%{version}.tar.gz
Source1:        perlbal.init
BuildArch:      noarch

BuildRequires:    perl(ExtUtils::MakeMaker)
BuildRequires:    perl(Test::More)
BuildRequires:    perl(HTTP::Date)
BuildRequires:    perl(HTTP::Response)
BuildRequires:    perl(BSD::Resource)
BuildRequires:    perl(Danga::Socket)
BuildRequires:    perl(IO::AIO)

Requires:         perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:         perl(IO::AIO)
Requires:         perl(BSD::Resource)
Requires:         perl(Perlbal::XS::HTTPHeaders)

Requires(post):   chkconfig
Requires(preun):  chkconfig, initscripts
Requires(postun): chkconfig

%description
Perlbal is a single-threaded event-based server supporting HTTP load 
balancing, web serving, and a mix of the two. Perlbal can act as either a web 
server or a reverse proxy. 

One of the defining things about Perlbal is that almost everything can be 
configured or reconfigured on the fly without needing to restart the software. 
A basic configuration file containing a management port enables you to easily 
perform operations on a running instance of Perlbal. 

Perlbal can also be extended by means of per-service (and global) plugins that 
can override many parts of request handling and behavior.

%prep
%setup -q

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

install -D -p -m 0644 conf/webserver.conf %{buildroot}%{_sysconfdir}/perlbal/perlbal.conf
install -D -p -m 0755 %{SOURCE1} %{buildroot}%{_initddir}/perlbal
mkdir -p doc/examples
mv conf/* doc/examples

%check
make test

%post
/sbin/chkconfig --add perlbal

%preun
if [ $1 -eq 0 ]; then
    /sbin/chkconfig --del perlbal
    /sbin/service perlbal stop >/dev/null 2>&1 || :
fi

%postun
if [ $1 -ge 1 ] ; then
    /sbin/service perlbal condrestart > /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/perlbal
%config(noreplace) %{_sysconfdir}/perlbal/perlbal.conf
%{_initddir}/perlbal
%doc CHANGES doc/*
%{perl_vendorlib}/*
%{_bindir}/perlbal
%{_mandir}/man1/*
%{_mandir}/man3/*


%changelog
* Wed Jul 20 2011 Luis Bazan <lbazan@bakertillypanama.com> - 1.78-2
- rebuilt

* Wed Feb 09 2011 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.78-1
- Upstream released new version:
  http://cpansearch.perl.org/src/DORMANDO/Perlbal-1.78/CHANGES

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 22 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.76-1
- Upstream released new version: http://cpansearch.perl.org/src/DORMANDO/Perlbal-1.76/CHANGES
- Minor spec and initscript cleanup

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.75-2
- Mass rebuild with perl-5.12.0

* Tue Apr 06 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.75-1
- Upstream released new version

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.70-5
- rebuild against perl 5.10.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.70-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.70-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 19 2008 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.70-2
- Use Perlbal::XS::HTTPHeaders to speed up header parsing

* Sun Mar 09 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.70-1
- 1.70 (fixes build for perl 5.10.0)

* Thu Feb 07 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.60-2
- don't need patch, merged with 1.60

* Thu Feb 07 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.60-1
- 1.60

* Thu Feb 07 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.59-2
- rebuild for new perl

* Wed Jun 20 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.59-1
- Upstream released new version
- Received patch from upstream for failing buffered upload test (240693)
* Sat May 12 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.58-1
- Initial import

