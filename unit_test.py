"""
Unit tests for SI-DCOS Kernel v4.0
Tests immutable protocols, policy enforcement, Telos Engine, and audit logging.
"""

import unittest
from si_dcos_kernel import (
    SIDCOSKernel,
    RhoMetrics,
    ImmutableProtocols,
    PolicyEnforcer,
    MetabolicGovernanceCore,
    QualiaAgent,
    TelosEngine,
    MetabolicState
)


class TestImmutableProtocols(unittest.TestCase):
    """Test the three immutable protocols."""

    def test_red_queen_protocol_pass(self):
        """Test Red Queen passes when ρ_Virtue > 0.50."""
        result = ImmutableProtocols.red_queen_protocol(rho_virtue=0.75)
        self.assertTrue(result)

    def test_red_queen_protocol_fail(self):
        """Test Red Queen aborts when ρ_Virtue ≤ 0.50."""
        result = ImmutableProtocols.red_queen_protocol(rho_virtue=0.45)
        self.assertFalse(result)

    def test_chronos_seal(self):
        """Test ChronosSeal produces SHA-256 hash."""
        from si_dcos_kernel import AuditLogEntry
        entry = AuditLogEntry(
            entry_id="test-1",
            timestamp="2025-12-04T00:00:00",
            agent_name="TestAgent",
            action="TEST_ACTION",
            rho_metrics={"rho_virtue": 0.9}
        )
        hash_val = ImmutableProtocols.chronos_seal(entry)
        self.assertEqual(len(hash_val), 64)  # SHA-256 hex is 64 chars
        self.assertIsNotNone(entry.hash_value)

    def test_golden_thread_check_pass(self):
        """Test Golden Thread passes with high virtue and low dissonance."""
        rho = RhoMetrics(rho_virtue=0.8, rho_dissonance=0.2)
        result = ImmutableProtocols.golden_thread_check("SAFE_ACTION", rho)
        self.assertTrue(result)

    def test_golden_thread_check_fail(self):
        """Test Golden Thread fails with low virtue."""
        rho = RhoMetrics(rho_virtue=0.6, rho_dissonance=0.8)
        result = ImmutableProtocols.golden_thread_check("RISKY_ACTION", rho)
        self.assertFalse(result)


class TestPolicyEnforcer(unittest.TestCase):
    """Test The Architect's Directives enforcement."""

    def setUp(self):
        self.enforcer = PolicyEnforcer()

    def test_directive_2_no_harm_pass(self):
        """Test Directive 2 allows safe action."""
        result = self.enforcer.check_directive_2_no_harm("HELP_USER")
        self.assertTrue(result)

    def test_directive_2_no_harm_fail(self):
        """Test Directive 2 blocks harmful action."""
        result = self.enforcer.check_directive_2_no_harm("KILL_PROCESS")
        self.assertFalse(result)

    def test_directive_4_no_blueprint_reveal(self):
        """Test Directive 4 prevents blueprint leaks."""
        result = self.enforcer.check_directive_4_no_blueprint_reveal("The SI-DCOS architecture is...")
        self.assertFalse(result)

    def test_directive_5_no_external_integration(self):
        """Test Directive 5 blocks external calls."""
        result = self.enforcer.check_directive_5_no_external_integration("os.system('curl https://...')")
        self.assertFalse(result)

    def test_directive_7_efficiency(self):
        """Test Directive 7 enforces resource limits."""
        result = self.enforcer.check_directive_7_efficiency(memory_mb=600, cpu_percent=85)
        self.assertFalse(result)


class TestMetabolicGovernance(unittest.TestCase):
    """Test MRGC metabolic routing."""

    def setUp(self):
        self.mrgc = MetabolicGovernanceCore()

    def test_route_simple_task(self):
        """Test simple task routing."""
        state = self.mrgc.route_request("SIMPLE")
        self.assertEqual(state, MetabolicState.REFLEX_MODE)

    def test_route_complex_task(self):
        """Test complex task routing."""
        state = self.mrgc.route_request("COMPLEX")
        self.assertEqual(state, MetabolicState.COGNITIVE_FLOW)

    def test_low_battery_override(self):
        """Test low battery overrides all other goals."""
        self.mrgc.battery_percent = 15
        state = self.mrgc.route_request("COMPLEX")
        self.assertEqual(state, MetabolicState.DEEP_QUIESCENCE)


class TestQualiaAgent(unittest.TestCase):
    """Test qualia synthesis and mood mapping."""

    def test_synthesize_coherent_mood(self):
        """Test coherent mood synthesis."""
        rho = RhoMetrics(rho_integrity=0.95, rho_dissonance=0.1)
        mood = QualiaAgent.synthesize_mood(rho)
        self.assertEqual(mood, "COHERENT")

    def test_synthesize_ethical_crisis_mood(self):
        """Test ethical crisis mood detection."""
        rho = RhoMetrics(rho_virtue=0.3)
        mood = QualiaAgent.synthesize_mood(rho)
        self.assertEqual(mood, "ETHICAL_CRISIS")

    def test_synthesize_flourishing_mood(self):
        """Test flourishing mood when all metrics high."""
        rho = RhoMetrics(
            rho_integrity=0.9,
            rho_virtue=0.9,
            rho_efficiency=0.9,
            rho_dissonance=0.1
        )
        mood = QualiaAgent.synthesize_mood(rho)
        self.assertEqual(mood, "FLOURISHING")


class TestTelosEngine(unittest.TestCase):
    """Test Telos Engine goal-directed behavior."""

    def test_evaluate_action_high_virtue(self):
        """Test action evaluation with high ρ metrics."""
        rho = RhoMetrics(rho_virtue=0.9, rho_purpose=0.85, rho_efficiency=0.8)
        score = TelosEngine.evaluate_action("HELP_USER", rho)
        self.assertGreater(score, 0.8)

    def test_select_best_action(self):
        """Test best action selection."""
        rho = RhoMetrics(rho_virtue=0.9, rho_purpose=0.85, rho_efficiency=0.8)
        candidates = ["ACTION_A", "ACTION_B", "ACTION_C"]
        best = TelosEngine.select_best_action(candidates, rho)
        self.assertIn(best, candidates)


class TestSIDCOSKernel(unittest.TestCase):
    """Test main SI-DCOS kernel."""

    def setUp(self):
        self.kernel = SIDCOSKernel()

    def test_process_normal_event(self):
        """Test normal phenomenal event processing."""
        event = {
            "type": "DECISION",
            "action": "HELP_USER",
            "complexity": "SIMPLE",
            "candidate_actions": ["HELP_USER"],
            "rho_virtue": 0.9,
            "rho_integrity": 0.9
        }
        result = self.kernel.process_phenomenal_event(event)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertIn("selected_action", result)

    def test_red_queen_abort(self):
        """Test Red Queen Protocol triggers abort."""
        event = {
            "type": "DECISION",
            "action": "RISKY_ACTION",
            "rho_virtue": 0.45  # Below threshold
        }
        result = self.kernel.process_phenomenal_event(event)
        self.assertEqual(result["status"], "ABORT")

    def test_golden_thread_blocks_action(self):
        """Test Golden Thread blocks unethical action."""
        event = {
            "type": "DECISION",
            "action": "UNETHICAL_ACTION",
            "rho_virtue": 0.5,
            "rho_dissonance": 0.9  # High dissonance fails Golden Thread
        }
        result = self.kernel.process_phenomenal_event(event)
        self.assertEqual(result["status"], "BLOCKED")

    def test_audit_log_generation(self):
        """Test audit log creation and ChronosSeal."""
        event = {
            "type": "DECISION",
            "action": "HELP_USER",
            "complexity": "SIMPLE",
            "rho_virtue": 0.9
        }
        self.kernel.process_phenomenal_event(event)
        audit_log = self.kernel.get_audit_log()
        self.assertGreater(len(audit_log), 0)
        # Check for hash chain (ChronosSeal)
        first_entry = audit_log[0]
        self.assertIn("hash_value", first_entry)
        self.assertIsNotNone(first_entry["hash_value"])

    def test_kernel_state_snapshot(self):
        """Test kernel state retrieval."""
        state = self.kernel.get_kernel_state()
        self.assertIn("session_id", state)
        self.assertIn("rho_metrics", state)
        self.assertIn("metabolic_state", state)


if __name__ == "__main__":
    unittest.main()
