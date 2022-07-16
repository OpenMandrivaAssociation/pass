%bcond_without passmenu

Name:           pass
Summary:        A password manager using standard Unix tools
Version:        1.7.4
Release:        1
License:        GPLv2+
Url:            http://zx2c4.com/projects/password-store/
BuildArch:      noarch
Source:         http://git.zx2c4.com/password-store/snapshot/password-store-%{version}.tar.xz

BuildRequires:	make
BuildRequires:  git-core
BuildRequires:       gnupg2
BuildRequires:       perl-generators
BuildRequires:       tree >= 1.7.0
Requires:            git-core
Requires:            gnupg2
Requires:            qrencode
Requires:            tree >= 1.7.0

%description
Stores, retrieves, generates, and synchronizes passwords securely using gpg
and git.

%if %{with passmenu}
%package -n passmenu
Summary:        A dmenu based interface to pass.
Requires:       pass
Requires:       dmenu
Requires:       xdotool

%description -n passmenu
A dmenu based interface to pass, the standard Unix password manager. This
design allows you to quickly copy a password to the clipboard without having to
open up a terminal window if you don't already have one open. If `--type` is
specified, the password is typed using xdotool instead of copied to the
clipboard.
%endif

%prep
%setup -q -n password-store-%{version}
rm -f contrib/emacs/.gitignore

%install
make DESTDIR=%{buildroot} PREFIX=%{_prefix} \
     BINDIR=%{_bindir} SYSCONFDIR=%{_sysconfdir} \
     MANDIR=%{_mandir} WITH_ALLCOMP="yes" \
     install

%if %{with passmenu}
install -D -p -m 0755 contrib/dmenu/passmenu %{buildroot}%{_bindir}/passmenu
%endif

# Used by extensions
mkdir -p %{buildroot}%{_prefix}/lib/password-store/extensions

%check
make test

%files
%doc README COPYING contrib/emacs contrib/importers contrib/vim
%{_bindir}/pass
%{_datadir}/bash-completion/completions/pass
%{_datadir}/fish/vendor_completions.d/pass.fish
%{_datadir}/zsh/site-functions/_pass
%doc %{_mandir}/man1/*
%dir %{_prefix}/lib/password-store
%dir %{_prefix}/lib/password-store/extensions

%if %{with passmenu}
%files -n passmenu
%doc contrib/dmenu/README.md
%{_bindir}/passmenu
%endif

