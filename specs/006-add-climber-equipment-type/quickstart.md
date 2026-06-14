# Quickstart: Add Climber Equipment Type

## Setup

```bash
cd backend
python -m pip install -r requirements.txt   # if new deps
python manage.py migrate
```

The migration `0002_seed_climber_equipments.py`:
1. Inserts 30 Equipment records (E01–E30) with `equipment_type="climber"`
2. Is reversible — running `migrate equipment 0001` removes them

## Verification

```bash
# Check Climber type exists as first option
python manage.py shell -c "
from apps.equipment.models import Equipment
print('EQUIPMENT_TYPES[0]:', Equipment.EQUIPMENT_TYPES[0])
print('Climber count:', Equipment.objects.filter(equipment_type='climber').count())
print('Names:', [e.name for e in Equipment.objects.filter(equipment_type='climber')[:5]])
"
```

Expected output:
```
EQUIPMENT_TYPES[0]: ('climber', 'Climber')
Climber count: 30
Names: ['E01', 'E02', 'E03', 'E04', 'E05']
```

## Tests

```bash
cd backend
.venv/bin/python -m pytest tests/ -v
```

All 29 tests should pass.
