# Security Disclosure

**This project is currently in beta and is not considered secure.**

We are trying to iterate rapidly and build out our vision and only have so many hours in the day. Due to this, we've decided to make the following trade-offs to allow us to ship a working beta with critical features, such as over-the-air (OTA) updates and easy log access, as soon as possible.

**No signature verification on OTA updates**

The lack of signature verification means GitHub as a company could backdoor the OTA update process. It's quite unlikely that they would do this but currently we just have to trust that they won't. If this were to occur, the current update system would not detect or prevent it.

**3rd-party Node.js dependencies.**

During the beta phase we are making use of Node.js and its rich ecosystem of npm packages to rapidly build out features. However the npm ecosystem tends to make use of a large number of small focused modules. This can make audibility difficult as you end up with a huge dependency tree for even relatively simple projects.

The issues raised above will all be resolved before we do a stable release.
