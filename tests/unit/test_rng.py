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
