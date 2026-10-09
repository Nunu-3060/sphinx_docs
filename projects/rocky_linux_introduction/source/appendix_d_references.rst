.. _appendix-references:

付録 D 参考文献
===============

本書の執筆にあたって参照した資料と、さらに学ぶための資料を示します。

Rocky Linux
-----------

* Rocky Linux 公式サイト: https://rockylinux.org/
* Rocky Linux のダウンロード: https://rockylinux.org/download
* Rocky Linux Documentation（公式ドキュメント）: https://docs.rockylinux.org/
* Rocky Releases（リリースとサポート期間の一覧）: https://docs.rockylinux.org/releases/
* Rocky Linux 10 のリリースノート: https://docs.rockylinux.org/releases/release_notes/10_0/
* Rocky Linux フォーラム: https://forums.rockylinux.org/

Red Hat Enterprise Linux
------------------------

Rocky Linux は RHEL と互換性があるため、RHEL のドキュメントの多くを参考にできます。

* Red Hat Enterprise Linux 10 のドキュメント: https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10

NVIDIA の GPU
-------------

* Installing NVIDIA GPU Drivers（Rocky Linux Documentation）: https://docs.rockylinux.org/desktop/display/installing_nvidia_gpu_drivers/
* NVIDIA Driver Installation Guide: https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/index.html
* NVIDIA Driver Installation Guide の Rocky Linux の節: https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/rocky-linux.html
* NVIDIA Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html
* CUDA Toolkit Documentation: https://docs.nvidia.com/cuda/

各ソフトウェア
--------------

* EPEL（Fedora Docs）: https://docs.fedoraproject.org/en-US/epel/
* systemd: https://systemd.io/
* NetworkManager: https://networkmanager.dev/
* firewalld: https://firewalld.org/
* SELinux Project: https://github.com/SELinuxProject
* GNOME: https://www.gnome.org/
* Flathub: https://flathub.org/
* Podman: https://podman.io/
* nginx: https://nginx.org/en/docs/
* Let's Encrypt: https://letsencrypt.org/
* Certbot: https://certbot.eff.org/
* Cockpit: https://cockpit-project.org/
* Ansible: https://docs.ansible.com/
* Kubernetes: https://kubernetes.io/docs/

Python
------

* Python ドキュメント（日本語）: https://docs.python.org/ja/3/
* PEP 8 -- Style Guide for Python Code: https://peps.python.org/pep-0008/
* flake8: https://flake8.pycqa.org/
* mypy: https://mypy.readthedocs.io/

マニュアル
----------

本書で扱ったコマンドや設定ファイルの詳細は、Rocky Linux 上で ``man`` コマンドで参照できます（「:ref:`ch-shell`」を参照）。主なものは次のとおりです。

* ``man dnf``、``man systemctl``、``man systemd.unit``、``man systemd.service``、``man systemd.timer``
* ``man journalctl``、``man nmcli``、``man nm-settings-keyfile``、``man firewall-cmd``
* ``man semanage-fcontext``、``man sshd_config``、``man update-crypto-policies``
* ``man podman-run``、``man podman-systemd.unit``
