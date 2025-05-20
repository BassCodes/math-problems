# Commands

## Dump database to json

```shell
uv run python manage.py dumpdata -e admin -e sessions -e contenttypes -e auth -e accounts > database_dump.json
```
