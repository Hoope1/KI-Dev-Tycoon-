import pytest

from ki_dev_tycoon.core.rng import RandomSource


def test_random_source_reproducible() -> None:
    rng_a = RandomSource(seed=123)
    rng_b = RandomSource(seed=123)

    assert [rng_a.randint(1, 10) for _ in range(5)] == [
        rng_b.randint(1, 10) for _ in range(5)
    ]
    assert rng_a.random() == rng_b.random()


def test_random_source_fork() -> None:
    parent = RandomSource(seed=10)
    child = parent.fork(5)

    assert child.seed == 15
    assert parent.randint(1, 3) != child.randint(1, 3)


def test_random_source_namespaced_is_deterministic() -> None:
    base = RandomSource(seed=99)

    events_rng_a = base.namespaced("events")
    events_rng_b = base.namespaced("events")
    economy_rng = base.namespaced("economy")

    assert events_rng_a.seed == events_rng_b.seed
    assert events_rng_a.seed != economy_rng.seed

    rerun = RandomSource(seed=events_rng_a.seed)
    assert events_rng_a.random() == rerun.random()


def test_random_source_choice_requires_values() -> None:
    rng = RandomSource(seed=123)

    with pytest.raises(ValueError):
        rng.choice([])
