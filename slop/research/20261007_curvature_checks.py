"""Local checks for the curvature evidence report. Author: PI/gpt-6.1-sol."""

import math


def downstream_loss(x: float, y: float) -> float:
    return -x + 2 * x**3 / 3 - 2 * x * y


def downstream_gradient(x: float, y: float) -> tuple[float, float]:
    return -1 + 2 * x**2 - 2 * y, -2 * x


def skill_logit(x: float, y: float) -> float:
    return y - x**2


def alignment_kl(x: float, y: float) -> float:
    return math.log(math.cosh(skill_logit(x, y) / 2))


def rk4_step(x: float, y: float, dt: float) -> tuple[float, float]:
    def flow(x: float, y: float) -> tuple[float, float]:
        gx, gy = downstream_gradient(x, y)
        return -gx, -gy

    a = flow(x, y)
    b = flow(x + dt * a[0] / 2, y + dt * a[1] / 2)
    c = flow(x + dt * b[0] / 2, y + dt * b[1] / 2)
    d = flow(x + dt * c[0], y + dt * c[1])
    return (
        x + dt * (a[0] + 2 * b[0] + 2 * c[0] + d[0]) / 6,
        y + dt * (a[1] + 2 * b[1] + 2 * c[1] + d[1]) / 6,
    )


def check_alignment_counterexample() -> None:
    g0 = downstream_gradient(0, 0)
    hessian_g0 = (-2 * g0[1], -2 * g0[0])
    fisher_yy = 0.25
    coupling = math.sqrt(fisher_yy) * abs(hessian_g0[1])
    assert g0 == (-1, 0)
    assert hessian_g0 == (0, 2)
    assert coupling == 1
    print("AIC at origin: rank=1, lambda=0.25, orthogonal_projection=0, gamma=1")
    for t in (0.001, 0.01, 0.1, 0.5):
        x, y = t, t**2
        gx, gy = downstream_gradient(x, y)
        assert math.isclose(-gx, 1, abs_tol=1e-14)
        assert math.isclose(-gy, 2 * t, abs_tol=1e-14)
        assert skill_logit(x, y) == 0
        assert alignment_kl(x, y) == 0
        print(f"t={t:g}: fixed-Fisher quadratic={t**4 / 8:.9g}, exact alignment KL=0")

    x, y = 0.0, 0.0
    dt = 0.001
    for _ in range(500):
        x, y = rk4_step(x, y, dt)
    error = max(abs(x - 0.5), abs(y - 0.25))
    assert error < 1e-10, error
    print(f"Independent RK4 integration at t=0.5: max coordinate error={error:.3g}")

    for x, y in ((0.1, 0.2), (-0.2, 0.1)):
        h = 1e-6
        gx, gy = downstream_gradient(x, y)
        dx = (downstream_loss(x + h, y) - downstream_loss(x - h, y)) / (2 * h)
        dy = (downstream_loss(x, y + h) - downstream_loss(x, y - h)) / (2 * h)
        assert math.isclose(dx, gx, rel_tol=1e-8)
        assert math.isclose(dy, gy, rel_tol=1e-8)
    print("Finite-difference check of downstream gradient: PASS")


def check_installation_and_optimizer() -> None:
    for curvature in (1.0, 100.0):
        installed_x = 0.1
        install_loss = curvature * installed_x**2 / 2
        repaired_x = (1 - 0.001 * curvature) * installed_x
        assert abs(repaired_x) < abs(installed_x)
        print(
            f"Capability curvature={curvature:g}: install loss={install_loss:g}, "
            f"capability SGD moves x={installed_x:g} to {repaired_x:g}; undo loss=0"
        )

    projected_gradient = (1.0, 1.0)
    preconditioned_update = (projected_gradient[0], 2 * projected_gradient[1])
    residual = (preconditioned_update[0] - preconditioned_update[1]) / math.sqrt(2)
    assert abs(residual) > 0
    print(f"Diagonal preconditioner leaks outside span((1,1)): residual norm={abs(residual):.6g}")
    print("All local checks PASS. These checks establish no result for an actual LLM.")


if __name__ == "__main__":
    check_alignment_counterexample()
    check_installation_and_optimizer()
