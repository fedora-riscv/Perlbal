Name:           Perlbal
Version:        1.75
Release:        1%{?dist}
Summary:        Reverse-proxy load balancer and webserver
License:        GPL+ or Artistic
Group:          System Environment/Daemons
URL:            http://search.cpan.org/dist/Perlbal/
Source0:        http://search.cpan.org/CPAN/authors/id/B/BR/BRADFITZ/%{name}-%{version}.tar.gz
Source1:        perlbal.init
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
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

Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service

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
%setup -q -n Perlbal-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}


make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

install -D -p -m 0644 conf/webserver.conf %{buildroot}%{_sysconfdir}/perlbal/perlbal.conf
install -D -p -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/perlbal
mkdir -p doc/examples
mv conf/* doc/examples

%check
make test

%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --add perlbal

%preun
if [ $1 = 0 ]; then
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
%{_initrddir}/perlbal
%doc CHANGES doc/*
%{perl_vendorlib}/*
%{_bindir}/perlbal
%{_mandir}/man1/*
%{_mandir}/man3/*


%changelog
* Tue Apr 06 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.75-1
- Upstream released new version

* Wed Jun 20 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.59-1
- Upstream released new version
- Received patch from upstream for failing buffered upload test (240693)
* Sat May 12 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.58-1
- Initial import

