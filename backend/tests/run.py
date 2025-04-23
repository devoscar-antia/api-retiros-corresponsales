from datetime import datetime, time

fecha_actual = datetime(2000, 1, 1)
fecha_a = datetime.combine(fecha_actual, time(18, 0, 0))
fecha_b = datetime.combine(fecha_a, datetime.now().time())
fecha_c = datetime.now(fecha_a.tzinfo)

print(fecha_a)
print(fecha_b)
print(fecha_c)
print(fecha_a.tzinfo)
