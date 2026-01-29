"""
Test win condition
"""

from game.game import BTD6Game, GameState

game = BTD6Game(width=800, height=600)
game.place_tower(100, 300)
game.place_tower(300, 250)
game.place_tower(500, 250)

dt = 1/60
max_frames = 1200  # 20 seconds

for frame in range(max_frames):
    game.update(dt)
    
    if frame % 60 == 0:
        print(f"[{frame//60}s] Lives: {game.lives}, Balloons: {len(game.balloons)}, State: {game.state.name}")
    
    if game.state != GameState.RUNNING:
        print(f"\n=== GAME ENDED at {frame/60:.1f}s ===")
        print(f"Final state: {game.state.name}")
        break

if game.state == GameState.RUNNING:
    print("\nReached max time, game still running")

print(f"\nFinal: State={game.state.name}, Lives={game.lives}, Balloons={len(game.balloons)}")
