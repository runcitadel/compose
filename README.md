Please don't try running this, it won't work yet.

# compose

> This software is currently in beta and is not considered secure. Please see [SECURITY.md](SECURITY.md) for more details.

This is the main respository of an open source bitcoin node project and contains the framework for orchestration of all containerized services running on [our OS](https://github.com/BitcoinNodeCommunity/os).

It is platform and architecture-agnostic, thus can be used to directly spin up instances of Umbrel without installing the [our OS](https://github.com/BitcoinNodeCommunity/os) since all orchestrated services use multi-architecture Docker images.

We run it on Raspbery Pis (ARMv8) as a part of [our OS](https://github.com/BitcoinNodeCommunity/os) and Ubuntu (x64).

## 🚀 Getting started

If you're looking to run a Bitcoin node on:

- A Raspberry Pi 4 (recommended) - [Download our OS](https://github.com/BitcoinNodeCommunity/os)
- Anything else (**not recommended** as it's experimental at the moment) - [Install](#-installation)

## 🛠 Installation

[Our OS for the Raspberry Pi](https://github.com/BitcoinNodeCommunity/os) is the easiest and the **recommended** way to run Umbrel. If you don't have a Raspberry Pi, you can manually install Umbrel on any hardware running a Linux-based operating system such as Ubuntu, Debian, etc by following the instructions below, but please note it's not the recommended way to run Umbrel as it's still very experimental.

### Installation Requirements

- [Docker](https://docs.docker.com/engine/install)
- [Python 3.0+](https://www.python.org/downloads)
- [Docker Compose](https://docs.docker.com/compose/install)
- [fswatch](https://emcrisostomo.github.io/fswatch/), [jq](https://stedolan.github.io/jq/), [rsync](https://linuxize.com/post/how-to-use-rsync-for-local-and-remote-data-transfer-and-synchronization/#installing-rsync), [curl](https://curl.haxx.se/docs/install.html) (`sudo apt-get install fswatch jq rsync curl`)

Make sure your User ID is `1000` (verify it by running `id -u`) and ensure that your account is [correctly permissioned to use docker](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

### Step 1. Download

> Run this in an empty directory where you want to install this project. If using an external storage such as an SSD or HDD, run this inside an empty directory on that drive.

```bash
curl -L https://github.com/BitcoinNodeCommunity/compose/archive/main.tar.gz | tar -xz --strip-components=1
```

### Step 2. Run

```bash
# To use mainnet, run:
sudo ./scripts/start

# For testnet, run:
sudo NETWORK=testnet ./scripts/start

# For regtest, run:
sudo NETWORK=regtest ./scripts/start
```

To stop the node, run:

```bash
sudo ./scripts/stop
```

## 🎹 Services orchestrated

- [`Umbrel Dashboard`](https://github.com/getumbrel/umbrel-dashboard) Please note: This will be replaced soon and is only used temporarily
- [`Manager`](https://github.com/BitcoinNodeCommunity/manager)
- [`Middleware`](https://github.com/BitcoinNodeCommunity/middleware)
- [`Bitcoin Core`](https://github.com/lncm/docker-bitcoind)
- [`LND`](https://github.com/lncm/docker-lnd)
- [`Tor`](https://github.com/lncm/docker-tor)
- [`Nginx`](https://github.com/nginx/nginx)
- [`Neutrino Switcher`](https://github.com/lncm/docker-lnd-neutrino-switch)


**Architecture**

```
                          + -------------------- +
                          |      dashboard       |
                          + -------------------- +
                                      |
                                      |
                              + ------------- +
                              |     nginx     |
                              + ------------- +
                                      |
                                      |
              + - - - - - - - - - - - + - - - - - - - - +
              |                                         |
              |                                         |
   +------------ +                         + -------------------- +
   |   manager   | < - - - jwt auth - - -  |      middleware      |
   + ----------- +                         + -------------------- +
                                                              |
                                                              |
                                            + - - - - - - - - + - - - - - - - - +
                                            |                                   |
                                            |                                   |
                                    + ------------- +                   + ------------- +
                                    |    bitcoind   | < - - - - - - - - |      lnd      |
                                    + ------------- +                   + ------------- +
```

---

## ⚡️ Don't be too reckless

This project is still in beta development and should not be considered secure. [Read our writeup of security tradeoffs](https://github.com/BitcoinNodeCommunity/compose/blob/main/SECURITY.md) that exist today.

It's recommended that you note down your 24 secret words (seed phrase) with a pen and paper, and secure it safely. If you forget your dashboard's password, or in case something goes wrong with your Umbrel, you will need these 24 words to recover your funds in the Bitcoin wallet of your Umbrel.

You're also recommended to download a backup of your payment channels regularly as it'll be required to recover your funds in the Lightning wallet of your Umbrel in case something goes wrong. You should also always download the latest backup file before installing an update.

## ❤️ Contributing

We welcome and appreciate new contributions.

If you're a developer looking to help but not sure where to begin, check out [these issues](https://github.com/BitcoinNodeCommunity/compose/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) that have specifically been marked as being friendly to new contributors.

If you're looking for a bigger challenge, before opening a pull request please [create an issue](https://github.com/BitcoinNodeCommunity/compose/issues/new/choose) to get feedback, discuss the best way to tackle the challenge, and to ensure that there's no duplication of work.

---

_"Being open source means anyone can independently review the code. If it was closed source, nobody could verify the security. I think it's essential for a program of this nature to be open source." — Satoshi Nakamoto_

[![License](https://img.shields.io/github/license/BitcoinNodeCommunity/compose?color=%235351FB)](https://github.com/BitcoinNodeCommunity/compose/blob/master/LICENSE)

---

This project was made possible by [Umbrel](https://getumbrel.com) which is Copyright (c) 2020 Umbrel. https://getumbrel.com.
The version we forked was available under the MIT license.
