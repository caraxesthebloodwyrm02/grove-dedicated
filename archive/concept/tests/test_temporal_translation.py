import builtins
import types

import temporal_translation as tt


class DummySleep:
    def __call__(self, *_args, **_kwargs):
        # no-op to keep tests fast and deterministic
        return None


def test_tempo_engine_initialization():
    engine = tt.TempoEngine(bpm=120, toggle=True)
    assert engine.bpm == 120
    assert engine.toggle is True
    assert abs(engine.beat_interval - 0.5) < 1e-9


def test_toggle_and_structure_description():
    engine = tt.TempoEngine(bpm=100, toggle=True)
    assert "quantized" in engine.get_structure_description()

    engine.toggle_tempo(False)
    assert engine.toggle is False
    assert "freeform" in engine.get_structure_description()


def test_interpret_tempo_perception_mapping():
    assert "rigid" in tt.interpret_tempo_perception(True)
    assert "flexible" in tt.interpret_tempo_perception(False)


def test_simulate_sequence_runs_without_error(monkeypatch):
    # Patch time.sleep on the module under test to avoid delays
    dummy = DummySleep()
    monkeypatch.setattr(tt.time, "sleep", dummy)

    # Ensure function runs for both modes without raising
    engine_on = tt.TempoEngine(bpm=120, toggle=True)
    engine_on.simulate_sequence(beats=3)

    engine_off = tt.TempoEngine(bpm=120, toggle=False)
    engine_off.simulate_sequence(beats=3)
