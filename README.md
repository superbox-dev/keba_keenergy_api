# KEBA KeEnergy API

<!--start-home-->
A Python wrapper for the KEBA KeEnergy API used by the Web HMI.

> **Note:** This is an unofficial community project. It is not affiliated with, endorsed by or supported by KEBA.
> For support, open an [issue](https://github.com/superbox-dev/keba_keenergy_api/issues), do not contact KEBA.

![coverage-badge](https://raw.githubusercontent.com/superbox-dev/keba_keenergy_api/main/coverage-badge.svg)

[![CI](https://github.com/superbox-dev/keba_keenergy_api/actions/workflows/ci.yml/badge.svg?branch=main)][workflow-ci]
![Typing: strict][typing-strict]
![Code style: Ruff][code-ruff]

[workflow-ci]: https://github.com/superbox-dev/keba_keenergy_api/actions/workflows/ci.yml
[typing-strict]: https://img.shields.io/badge/typing-strict-green.svg
[code-ruff]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v1.json

<!--end-home-->

## Donation

<!--start-donation-->

I put a lot of time into this project. If you like it, you can support me with a donation.

[![KoFi](https://raw.githubusercontent.com/superbox-dev/.github/refs/heads/main/profile/superbox-kofi.jpg)][kofi]

[kofi]: https://ko-fi.com/F2F0KXO6D

or [donate with PayPal](https://www.paypal.com/donate?hosted_button_id=34ZFWTH4TNLXS)

<!--end-donation-->

<!--start-home-->

## Getting started

```bash
pip install keba-keenergy-api
```

```python
import asyncio

from keba_keenergy_api import KebaKeEnergyAPI
from keba_keenergy_api.endpoints import System


async def main():
    async with KebaKeEnergyAPI(
        host="ap4400.local", username="test", password="test", ssl=True, verify_ssl=False
    ) as client:
        readings = await client.read([System.OUTDOOR_TEMPERATURE])
        print(readings[System.OUTDOOR_TEMPERATURE][0].value)


asyncio.run(main())
```

See [Usage](https://superbox-dev.github.io/keba_keenergy_api/usage) for reading and writing multiple values
and sharing a session, and [Migration](https://superbox-dev.github.io/keba_keenergy_api/migration) for upgrading
from 2.x.

### ⚠️ Write warnings

This is a low-level API that allows writing values outside the safe operating range.
Improper use can damage heating systems and hardware. Always check `lower_limit` and `upper_limit` of a reading,
and write values only as often as the Web HMI would, as frequent writes wear out the built-in flash memory.
*Use at your own risk!* Read the full [write warnings](https://superbox-dev.github.io/keba_keenergy_api/usage#write-warnings)
before writing values.

<!--end-home-->

## Documentation

Read the full API documentation on [superbox-dev.github.io/keba_keenergy_api](https://superbox-dev.github.io/keba_keenergy_api/).

## Changelog

The changelog lives in the [CHANGELOG.md](CHANGELOG.md) document.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

<!--start-contributing-->

## Get Involved

The **KEBA KeEnergy API** is an open-source project and contributions are welcome. You can:

- Report [issues](https://github.com/superbox-dev/keba_keenergy_api/issues/new/choose) or request new features
- Improve documentation
- Contribute code
- Support the project by starring it on GitHub ⭐

<!--end-contributing-->

I'm happy about your contributions to the project!
You can get started by reading the [CONTRIBUTING.md](CONTRIBUTING.md).
