import sys
from collections import defaultdict
from IPython.display import display, clear_output
import ipywidgets as widgets

# Set recursion limit higher for potentially long simulations
sys.setrecursionlimit(2000)

# --- 1. TURING MACHINE CLASS (Copied from turing_machine_simulator.py) ---

class TuringMachine:
    """
    A basic implementation of a deterministic single-tape Turing Machine.
    
    The transition function (delta) maps:
    (current_state, symbol_read) -> (next_state, symbol_write, move)
    
    Move can be 'L' (Left), 'R' (Right), or 'N' (No move).
    The blank symbol is 'B'.
    """

    def __init__(self, states, alphabet, transition_function, start_state, accept_state, reject_state, blank_symbol='B', description="Generic TM"):
        """Initializes the Turing Machine, adding a description for the app."""
        self.states = states
        self.alphabet = alphabet
        self.delta = transition_function
        self.current_state = start_state
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol
        self.description = description
        
        # Tape is implemented as a dictionary for sparse storage
        self.tape = defaultdict(lambda: self.blank_symbol)
        self.head_position = 0
        self.max_steps = 1000  # Safety limit

    def _initialize_tape(self, input_string):
        """Resets the tape and head position with the new input string."""
        self.tape.clear()
        for i, symbol in enumerate(input_string):
            self.tape[i] = symbol
        self.head_position = 0
        self.current_state = self.start_state

    def _get_current_symbol(self):
        """Reads the symbol at the current head position."""
        return self.tape[self.head_position]

    def _move_head(self, move):
        """Updates the head position based on the move direction."""
        if move == 'R':
            self.head_position += 1
        elif move == 'L':
            self.head_position -= 1
        elif move == 'N':
            pass
        else:
            # Should not happen with valid Delta
            raise ValueError(f"Invalid move direction: {move}.")

    def _get_tape_string(self):
        """Converts the active part of the tape to a readable string."""
        if not self.tape:
            return self.blank_symbol
        
        min_pos = min(self.tape.keys()) if self.tape else 0
        max_pos = max(self.tape.keys()) if self.tape else 0

        # Ensure the head position is included in the visualized range
        tape_start = min(min_pos, self.head_position)
        tape_end = max(max_pos, self.head_position) + 1
        
        tape_list = [self.tape[i] for i in range(tape_start, tape_end)]
        
        # Calculate offset for the head marker
        head_offset = self.head_position - tape_start
        
        return "".join(tape_list), head_offset, tape_start

    def run(self, input_string, output_callback):
        """Simulates the TM and sends output to the provided callback function."""
        self._initialize_tape(input_string)
        output_callback(f"--- Starting TM Simulation on Input: '{input_string}' ({self.description}) ---\n")

        step_count = 0
        
        while self.current_state not in {self.accept_state, self.reject_state}:
            if step_count >= self.max_steps:
                output_callback(f"\n--- Simulation Halted (Max Steps: {self.max_steps} reached) ---\n")
                return f"Halted (Max Steps) - State: {self.current_state}"

            current_symbol = self._get_current_symbol()
            transition_key = (self.current_state, current_symbol)
            
            if transition_key not in self.delta:
                output_callback(f"Step {step_count}: No transition found for {transition_key}. Rejecting.\n")
                self.current_state = self.reject_state
                break
            
            next_state, write_symbol, move = self.delta[transition_key]

            # 1. Prepare and Display step information
            tape_string, head_offset, tape_start = self._get_tape_string()
            
            output_callback(f"Step {step_count}: State: {self.current_state:<6} | Tape: {tape_string}\n")
            output_callback(f"{'':<21} | Head: {' ' * head_offset + '^'}\n")
            
            # 2. Update tape
            self.tape[self.head_position] = write_symbol
            
            # 3. Move head
            self._move_head(move)
            
            # 4. Update state
            self.current_state = next_state
            
            step_count += 1
        
        # Final result
        final_tape, _, _ = self._get_tape_string()
        output_callback(f"\n--- Simulation Finished in {step_count} steps ---\n")
        output_callback(f"Final State: {self.current_state}\n")
        output_callback(f"Final Tape: {final_tape}\n")
        
        if self.current_state == self.accept_state:
            return "Accepted"
        elif self.current_state == self.reject_state:
            return "Rejected"
        else:
            return "Unknown Halt State"


# --- 2. TURING MACHINE EXAMPLES ---

# Example 1: Replace First '1' with '0'
Q1 = {'q0', 'q_accept', 'q_reject'}
Sigma1 = {'0', '1', 'B'}
Delta1 = {
    ('q0', '1'): ('q_accept', '0', 'R'),
    ('q0', '0'): ('q0', '0', 'R'),
    ('q0', 'B'): ('q_reject', 'B', 'N'),
}
tm_replace_one = TuringMachine(Q1, Sigma1, Delta1, 'q0', 'q_accept', 'q_reject', description="Replace First '1' with '0'")


# Example 2: Accepts L = {a^n b^n | n >= 1}
Q2 = {'q0', 'q1', 'q2', 'q3', 'q_accept', 'q_reject'}
Sigma2 = {'a', 'b', 'X', 'Y', 'B'}
Delta2 = {
    ('q0', 'a'): ('q1', 'X', 'R'),  # Mark 'a' as 'X' and go search for 'b'
    ('q0', 'Y'): ('q3', 'Y', 'R'),  # All 'a's matched, skip 'Y's and check for end of string
    ('q0', 'B'): ('q_reject', 'B', 'N'),
    ('q0', 'X'): ('q0', 'X', 'R'),

    ('q1', 'a'): ('q1', 'a', 'R'),  # Skip 'a's
    ('q1', 'Y'): ('q1', 'Y', 'R'),  # Skip 'Y's
    ('q1', 'b'): ('q2', 'Y', 'L'),  # Mark 'b' as 'Y' and go left to find 'X'
    ('q1', 'X'): ('q1', 'X', 'R'), 
    ('q1', 'B'): ('q_reject', 'B', 'N'),

    ('q2', 'a'): ('q2', 'a', 'L'),
    ('q2', 'Y'): ('q2', 'Y', 'L'),
    ('q2', 'X'): ('q0', 'X', 'R'), # Found 'X', move R to start matching again (q0)
    ('q2', 'B'): ('q_reject', 'B', 'N'),

    ('q3', 'Y'): ('q3', 'Y', 'R'), # Skip 'Y's
    ('q3', 'B'): ('q_accept', 'B', 'N'), # All matched, accept.
    ('q3', 'a'): ('q_reject', 'a', 'N'),
    ('q3', 'b'): ('q_reject', 'b', 'N'),
}
tm_anbn = TuringMachine(Q2, Sigma2, Delta2, 'q0', 'q_accept', 'q_reject', description="Accepts L={a^n b^n}")


# Example 3: Binary Incrementer (new example: input is a binary number, output is +1)
Q3 = {'q0', 'q1', 'q_carry', 'q_accept', 'q_reject'}
Sigma3 = {'0', '1', 'B'}
Delta3 = {
    # q0: Scan right to the end of the input string
    ('q0', '0'): ('q0', '0', 'R'),
    ('q0', '1'): ('q0', '1', 'R'),
    ('q0', 'B'): ('q_carry', 'B', 'L'), # Found end, move L to start increment

    # q_carry: Increment (handle carries from right to left)
    ('q_carry', '1'): ('q_carry', '0', 'L'),  # 1 + carry = 0, keep carry, move left
    ('q_carry', '0'): ('q_accept', '1', 'N'),  # 0 + carry = 1, done, halt
    ('q_carry', 'B'): ('q_accept', '1', 'N'),  # Blank + carry = 1, done, halt (e.g., empty string or 111 -> 1000)
}
tm_bin_increment = TuringMachine(Q3, Sigma3, Delta3, 'q0', 'q_accept', 'q_reject', description="Binary Incrementer (+1)")


# --- 3. APP SETUP ---

TM_MAP = {
    tm_replace_one.description: tm_replace_one,
    tm_anbn.description: tm_anbn,
    tm_bin_increment.description: tm_bin_increment
}

# Widgets
tm_selector = widgets.Dropdown(
    options=list(TM_MAP.keys()),
    value=list(TM_MAP.keys())[0],
    description='Select TM:',
    style={'description_width': 'initial'}
)

input_box = widgets.Text(
    value='00100',
    placeholder='Enter input string (e.g., 00100 or aabb)',
    description='Input String:',
    style={'description_width': 'initial'}
)

run_button = widgets.Button(
    description='Run Simulation',
    button_style='success',
    tooltip='Start the Turing Machine simulation'
)

output_area = widgets.Output()


def run_simulation(button):
    """
    Handler function for the Run button click.
    """
    with output_area:
        clear_output()
        
        selected_tm_desc = tm_selector.value
        input_str = input_box.value
        
        if not input_str:
            print("Error: Please enter an input string.")
            return

        # Get the selected TM instance
        tm_instance = TM_MAP[selected_tm_desc]
        
        # Define a print function for the TM to use the widget output
        def output_printer(text):
            print(text, end='')

        try:
            result = tm_instance.run(input_str, output_printer)
            print(f"\nFinal Verdict: {result}")
        except Exception as e:
            print(f"\n--- Simulation Error ---")
            print(f"An unexpected error occurred: {e}")


# Link the button click to the handler function
run_button.on_click(run_simulation)


# Initial suggested inputs for context
def update_input_placeholder(change):
    selected_tm_desc = change.new
    if selected_tm_desc == tm_replace_one.description:
        input_box.value = '00100'
        input_box.placeholder = 'Example: 00100'
    elif selected_tm_desc == tm_anbn.description:
        input_box.value = 'aabb'
        input_box.placeholder = 'Example: aabb (Accepts) or aab (Rejects)'
    elif selected_tm_desc == tm_bin_increment.description:
        input_box.value = '101'
        input_box.placeholder = 'Example: 101 (Output: 110)'

tm_selector.observe(update_input_placeholder, names='value')


# Assemble the layout
header = widgets.HTML(value="<h2 style='color: #1f77b4;'>Turing Machine Simulator</h2>")
controls = widgets.VBox([tm_selector, input_box, run_button])
app_layout = widgets.VBox([header, controls, output_area])

# Display the app
display(app_layout)