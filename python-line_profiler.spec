%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2:  %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2}  -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%global pkgname line_profiler

Name:           python-%{pkgname}
Version:        1.0
Release:        1%{?dist}
Summary:        Line-by-line profiler for python

License:        BSD
URL:            https://github.com/rkern/%{pkgname}
Source0:        https://pypi.python.org/packages/source/l/%{pkgname}/%{pkgname}-%{version}.tar.gz

BuildRequires:  python, python2-devel, python-libs
Requires:       python

%description
line_profiler is a module for doing line-by-line profiling of functions. 
kernprof is a convenient script for running either line_profiler or 
the Python standard library's cProfile or profile modules, 
depending on what is available.

%if 0%{?with_python3}
%package -n     python3-%{pkgname}
Summary:        Line-by-line profiler for python3
BuildRequires:  python3, python3-devel
Requires:       python3
%description -n python3-%{pkgname}
line_profiler is a module for doing line-by-line profiling of functions. 
kernprof is a convenient script for running either line_profiler or 
the Python standard library's cProfile or profile modules, 
depending on what is available.

%endif

%prep
%setup -q -n %{pkgname}-%{version}

%{__sed} -i '/^#!\/usr\/bin\/env\ python/d' *.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%{__sed} -i '/^#!\/usr\/bin\/env\ python/d' *.py
%endif

rm -rf *.egg-info

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%{__python2} setup.py install --skip-build --root=%{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root=%{buildroot}
popd
%endif


%files
%doc README.rst
%license LICENSE.txt
%{python2_sitearch}/*
%{_bindir}/kernprof

%if 0%{?with_python3}
%files -n python3-%{pkgname}
%doc README.rst
%license LICENSE.txt
%{python3_sitearch}/*
%{_bindir}/kernprof
%endif


%changelog
* Wed Jul  8 2015 Jackson Isaac - 1.0-1
- Initial version of line_profiler package
