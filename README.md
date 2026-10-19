# SolidCraft for Fedora (COPR)

[![COPR build status](https://copr.fedorainfracloud.org/coprs/blackhawk/SolidCraft/package/solidcraft/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/blackhawk/SolidCraft/package/solidcraft/)

Unofficial Fedora packages of [SolidCraft](https://github.com/tangency-labs/solidcraft), built in
[blackhawk/SolidCraft](https://copr.fedorainfracloud.org/coprs/blackhawk/SolidCraft/).

```sh
sudo dnf copr enable blackhawk/SolidCraft
sudo dnf install solidcraft
```

## How it updates

- `.github/workflows/update.yml` runs daily. When upstream has a newer release it bumps
  `solidcraft.spec` and pushes; the push triggers a COPR rebuild through the GitHub webhook.
- The same workflow fails (and GitHub emails) while the latest COPR build is failed.
- COPR builds the SRPM with `.copr/Makefile` (make_srpm method).
