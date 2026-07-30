from app.models.health import Health


health = Health(
	current=10,
	maximum=10,
	temporary=3,
)

damage = health.take_damage(5)

assert damage == 5
assert health.temporary == 0
assert health.current == 8

healing = health.heal(10)

assert healing == 2
assert health.current == 10

health.take_damage(100)

assert health.current == 0
assert not health.is_alive

print("Health tests passed")