%define pkgname prawn
Summary:	Pure Ruby PDF generation library
Name:		ruby-%{pkgname}
Version:	0.8.4
Release:	1
License:	Ruby License
Source0:	http://rubygems.org/downloads/%{pkgname}-core-%{version}.gem
# Source0-md5:	6d0d9e583b24b0323b53756ce53edd7c
Source1:	http://rubygems.org/downloads/%{pkgname}-layout-%{version}.gem
# Source1-md5:	898db7f4a42e854277d316970c39ace6
Source2:	http://rubygems.org/downloads/%{pkgname}-security-%{version}.gem
# Source2-md5:	35213b39e4ca4a232c1cb4fa957614bd
Patch0:		%{name}-vendor.patch
Group:		Development/Languages
URL:		http://rubyforge.org/projects/.../
BuildRequires:	rpmbuild(macros) >= 1.484
BuildRequires:	ruby >= 1:1.8.6
BuildRequires:	ruby-modules
%{?ruby_mod_ver_requires_eq}
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# nothing to be placed there. we're not noarch only because of ruby packaging
%define		_enable_debug_packages	0

%description
Prawn is a pure Ruby PDF generation library that aims to make low
level PDF generation tasks easy. It is currently under active
development, and could be considered somewhere between alpha and beta
quality software. You might be able to use it in production, but then
again, you might not.

%package rdoc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for %{pkgname}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%package ri
Summary:	ri documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{pkgname}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for %{pkgname}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla %{pkgname}.

%prep
%setup -q -c
%{__tar} xf %{SOURCE2} -O data.tar.gz | %{__tar} xz
mv README{,.security}
%{__tar} xf %{SOURCE1} -O data.tar.gz | %{__tar} xz
mv README{,.layout}
%{__tar} xf %{SOURCE0} -O data.tar.gz | %{__tar} xz
find -newer README -o -print | xargs touch --reference %{SOURCE0}
%patch0 -p1

%build
rdoc --ri --op ri lib
rdoc --op rdoc lib
rm -r ri/{Arcfour,File,Numeric,String}
rm ri/created.rid

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rubylibdir},%{ruby_ridir},%{ruby_rdocdir}}

cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}
cp -a vendor $RPM_BUILD_ROOT%{ruby_rubylibdir}/prawn
cp -a data $RPM_BUILD_ROOT%{ruby_rubylibdir}/prawn

cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HACKING README*
%{ruby_rubylibdir}/%{pkgname}

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Prawn
