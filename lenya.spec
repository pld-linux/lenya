# TODO:
# - some directories should be writeable for tomcat. Which one? Move them to /var/lib/lenya
# - where to setup lenya username/passwords? Is it possible to integrate it
#   with LDAP?

%include	/usr/lib/rpm/macros.java
Summary:	Open Source Java/XML Content Management System
Summary:(pl.UTF-8)	System zarządzania treścią oparty na Javie i XML
Name:		lenya
Version:	2.0.2
Release:	0.2
License:	Apache v2
Group:		Networking/Daemons/Java/Servlets
Source0:	http://ftp.tpnet.pl/vol/d1/apache/lenya/SOURCES/apache-%{name}-%{version}-src.tar.gz
# Source0-md5:	7e600d88ad6c866b5eda30d6d0133d11
Source1:	%{name}-context.xml
Source2:	%{name}-log4j.xconf
Source3:	%{name}-cocoon.xconf
Source4:	%{name}-web.xml
Source5:	%{name}-mysql-schema.sql
URL:		http://lenya.apache.org/
BuildRequires:	ant
BuildRequires:	java-sun
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	group(servlet)
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Apache Lenya is an Open Source Java/XML Content Management System and
comes with revision control, multi-site management, scheduling,
search, WYSIWYG editors, and workflow.

%description -l pl.UTF-8
Apache Lenya jest napisanym w Javie systemem zarządzania treścią
intensywnie wykorzystującym XML. Lenya zawiera system kontroli wersji,
edytor WYSIWYG, możliwość zarządzania wieloma publikacjami,
definiowania procedury workflow.

%prep
%setup -q -n apache-%{name}-%{version}-src

cp %{SOURCE5} mysql-schema.sql

%build

export ANT_HOME=tools

# some libs
CLASSPATH=$(build-classpath-directory externals/cocoon_2_1_x/lib/endorsed)
CLASSPATH=$CLASSPATH:externals/cocoon_2_1_x/tools/lib/ant-contrib-0.6.jar
CLASSPATH=$CLASSPATH:externals/cocoon_2_1_x/tools/lib/jing-20030619.jar

%ant webapp

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/lenya,%{_datadir},%{_sharedstatedir}/tomcat/conf/Catalina/localhost,/var/log/lenya}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/lenya.xml
cp -a build/lenya/webapp $RPM_BUILD_ROOT%{_datadir}/lenya
mv $RPM_BUILD_ROOT%{_datadir}/lenya/lenya $RPM_BUILD_ROOT%{_sharedstatedir}/lenya
ln -s %{_sharedstatedir}/lenya $RPM_BUILD_ROOT%{_datadir}/lenya

# use libraries provided by lenya. Lenya need exact version of these jars.
# Don't try to use system libraries. It won't work.
mv $RPM_BUILD_ROOT%{_datadir}/lenya/WEB-INF/lib{/endorsed/*,}
rmdir $RPM_BUILD_ROOT%{_datadir}/lenya/WEB-INF/lib/endorsed

cp %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/lenya/WEB-INF/log4j.xconf
cp %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/lenya/WEB-INF/cocoon.xconf
cp %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/lenya/WEB-INF/web.xml
mv $RPM_BUILD_ROOT%{_datadir}/lenya/WEB-INF/{*conf,*xml,*properties} $RPM_BUILD_ROOT%{_sysconfdir}/lenya
for I in $RPM_BUILD_ROOT%{_sysconfdir}/lenya/*; do
  ln -sf %{_sysconfdir}/lenya/$(basename $I) $RPM_BUILD_ROOT%{_datadir}/lenya/WEB-INF/
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CREDITS.txt KEYS NOTICE.txt README.txt RELEASE-NOTES.txt mysql-schema.sql
%dir %{_sysconfdir}/lenya
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lenya/*
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/lenya.xml
%{_datadir}/lenya
%attr(2775,root,servlet) %{_sharedstatedir}/lenya
%attr(2775,root,servlet) %dir /var/log/lenya
