"""Contrato de limites entre submódulos de rastreamento.

Confere fontes realmente fixadas nos gitlinks. Não substitui E2E Kafka/Mongo.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def constant(text: str, pattern: str) -> int:
    match = re.search(pattern, text)
    if match is None:
        raise AssertionError(f"Constante de contrato ausente: {pattern}")
    return int(match.group(1))


class RouteBudgetContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.producer = (ROOT / "nestjs-api/src/routes/routes.service.ts").read_text(encoding="utf-8")
        cls.simulator = (ROOT / "golang-simulador/internal/handler.go").read_text(encoding="utf-8")
        cls.hub = (ROOT / "golang-simulador/internal/eventhub.go").read_text(encoding="utf-8")

    def test_same_route_point_budget(self):
        producer_limit = constant(self.producer, r"MAX_ROUTE_SIMULATION_POINTS\s*=\s*(\d+)")
        consumer_limit = constant(self.simulator, r"const\s+MaxRoutePoints\s*=\s*(\d+)")
        self.assertEqual(600, producer_limit)
        self.assertEqual(producer_limit, consumer_limit)
        self.assertIn("legs.steps.length * 2 > MAX_ROUTE_SIMULATION_POINTS", self.producer)
        self.assertIn("len(directions) > MaxRoutePoints", self.simulator)

    def test_simulator_rejects_large_messages_before_json_decode(self):
        limit = constant(self.hub, r"const\s+MaxEventBytes\s*=\s*(\d+)\s*\*\s*1024")
        self.assertEqual(256, limit)
        self.assertLess(self.hub.index("len(msg) > MaxEventBytes"),
                        self.hub.index("json.Unmarshal(msg"))

    def test_persisted_routes_are_validated_before_movements(self):
        self.assertIn("validateDirections(route.Directions)", self.simulator)
        self.assertLess(
            self.simulator.index("validateDirections(route.Directions)"),
            self.simulator.index("return BuildDriverMovementEvents(route), nil"),
        )

    def test_producer_checks_directions_before_writing(self):
        self.assertLess(
            self.producer.index("legs.steps.length * 2 > MAX_ROUTE_SIMULATION_POINTS"),
            self.producer.index("this.prismaService.route.create("),
        )
        self.assertLess(
            self.producer.index("directions.some("),
            self.producer.index("this.prismaService.route.create("),
        )


if __name__ == "__main__":
    unittest.main()
