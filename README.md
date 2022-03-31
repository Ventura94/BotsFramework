# MT5BotFramework

[![Pylint](https://github.com/firagapecoin/MT5BotFramework/actions/workflows/pylint.yml/badge.svg)](https://github.com/firagapecoin/MT5BotFramework/actions/workflows/pylint.yml)
[![Black](https://github.com/firagapecoin/MT5BotFramework/actions/workflows/black.yml/badge.svg)](https://github.com/firagapecoin/MT5BotFramework/actions/workflows/black.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Para instalar:

```bash
python setup.py install
```

Después de instalar se puede borrar el directorio raíz

Se importa en el script de python de la siguiente forma

```python
from MT5BotsFramework.templates.bot_strategy import BotStrategy


class SMA(BotStrategy):
    pass


```
