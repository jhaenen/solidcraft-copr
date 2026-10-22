%global app_id ai.storyteller.solidcraft

Name:           solidcraft
Version:        0.19.0
Release:        1%{?dist}
Summary:        Open-source parametric 3D CAD application built in pure Rust

License:        MIT OR Apache-2.0
URL:            https://github.com/tangency-labs/solidcraft
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Upstream only builds and tests these architectures.
ExclusiveArch:  x86_64 aarch64

# Upstream's workspace needs rust-version 1.95. Crates are fetched from crates.io during
# the build, so the COPR project needs "Enable internet access during builds".
BuildRequires:  cargo
BuildRequires:  rust >= 1.95
BuildRequires:  gcc
BuildRequires:  desktop-file-utils
BuildRequires:  appstream

# The binaries only link glibc and libgcc_s; windowing and the GPU are dlopen()ed at
# runtime, so list them by hand (same set as upstream's packaging/linux/nfpm.yaml).
Requires:       libxkbcommon.so.0()(64bit)
Requires:       libxkbcommon-x11.so.0()(64bit)
Requires:       libwayland-client.so.0()(64bit)
Requires:       libX11.so.6()(64bit)
Requires:       libX11-xcb.so.1()(64bit)
Requires:       libxcb.so.1()(64bit)
Requires:       libXcursor.so.1()(64bit)
Requires:       libXi.so.6()(64bit)
Requires:       (libvulkan.so.1()(64bit) or libEGL.so.1()(64bit))
Recommends:     mesa-vulkan-drivers
Recommends:     xdg-desktop-portal

# The project was called SolveCraft before 0.8.
Obsoletes:      solvecraft < %{version}-%{release}
Provides:       solvecraft = %{version}-%{release}

%description
SolidCraft is an open-source parametric 3D CAD application in the style of Fusion:
sketches with a constraint solver, a parametric feature timeline, components and
joints, sheet metal, and STEP, IGES, 3MF, STL and OBJ import and export.

It includes solidcraft-cli, a headless command runner and MCP server for AI agents.

%prep
%autosetup -n %{name}-%{version}

%build
# Upstream's thin LTO needs ~12 GB of RAM per binary in its final step, more than COPR
# builders reliably have. Without it the binaries are larger but just as usable.
export CARGO_PROFILE_RELEASE_LTO=off
# Some crates (cadmpeg-ir) need ~6 GB each to compile; one job per CPU gets rustc OOM-killed.
%constrain_build -m 6144
cargo build --release --locked -j %{_smp_build_ncpus} -p solidcraft -p solidcraft-cli

%install
install -Dm755 target/release/solidcraft     %{buildroot}%{_bindir}/solidcraft
install -Dm755 target/release/solidcraft-cli %{buildroot}%{_bindir}/solidcraft-cli
# Compatibility shim: the old CLI name forwards to solidcraft-cli.
install -Dm755 target/release/solvecraft-cli %{buildroot}%{_bindir}/solvecraft-cli

install -Dm644 assets/platforms/linux/%{app_id}.desktop \
  %{buildroot}%{_datadir}/applications/%{app_id}.desktop
install -Dm644 assets/platforms/linux/%{app_id}.mime.xml \
  %{buildroot}%{_datadir}/mime/packages/%{app_id}.xml

release_date=$(date -u -d "@${SOURCE_DATE_EPOCH:-$(date +%%s)}" +%%Y-%%m-%%d)
mkdir -p %{buildroot}%{_metainfodir}
sed -e "s/@VERSION@/%{version}/g" -e "s/@DATE@/${release_date}/g" \
  assets/platforms/linux/%{app_id}.metainfo.xml.in \
  > %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml

for s in 16 24 32 48 64 128 256 512; do
  install -Dm644 assets/icons/app/linux/exports/hicolor/${s}x${s}/apps/%{app_id}.png \
    %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/%{app_id}.png
done

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{app_id}.desktop
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml
%{buildroot}%{_bindir}/solidcraft-cli --version

%files
%license LICENSE-MIT LICENSE-APACHE NOTICE THIRD-PARTY-LICENSES.txt
%doc README.md
%{_bindir}/solidcraft
%{_bindir}/solidcraft-cli
%{_bindir}/solvecraft-cli
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/mime/packages/%{app_id}.xml
%{_metainfodir}/%{app_id}.metainfo.xml
%{_datadir}/icons/hicolor/*/apps/%{app_id}.png

%changelog
* Thu Oct 22 2026 SolidCraft COPR bot <jasper@haenenweb.nl> - 0.19.0-1
- Update to 0.19.0

* Wed Oct 21 2026 SolidCraft COPR bot <jasper@haenenweb.nl> - 0.18.2-1
- Update to 0.18.2

* Mon Oct 19 2026 SolidCraft COPR bot <jasper@haenenweb.nl> - 0.16.2-1
- Update to 0.16.2

* Mon Oct 19 2026 blackhawk <jasper@haenenweb.nl> - 0.16.1-1
- Initial COPR package
