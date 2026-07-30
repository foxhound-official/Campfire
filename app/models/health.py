from dataclasses import dataclass

from dataclass_wizard import JSONWizard


@dataclass(slots=True)
class Health(JSONWizard):
	current: int
	maximum: int
	temporary: int = 0

	def __post_init__(self) -> None:
		self.maximum = max(1, self.maximum)
		self.current = max(
			0,
			min(self.current, self.maximum),
		)
		self.temporary = max(0, self.temporary)

	@property
	def is_alive(self) -> bool:
		return self.current > 0

	def take_damage(self, amount: int) -> int:
		safe_amount = max(0, amount)

		absorbed_damage = min(
			self.temporary,
			safe_amount,
		)
		self.temporary -= absorbed_damage

		remaining_damage = safe_amount - absorbed_damage
		health_damage = min(
			self.current,
			remaining_damage,
		)
		self.current -= health_damage

		return absorbed_damage + health_damage

	def heal(self, amount: int) -> int:
		safe_amount = max(0, amount)
		missing_health = self.maximum - self.current
		restored_health = min(
			safe_amount,
			missing_health,
		)

		self.current += restored_health

		return restored_health