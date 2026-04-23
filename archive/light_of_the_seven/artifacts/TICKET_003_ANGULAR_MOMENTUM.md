# TICKET-003: Depth Graph — Angular Momentum Research

**Status**: ASSIGNED  
**Assignee**: @user  
**Priority**: High  
**Type**: Research → Implementation

---

## Objective

Extend 2D animation engine to 3D with angular momentum support.

---

## Scope

### 1. Z-Axis Integration
- [ ] Extend `Vector2D` → `Vector3D` (x, y, z)
- [ ] Add depth coordinate to Agent position
- [ ] Implement 3D → 2D projection for screen rendering

### 2. Angular Momentum
- [ ] `L = r × p` (position × momentum, cross product)
- [ ] Angular velocity: `ω = dθ/dt`
- [ ] Torque: `τ = r × F`
- [ ] Moment of inertia for different shapes

### 3. 3D Rotation
- [ ] Pitch (X-axis rotation)
- [ ] Yaw (Y-axis rotation)  
- [ ] Roll (Z-axis rotation)
- [ ] Quaternions (optional, avoids gimbal lock)

---

## Physics Reference

```
Linear:   p = m × v       (momentum)
Angular:  L = I × ω       (angular momentum)
          L = r × p       (cross product form)
          τ = dL/dt       (torque = rate of change)

Cross Product:
  a × b = (ay*bz - az*by,
           az*bx - ax*bz,
           ax*by - ay*bx)

Rotation Matrix (around Z):
  [cos(θ)  -sin(θ)  0]
  [sin(θ)   cos(θ)  0]
  [0        0       1]
```

---

## Axes Convention

```
        +Y (up)
         │
         │
         │
         └──────── +X (right)
        /
       /
      +Z (toward viewer)

Angles:
  θx = pitch (nose up/down)
  θy = yaw   (turn left/right)
  θz = roll  (tilt sideways)
```

---

## Starting Point

```
File: experiments/animation_engine.py
Line: 30 (Vector2D class)

Add:
  - Vector3D dataclass
  - cross_product() method
  - rotate_3d(pitch, yaw, roll) method
  - project_to_2d(camera_distance) method
```

---

## Deliverables

1. `Vector3D` class with rotation support
2. `AngularBody` class (extends Agent with angular properties)
3. 3D checkpoint navigation demo
4. Projection rendering (ASCII perspective)

---

## Success Criteria

- [ ] Agent can move in X, Y, Z
- [ ] Agent can rotate (spin) with angular momentum
- [ ] Torque applies rotational force
- [ ] 3D scene renders to 2D with depth cues

---

## Notes

> "Like old video games going left-right, but now we add vertical (gravity) AND depth (into screen). Angular momentum = spinning while moving."

---

*Est. effort: 2-4 hours*