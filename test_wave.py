"""
Debug wave completion
"""

from game.game import BTD6Game, GameState

game = BTD6Game(width=800, height=600)
game.place_tower(100, 300)
game.place_tower(300, 250)

dt = 1/60

for frame in range(600):
    game.update(dt)
    
    if frame % 60 == 0:
        expected_spawns = sum(count for _, count in game.round_waves[game.current_wave])
        print(f"[{frame//60}s] Spawned: {game.balloons_spawned}/{expected_spawns}, Balloons: {len(game.balloons)}, Projectiles: {len(game.projectiles)}, State: {game.state.name}")
        print(f"    Wave index: {game.current_wave}/{len(game.round_waves)}, Spawn index: {game.spawn_index}")
    
    if game.state != GameState.RUNNING:
        print(f"\n=== GAME ENDED ===")
        break

print(f"\nFinal state: {game.state.name}")
