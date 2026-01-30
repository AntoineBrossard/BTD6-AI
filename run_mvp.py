"""
MVP runner: load Monkey Meadows (easy), detect game window via PIL,
evaluate replica AI, if AI wins place towers in real game via hotkeys,
then start the round.

Usage: python run_mvp.py
"""

import time
from ai.train import evaluate_model
from integration.btd6_integration import BTD6Integration

MODEL_PATH = "models/btd6_test_final.zip"


def main():
    print("Starting MVP orchestrator: Monkey Meadows (easy)")

    # Initialize integration and detect window
    integration = BTD6Integration()
    print("Detecting game window (using PIL full-screen capture)...")
    region = integration.detect_game_window()
    print(f"Detected game region: {region}")

    # Evaluate the replica AI in the simulator
    print("Evaluating replica AI in simulation...")
    try:
        result = evaluate_model(MODEL_PATH, episodes=3, render=False)
    except Exception as e:
        print(f"Failed to evaluate model: {e}")
        return

    print(f"AI wins: {result['wins']}/{result['episodes']}")

    if result["wins"] > 0:
        # Use placements from the first winning episode (if any)
        placements = []
        for pl in result["placements"]:
            if pl:
                placements = pl
                break

        # Convert placements (x,y) -> action dicts
        actions = [{"type": "dart_monkey", "x": x, "y": y} for (x, y) in placements]

        if actions:
            print(f"AI suggested {len(actions)} tower placements")
            print(f"Available cash: ~${result.get('average_reward', 0):.0f} (simulator estimate)")
            print(f"Tower cost: $1200 each (total needed: ${len(actions) * 1200})")
            print(f"Placing towers using hotkeys (0.2s delay between placement)...")
            integration.place_towers_hotkeys(actions)
            print(f"Tower placement complete")
        else:
            print("AI chose no placements; skipping tower placement.")

        # Start the round
        print("Starting round in real game (attempting click on Start button)...")
        integration.start_round_auto()
    else:
        print("AI did not win in the simulation; aborting real-game placement.")


if __name__ == "__main__":
    main()
