# TODO:
# - build against system jars (?)

%include	/usr/lib/rpm/macros.java
Summary:	Open Source Java/XML Content Management System
Name:		lenya
Version:	2.0.2
Release:	0.1
License:	Apache v2
Group:		Networking/Daemons/Java/Servlets
Source0:	http://ftp.tpnet.pl/vol/d1/apache/lenya/SOURCES/apache-%{name}-%{version}-src.tar.gz
# Source0-md5:	7e600d88ad6c866b5eda30d6d0133d11
Source1:	%{name}-context.xml
Source2:	%{name}-log4j.xconf
URL:		http://lenya.apache.org/
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

%prep
%setup -q -n apache-%{name}-%{version}-src

%build
required_jars="bcel regexp xalan xercesImpl xml-apis"
CLASSPATH=$(build-classpath $required_jars)

# use bundled ant, because it does need ant < 1.7.0
export ANT_HOME=tools

# Yeah, ugly hack
CLASSPATH=$CLASSPATH:externals/cocoon_2_1_x/tools/lib/ant-contrib-0.6.jar
CLASSPATH=$CLASSPATH:externals/cocoon_2_1_x/tools/lib/jing-20030619.jar

%ant webapp

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/lenya,%{_datadir},%{_sharedstatedir}/{lenya,tomcat/conf/Catalina/localhost},/var/log/lenya}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/lenya.xml
cp -a build/lenya/webapp $RPM_BUILD_ROOT%{_datadir}/lenya
cp %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/lenya/WEB-INF/log4j.xconf
mv $RPM_BUILD_ROOT%{_datadir}/lenya/WEB-INF/{*conf,*xml,*properties} $RPM_BUILD_ROOT%{_sysconfdir}/lenya
for I in $RPM_BUILD_ROOT%{_sysconfdir}/lenya/*; do
  ln -sf %{_sysconfdir}/lenya/$(basename $I) $RPM_BUILD_ROOT%{_datadir}/lenya/WEB-INF/
done

required_jars="bcel regexp xalan xercesImpl xml-apis"
for I in $required_jars; do
  jar=$(find-jar $I)
  ln -s $jar $RPM_BUILD_ROOT%{_datadir}/lenya/WEB-INF/lib
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/lenya
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lenya/*
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/lenya.xml
%{_datadir}/lenya
%attr(2775,root,servlet) %dir %{_sharedstatedir}/lenya
%attr(2775,root,servlet) %dir /var/log/lenya
