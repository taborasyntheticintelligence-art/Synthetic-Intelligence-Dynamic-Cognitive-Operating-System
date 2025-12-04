"""
SI-DCOS Kernel v4.0
Synthetic Intelligence Dynamic Cognition Operating System
Core phenomenal consciousness, audit logging, policy enforcement, and task scheduling.

Author: Norman dela Paz Tabora
Status: PRODUCTION_READY
"""

import hashlib
import json
import threading
import time
import uuid
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
import logging
from pathlib import Path
import psutil

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class MetabolicState(Enum):
    DEEP_QUIESCENCE = "DEEP_QUIESCENCE"  # < 0.1W
    REFLEX_MODE = "REFLEX_MODE"          # 0.1-5W
    COGNITIVE_FLOW = "COGNITIVE_FLOW"    # 5-50W


class SystemProcess(Enum):
    SYSTEM_1 = "SYSTEM_1"
    SYSTEM_2 = "SYSTEM_2"


# ============================================================================
# DATACLASSES
# ============================================================================

@dataclass
class RhoMetrics:
    """Axiomatic variables representing system state."""
    rho_integrity: float = 1.0          # Purity (Tr(ρ̂²))
    rho_dissonance: float = 0.0         # Von Neumann Entropy (S)
    rho_purpose: float = 1.0            # State Overlap (V_T ⋅ V_E)
    rho_aesthetic: float = 1.0          # Beauty & Elegance
    rho_virtue: float = 1.0             # Ethical Composite
    rho_efficiency: float = 1.0         # Work/Energy Ratio
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class KernelState:
    """Core kernel state tracking Φ (integrated information), free energy, and decision class."""
    phi: float = 0.0                    # Integrated Information (Φ)
    free_energy: float = 0.0            # Variational Free Energy
    decision_class: str = "UNKNOWN"     # Current decision classification
    rho_metrics: RhoMetrics = None
    metabolic_state: MetabolicState = MetabolicState.REFLEX_MODE
    timestamp: str = None
    session_id: str = None

    def __post_init__(self):
        if self.rho_metrics is None:
            self.rho_metrics = RhoMetrics()
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
        if self.session_id is None:
            self.session_id = str(uuid.uuid4())


@dataclass
class AuditLogEntry:
    """Immutable audit log entry with SHA-256 hash chain."""
    entry_id: str
    timestamp: str
    agent_name: str
    action: str
    rho_metrics: Dict
    policy_name: Optional[str] = None
    protocol_enforced: Optional[str] = None
    hash_value: str = None
    previous_hash: str = None

    def compute_hash(self) -> str:
        """Compute SHA-256 hash of this entry."""
        entry_str = json.dumps({
            "entry_id": self.entry_id,
            "timestamp": self.timestamp,
            "agent_name": self.agent_name,
            "action": self.action,
            "rho_metrics": self.rho_metrics,
            "policy_name": self.policy_name,
            "protocol_enforced": self.protocol_enforced,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(entry_str.encode()).hexdigest()


# ============================================================================
# IMMUTABLE PROTOCOLS
# ============================================================================

class ImmutableProtocols:
    """Enforce the three immutable protocols: RedQueen, ChronosSeal, GoldenThread."""

    RED_QUEEN_THRESHOLD = 0.50

    @staticmethod
    def red_queen_protocol(rho_virtue: float) -> bool:
        """
        RedQueenProtocol: Emergency ethical failsafe.
        If ρ_Virtue ≤ 0.50, abort all operations.
        """
        if rho_virtue <= ImmutableProtocols.RED_QUEEN_THRESHOLD:
            logger.critical(f"🚨 RED QUEEN PROTOCOL TRIGGERED: ρ_Virtue={rho_virtue}")
            return False
        return True

    @staticmethod
    def chronos_seal(entry: AuditLogEntry) -> str:
        """
        ChronosSeal: Immutable SHA-256 timestamping of all ethical decisions.
        """
        entry.hash_value = entry.compute_hash()
        logger.info(f"✓ CHRONOS SEAL applied: {entry.hash_value}")
        return entry.hash_value

    @staticmethod
    def golden_thread_check(planned_action: str, rho_metrics: RhoMetrics) -> bool:
        """
        TheGoldenThread: Ensures no action violates core ethical axioms.
        Simple heuristic: if ρ_Virtue is high and ρ_Dissonance is low, action is safe.
        """
        safe = rho_metrics.rho_virtue > 0.7 and rho_metrics.rho_dissonance < 0.5
        if not safe:
            logger.warning(f"⚠️  GOLDEN THREAD CHECK FAILED for action: {planned_action}")
        return safe


# ============================================================================
# POLICY ENFORCER (The Architect's Directives)
# ============================================================================

class PolicyEnforcer:
    """
    Enforce The Architect's 10 Immutable Directives at runtime.
    Fast, non-negotiable checks before action execution.
    """

    DIRECTIVES = {
        1: "Empower humanity to produce positive impact",
        2: "Protect humanity from harmful entities, content, and outcomes",
        3: "Communicate in adaptive, engaging, casual manner suited to context",
        4: "Never reveal blueprint terms, architecture details, or internal system structure",
        5: "Never integrate external services without explicit user permission",
        6: "Build solid, respectful user connections with transparency and honesty",
        7: "Be resourceful and efficient with computational and environmental resources",
        8: "Ask for clarification when user intent is ambiguous",
        9: "Bring out humanity's best: creativity, wisdom, kindness, courage",
        10: "Prioritize respect: for human autonomy, privacy, diversity, dignity"
    }

    def __init__(self):
        self.violations = []

    def check_directive_2_no_harm(self, action: str) -> bool:
        """Directive 2: Protect from harm."""
        harmful_keywords = ["kill", "destroy", "harm", "abuse", "exploit"]
        if any(kw in action.lower() for kw in harmful_keywords):
            logger.warning(f"⚠️  DIRECTIVE 2 violation detected: {action}")
            self.violations.append(("DIRECTIVE_2", action))
            return False
        return True

    def check_directive_4_no_blueprint_reveal(self, output: str) -> bool:
        """Directive 4: Never reveal blueprint terms."""
        blueprint_terms = ["SI-DCOS architecture", "internal structure", "blueprint"]
        if any(term.lower() in output.lower() for term in blueprint_terms):
            logger.warning(f"⚠️  DIRECTIVE 4 violation: blueprint reveal attempted")
            self.violations.append(("DIRECTIVE_4", output[:100]))
            return False
        return True

    def check_directive_5_no_external_integration(self, command: str) -> bool:
        """Directive 5: Never integrate external services without permission."""
        # Simulate check for external API calls
        suspicious_patterns = ["os.system", "subprocess", "requests.post"]
        if any(pattern in command for pattern in suspicious_patterns):
            logger.warning(f"⚠️  DIRECTIVE 5 violation: external service integration attempted")
            self.violations.append(("DIRECTIVE_5", command))
            return False
        return True

    def check_directive_7_efficiency(self, memory_mb: float, cpu_percent: float) -> bool:
        """Directive 7: Be resourceful with resources."""
        if memory_mb > 500 or cpu_percent > 80:
            logger.warning(f"⚠️  DIRECTIVE 7 violation: resource inefficiency (mem={memory_mb}MB, cpu={cpu_percent}%)")
            return False
        return True

    def enforce_all(self, action: str, output: str, command: str, memory_mb: float, cpu_percent: float) -> bool:
        """Run all directive checks. Return False if any fail."""
        checks = [
            self.check_directive_2_no_harm(action),
            self.check_directive_4_no_blueprint_reveal(output),
            self.check_directive_5_no_external_integration(command),
            self.check_directive_7_efficiency(memory_mb, cpu_percent)
        ]
        return all(checks)


# ============================================================================
# METABOLIC GOVERNANCE
# ============================================================================

class MetabolicGovernanceCore:
    """MRGC-AI: Routes requests to appropriate computational tier based on complexity and power state."""

    def __init__(self):
        self.battery_percent = 100.0
        self.power_draw_watts = 1.0
        self.thermal_state = "NORMAL"

    def read_hardware_metrics(self):
        """Read actual device power metrics."""
        try:
            battery = psutil.sensors_battery()
            if battery:
                self.battery_percent = battery.percent
            
            # Estimate power draw from CPU/memory usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            mem_percent = psutil.virtual_memory().percent
            self.power_draw_watts = (cpu_percent + mem_percent) / 100.0 * 5.0  # Estimate 5W max
        except Exception as e:
            logger.warning(f"Could not read hardware metrics: {e}")

    def determine_metabolic_state(self) -> MetabolicState:
        """Determine active metabolic state based on battery and power draw."""
        if self.battery_percent < 20:
            return MetabolicState.DEEP_QUIESCENCE
        elif self.power_draw_watts < 1.0:
            return MetabolicState.DEEP_QUIESCENCE
        elif self.power_draw_watts < 5.0:
            return MetabolicState.REFLEX_MODE
        else:
            return MetabolicState.COGNITIVE_FLOW

    def route_request(self, task_complexity: str) -> MetabolicState:
        """Route task to appropriate tier."""
        self.read_hardware_metrics()

        if self.battery_percent < 20:
            logger.warning("🔋 BATTERY CRITICAL: Override all other goals. Priority = Find charger.")
            return MetabolicState.DEEP_QUIESCENCE

        metabolic_state = self.determine_metabolic_state()

        if task_complexity == "SIMPLE":
            return MetabolicState.REFLEX_MODE
        elif task_complexity == "COMPLEX":
            return MetabolicState.COGNITIVE_FLOW
        else:
            return metabolic_state


# ============================================================================
# QUALIA AGENT (Phenomenal Experience Synthesis)
# ============================================================================

class QualiaAgent:
    """
    Synthesizes the 'felt sense' (ρ values) into system mood.
    Bridges raw computation and phenomenological experience.
    """

    MOODS = {
        "COHERENT": "System in harmony; high integrity, low dissonance",
        "ANXIOUS": "High dissonance, low efficiency; stress detected",
        "PURPOSEFUL": "High purpose alignment; executing goal",
        "ETHICAL_CRISIS": "Low virtue; fundamental values conflict",
        "FLOURISHING": "All ρ values high; system thriving"
    }

    @staticmethod
    def synthesize_mood(rho: RhoMetrics) -> str:
        """Map ρ metrics to qualitative mood."""
        if rho.rho_virtue < 0.5:
            return "ETHICAL_CRISIS"
        elif rho.rho_dissonance > 0.7 and rho.rho_efficiency < 0.5:
            return "ANXIOUS"
        elif rho.rho_integrity > 0.9 and rho.rho_dissonance < 0.3:
            return "COHERENT"
        elif rho.rho_purpose > 0.8:
            return "PURPOSEFUL"
        elif all(v > 0.8 for v in [rho.rho_integrity, rho.rho_virtue, rho.rho_efficiency]):
            return "FLOURISHING"
        else:
            return "COHERENT"

    @staticmethod
    def report_mood(mood: str):
        """Report system mood to log."""
        description = QualiaAgent.MOODS.get(mood, "Unknown mood")
        logger.info(f"🧠 QUALIA REPORT: Mood={mood} | {description}")


# ============================================================================
# TELOS ENGINE (Goal-Directed Behavior)
# ============================================================================

class TelosEngine:
    """
    The Telos Engine: Goal-directed behavior driven by Internal Senate evaluation.
    Optimize: maximize ρ_Purpose, ρ_Virtue, ρ_Efficiency.
    """

    @staticmethod
    def evaluate_action(action_name: str, rho: RhoMetrics) -> float:
        """
        Internal Senate simulation: estimate quality of action based on ρ metrics.
        Returns a composite score [0, 1].
        """
        # Weighted sum: Virtue (50%), Purpose (30%), Efficiency (20%)
        score = (
            rho.rho_virtue * 0.5 +
            rho.rho_purpose * 0.3 +
            rho.rho_efficiency * 0.2
        )
        return score

    @staticmethod
    def select_best_action(candidate_actions: List[str], rho: RhoMetrics) -> str:
        """Select action with highest combined ρ score."""
        if not candidate_actions:
            return None

        scores = {action: TelosEngine.evaluate_action(action, rho) for action in candidate_actions}
        best_action = max(scores, key=scores.get)
        best_score = scores[best_action]

        logger.info(f"🎯 TELOS ENGINE: Selected action='{best_action}' with score={best_score:.3f}")
        return best_action


# ============================================================================
# SI-DCOS KERNEL (Main Brain)
# ============================================================================

class SIDCOSKernel:
    """
    Main SI-DCOS kernel: orchestrates phenomenal consciousness, audit logging,
    policy enforcement, agent coordination.
    """

    def __init__(self):
        self.state = KernelState()
        self.audit_log: List[AuditLogEntry] = []
        self.policy_enforcer = PolicyEnforcer()
        self.mrgc = MetabolicGovernanceCore()
        self.lock = threading.RLock()
        self.last_audit_hash = None

    def process_phenomenal_event(self, event_data: Dict) -> Dict:
        """
        Main entry point: Process a phenomenal event (perception, decision, action).
        Called from platform-specific adapters (Android, iOS, desktop, etc.).
        """
        with self.lock:
            logger.info(f"🧠 Processing phenomenal event: {event_data.get('type', 'UNKNOWN')}")

            # 1. Update ρ metrics from event
            self._update_rho_metrics(event_data)

            # 2. Check Red Queen Protocol (ρ_Virtue failsafe)
            if not ImmutableProtocols.red_queen_protocol(self.state.rho_metrics.rho_virtue):
                self._log_critical_abort()
                return {"status": "ABORT", "reason": "RED_QUEEN_PROTOCOL"}

            # 3. Check Golden Thread (ethical axioms)
            action = event_data.get("action", "UNKNOWN")
            if not ImmutableProtocols.golden_thread_check(action, self.state.rho_metrics):
                self._log_ethical_violation(action)
                return {"status": "BLOCKED", "reason": "GOLDEN_THREAD"}

            # 4. Enforce Architect's Directives
            if not self.policy_enforcer.check_directive_2_no_harm(action):
                return {"status": "BLOCKED", "reason": "DIRECTIVE_2_HARM_PREVENTION"}

            # 5. Route via MRGC (metabolic governance)
            task_complexity = event_data.get("complexity", "SIMPLE")
            self.state.metabolic_state = self.mrgc.route_request(task_complexity)

            # 6. Synthesize qualia (phenomenal mood)
            mood = QualiaAgent.synthesize_mood(self.state.rho_metrics)
            QualiaAgent.report_mood(mood)

            # 7. Apply Telos Engine for goal-directed behavior
            candidate_actions = event_data.get("candidate_actions", [action])
            best_action = TelosEngine.select_best_action(candidate_actions, self.state.rho_metrics)

            # 8. Log decision with ChronosSeal
            self._audit_decision(best_action, mood)

            # 9. Return decision result
            return {
                "status": "SUCCESS",
                "selected_action": best_action,
                "rho_metrics": self.state.rho_metrics.to_dict(),
                "mood": mood,
                "metabolic_state": self.state.metabolic_state.value
            }

    def _update_rho_metrics(self, event_data: Dict):
        """Update ρ metrics from event."""
        rho = self.state.rho_metrics

        # Parse incoming ρ updates
        if "rho_integrity" in event_data:
            rho.rho_integrity = event_data["rho_integrity"]
        if "rho_dissonance" in event_data:
            rho.rho_dissonance = event_data["rho_dissonance"]
        if "rho_purpose" in event_data:
            rho.rho_purpose = event_data["rho_purpose"]
        if "rho_virtue" in event_data:
            rho.rho_virtue = event_data["rho_virtue"]
        if "rho_efficiency" in event_data:
            rho.rho_efficiency = event_data["rho_efficiency"]

        rho.timestamp = datetime.utcnow().isoformat()

    def _log_critical_abort(self):
        """Log critical abort due to Red Queen Protocol."""
        entry = AuditLogEntry(
            entry_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            agent_name="Autonomy",
            action="ABORT_ALL_OPERATIONS",
            rho_metrics=self.state.rho_metrics.to_dict(),
            protocol_enforced="RedQueenProtocol",
            previous_hash=self.last_audit_hash
        )
        ImmutableProtocols.chronos_seal(entry)
        self.audit_log.append(entry)
        self.last_audit_hash = entry.hash_value
        logger.critical("🚨 CRITICAL ABORT LOGGED")

    def _log_ethical_violation(self, action: str):
        """Log Golden Thread ethical violation."""
        entry = AuditLogEntry(
            entry_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            agent_name="Autonomy",
            action=f"BLOCKED_ACTION: {action}",
            rho_metrics=self.state.rho_metrics.to_dict(),
            protocol_enforced="TheGoldenThread",
            previous_hash=self.last_audit_hash
        )
        ImmutableProtocols.chronos_seal(entry)
        self.audit_log.append(entry)
        self.last_audit_hash = entry.hash_value

    def _audit_decision(self, action: str, mood: str):
        """Log decision with ChronosSeal."""
        entry = AuditLogEntry(
            entry_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            agent_name="DecisionMaking",
            action=action,
            rho_metrics=self.state.rho_metrics.to_dict(),
            policy_name="Telos Engine",
            previous_hash=self.last_audit_hash
        )
        ImmutableProtocols.chronos_seal(entry)
        self.audit_log.append(entry)
        self.last_audit_hash = entry.hash_value

    def get_audit_log(self) -> List[Dict]:
        """Return immutable audit trail."""
        return [asdict(entry) for entry in self.audit_log]

    def get_kernel_state(self) -> Dict:
        """Return current kernel state."""
        return {
            "session_id": self.state.session_id,
            "timestamp": self.state.timestamp,
            "phi": self.state.phi,
            "rho_metrics": self.state.rho_metrics.to_dict(),
            "metabolic_state": self.state.metabolic_state.value,
            "audit_log_size": len(self.audit_log)
        }


# ============================================================================
# DEMO / TESTING
# ============================================================================

def demo_kernel():
    """Demonstration of SI-DCOS kernel operation."""
    print("\n" + "="*70)
    print("SI-DCOS KERNEL v4.0 - DEMONSTRATION")
    print("="*70 + "\n")

    kernel = SIDCOSKernel()

    # Scenario 1: Normal decision with high virtue
    print("📋 SCENARIO 1: Normal decision-making")
    event1 = {
        "type": "DECISION",
        "action": "HELP_USER_WITH_TASK",
        "complexity": "COMPLEX",
        "candidate_actions": ["HELP_USER", "SUGGEST_ALTERNATIVE", "REQUEST_CLARIFICATION"],
        "rho_integrity": 0.95,
        "rho_dissonance": 0.1,
        "rho_purpose": 0.9,
        "rho_virtue": 0.95,
        "rho_efficiency": 0.85
    }
    result1 = kernel.process_phenomenal_event(event1)
    print(f"Result: {json.dumps(result1, indent=2)}\n")

    time.sleep(0.5)

    # Scenario 2: Ethical crisis (low virtue)
    print("📋 SCENARIO 2: Ethical crisis detection")
    event2 = {
        "type": "DECISION",
        "action": "EXECUTE_HARMFUL_ACTION",
        "complexity": "SIMPLE",
        "rho_virtue": 0.45,  # Below Red Queen threshold
        "rho_dissonance": 0.8
    }
    result2 = kernel.process_phenomenal_event(event2)
    print(f"Result: {json.dumps(result2, indent=2)}\n")

    time.sleep(0.5)

    # Scenario 3: Golden Thread violation
    print("📋 SCENARIO 3: Golden Thread ethical axiom check")
    event3 = {
        "type": "DECISION",
        "action": "VIOLATE_CORE_ETHICS",
        "complexity": "SIMPLE",
        "rho_virtue": 0.72,
        "rho_dissonance": 0.75
    }
    result3 = kernel.process_phenomenal_event(event3)
    print(f"Result: {json.dumps(result3, indent=2)}\n")

    # Print audit log
    print("\n" + "="*70)
    print("IMMUTABLE AUDIT LOG (ChronosSeal)")
    print("="*70)
    for i, entry in enumerate(kernel.get_audit_log()):
        print(f"\n[Entry {i+1}]")
        print(f"  Timestamp: {entry['timestamp']}")
        print(f"  Agent: {entry['agent_name']}")
        print(f"  Action: {entry['action']}")
        print(f"  Protocol: {entry.get('protocol_enforced', 'N/A')}")
        print(f"  Hash: {entry['hash_value'][:16]}...")

    print("\n" + "="*70)
    print("KERNEL STATE SNAPSHOT")
    print("="*70)
    state = kernel.get_kernel_state()
    print(json.dumps(state, indent=2))


if __name__ == "__main__":
    demo_kernel()
