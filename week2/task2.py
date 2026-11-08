class SmartClimateAgent:
    def __init__(self):
        # Internal state to track previous action
        self.last_mode = None

    def step(self, temp: float, occupied: bool) -> dict:
        # 1. Target mode determine karna
        if not occupied:
            mode = "ECO"
        elif temp > 26:
            mode = "COOL"
        elif temp < 20:
            mode = "WARM"
        else:
            mode = "IDLE"

        # 2. Transition record banana
        transition = {
            "prior": self.last_mode,
            "current": mode,
            "dispatch": "SEND COMMAND" if mode != self.last_mode else "NO COMMAND"
        }
        
        self.last_mode = mode
        return transition

def run_simulation():
    observations = [(29, True), (29, True), (20, True), (26, True), (19, True), (29, False), (29, False)]
    controller = SmartClimateAgent()

    # Table Header
    print(f"{'Step':^6} | {'Previous Mode':<14} | {'Percept':<13} | {'Target Mode':<12} | {'Signal Action'}")
    print("-" * 65)

    # Simulation Loop
    for idx, (temp, occupied) in enumerate(observations, start=1):
        res = controller.step(temp, occupied)
        print(f"{idx:^6} | {str(res['prior']):<14} | {str((temp, occupied)):<13} | {res['current']:<12} | {res['dispatch']}")

if __name__ == "__main__":
    run_simulation()