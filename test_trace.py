"""
Ultra detailed projectile tracing
"""

from game.entities import Balloon, BalloonType, Tower, Vector2, Projectile

# Create simple scenario
tower = Tower(Vector2(200, 300), range=150, fire_rate=1.0)
balloon = Balloon(BalloonType.RED, Vector2(50, 300), [Vector2(50, 300), Vector2(400, 300)])

balloons = [balloon]

# Manually create and update projectile
projectile = Projectile(Vector2(200, 300), balloon, speed=300, damage=1)

print(f"Initial state:")
print(f"  Projectile at ({projectile.position.x}, {projectile.position.y})")
print(f"  Balloon at ({balloon.position.x}, {balloon.position.y}), health={balloon.health}")
print(f"  Distance: {projectile.position.distance_to(balloon.position)}")

dt = 1/60
for frame in range(30):  # 0.5 seconds
    # Update balloon
    balloon.update(dt)
    
    # Update projectile
    should_remove, new_balloons = projectile.update(dt, balloons)
    
    dist = projectile.position.distance_to(balloon.position)
    
    if frame % 5 == 0:
        print(f"\nFrame {frame} ({frame/60:.3f}s):")
        print(f"  Projectile at ({projectile.position.x:.1f}, {projectile.position.y:.1f})")
        print(f"  Balloon at ({balloon.position.x:.1f}, {balloon.position.y:.1f}), health={balloon.health}")
        print(f"  Distance: {dist:.1f}")
        print(f"  Should remove: {should_remove}")
        print(f"  New balloons: {len(new_balloons)}")
    
    if should_remove:
        print(f"\nProjectile removed at frame {frame}!")
        break
    
    # Remove dead balloons
    balloons = [b for b in balloons if b.health > 0]
    balloons.extend(new_balloons)

print(f"\nFinal balloon health: {balloon.health}")
print(f"Balloon in list: {balloon in balloons}")
