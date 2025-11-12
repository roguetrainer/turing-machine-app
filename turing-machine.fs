// --------------------------------------------------------------------------
// F# Turing Machine Emulator
// --------------------------------------------------------------------------

module TuringMachineSimulator

open System.Collections.Generic
open System

// --- 1. Core Type Definitions using Discriminated Unions ---

/// Defines the possible states of the machine.
type State = 
    | Q of string // Standard state, e.g., Q("q0")
    | Accept
    | Reject

/// Defines the tape alphabet symbols.
type Symbol = 
    | Zero
    | One
    | Blank
    | Other of char

/// Defines the head movement directions.
type Move = L | R | N

/// Converts a char input string into a list of Symbols, using 'B' for Blank.
let stringToSymbols (input: string) =
    input 
    |> Seq.map (function
        | '0' -> Zero
        | '1' -> One
        | ' ' -> Blank // Assuming spaces represent Blank in input
        | c   -> Other c)
    |> List.ofSeq

/// Converts a Symbol back to a char for display.
let symbolToChar (sym: Symbol) =
    match sym with
    | Zero    -> '0'
    | One     -> '1'
    | Blank   -> 'B'
    | Other c -> c

// --- 2. Tape and Configuration Representation ---

/// The Tape is modeled immutably as two lists: 
/// 'left' (reversed) and 'right' (standard). The head is on the first item of 'right'.
type Tape = { left: list<Symbol>; right: list<Symbol> }

/// The current configuration of the TM.
type Configuration = { state: State; tape: Tape }

/// Represents a single transition rule (delta function).
type Rule = 
    { currentState: State
      readSymbol: Symbol
      nextState: State
      writeSymbol: Symbol
      move: Move }

// --- 3. Simulation Logic ---

/// Tries to find a matching transition rule for the current state and symbol.
let findRule (rules: list<Rule>) (currentState: State) (readSymbol: Symbol) : Rule option =
    rules 
    |> List.tryFind (fun r -> r.currentState = currentState && r.readSymbol = readSymbol)

/// Applies the move instruction, returning a new immutable Tape.
let applyMove (move: Move) (tape: Tape) : Tape =
    match move, tape.left, tape.right with
    // Move Right: Takes the first symbol from the right list and adds it to the left list (in reverse order).
    | R, _, head :: tail -> { left = head :: tape.left; right = tail }
    // If the right list is empty, expand the tape with a Blank symbol.
    | R, _, [] -> { left = Blank :: tape.left; right = [] }
    
    // Move Left: Takes the first symbol from the left list and adds it to the right list.
    | L, head :: tail, _ -> { left = tail; right = head :: tape.right }
    // If the left list is empty, expand the tape with a Blank symbol.
    | L, [], _ -> { left = []; right = Blank :: tape.right }
    
    // No Move: Tape remains the same.
    | N, _, _ -> tape

/// Performs a single step of the Turing Machine (a pure function).
let step (rules: list<Rule>) (config: Configuration) : Configuration option =
    // Determine the symbol under the head (the first element of the 'right' list, or Blank if empty).
    let readSymbol = match config.tape.right with | head :: _ -> head | [] -> Blank
    
    match findRule rules config.state readSymbol with
    | Some rule -> 
        // 1. Write Symbol: The new tape's right list starts with the written symbol.
        let newRight = match config.tape.right with | _ :: tail -> rule.writeSymbol :: tail | [] -> [rule.writeSymbol]
        let tapeWritten = { left = config.tape.left; right = newRight }

        // 2. Move Head: Apply the move rule immutably.
        let newTape = applyMove rule.move tapeWritten

        // 3. New State: Return the new configuration.
        Some { state = rule.nextState; tape = newTape }
    | None -> 
        // No transition found, machine halts in the current non-halting state.
        None

/// Utility function to display the tape with the head position marked.
let printTape (tape: Tape) =
    // Reverse the left side back to its original order for printing
    let leftStr = tape.left |> List.rev |> List.map symbolToChar |> List.ofSeq |> String.Concat
    // Get the symbols in the right list
    let rightSymbols = tape.right |> List.map symbolToChar |> List.ofSeq
    
    match rightSymbols with
    | head :: tail -> 
        // Head is on 'head'
        let rightStr = head :: tail |> String.Concat
        let displayStr = leftStr + "[" + string head + "]" + String.Concat tail
        printfn "    Tape: %s" displayStr
        
    | [] -> 
        // Head is on a new Blank cell that hasn't been written to the dictionary/list yet
        let displayStr = leftStr + "[B]"
        printfn "    Tape: %s" displayStr
        
/// Utility function to display the current state.
let printState (state: State) =
    match state with
    | Q s -> printf "State: %s" s
    | Accept -> printf "State: Accept (Halt)"
    | Reject -> printf "State: Reject (Halt)"

/// Utility function to extract the final tape content and clean up Blanks.
let getFinalOutput (finalConfig: Configuration) =
    // Concatenate the reversed left list and the right list
    let finalSymbols = List.rev finalConfig.tape.left @ finalConfig.tape.right
    // Convert to a string and remove leading/trailing blanks
    let resultStr = finalSymbols 
                    |> List.map symbolToChar 
                    |> List.ofSeq 
                    |> String.Concat 
                    |> (fun s -> s.TrimEnd('B') |> (fun s -> s.TrimStart('B'))) 
    resultStr

/// The main recursive simulation loop.
let rec runSimulation maxSteps stepCount rules config =
    if stepCount >= maxSteps then
        printfn "\n--- Simulation Halted (Max Steps: %d Reached) ---" maxSteps
        config
    else
        // Display current configuration
        printf "\nStep %d: " stepCount
        printState config.state
        printfn ""
        printTape config.tape
        
        match config.state with
        | Accept | Reject -> 
            printfn "\n--- Simulation Finished in %d steps ---" stepCount
            config
        | _ -> 
            match step rules config with
            | Some nextConfig -> 
                runSimulation maxSteps (stepCount + 1) rules nextConfig
            | None ->
                // No rule found, transition to Reject state (implicit rejection)
                printfn "\nNo matching rule found. Implicitly rejecting."
                { config with state = Reject }

/// Generic function to run any TM setup.
let runTM (description: string) (input: string) (rules: list<Rule>) (maxSteps: int) =
    let symbols = stringToSymbols input
    
    // Initial tape: The input string is on the right side.
    let initialTape = { left = []; right = symbols }
    let initialConfig = { state = Q "q0"; tape = initialTape }

    printfn "================================================="
    printfn "TURING MACHINE: %s" description
    printfn "Input: %s" input
    printfn "Max Steps: %d" maxSteps
    printfn "================================================="
    
    let finalConfig = runSimulation maxSteps 0 rules initialConfig
    
    printfn "\n*** Final Result ***"
    printState finalConfig.state
    printfn ""
    printTape finalConfig.tape
    
    let resultStr = getFinalOutput finalConfig
    printfn "Final Output (trimmed Blanks): %s" resultStr
    printfn "================================================="


// --- 4. EXAMPLE 1: Binary Incrementer (+1) ---
// TM to compute N + 1 for input N in binary (e.g., "101" -> "110")

let tmIncrementerRules : list<Rule> = [
    // q0: Scan right to find the Blank symbol (end of input)
    { currentState = Q "q0"; readSymbol = Zero; nextState = Q "q0"; writeSymbol = Zero; move = R }
    { currentState = Q "q0"; readSymbol = One; nextState = Q "q0"; writeSymbol = One; move = R }
    { currentState = Q "q0"; readSymbol = Blank; nextState = Q "q_carry"; writeSymbol = Blank; move = L }

    // q_carry: Handle increment (move left)
    { currentState = Q "q_carry"; readSymbol = One; nextState = Q "q_carry"; writeSymbol = Zero; move = L } // 1 + carry = 0, keep carry (move left)
    { currentState = Q "q_carry"; readSymbol = Zero; nextState = Accept; writeSymbol = One; move = N }  // 0 + carry = 1, done (halt)
    { currentState = Q "q_carry"; readSymbol = Blank; nextState = Accept; writeSymbol = One; move = N }  // Blank (empty tape or 111) + carry = 1, done (halt)
]

// --- 5. EXAMPLE 2: Busy Beaver 2-State (BB-2) ---
// The most productive 2-state TM that halts. Writes 4 ones in 6 steps.
// States are A (q0) and B (q1), Halt (Accept).

let tmBusyBeaver2Rules : list<Rule> = [
    // State A (Q "q0")
    { currentState = Q "q0"; readSymbol = Blank; nextState = Q "q1"; writeSymbol = One; move = R }
    { currentState = Q "q0"; readSymbol = One; nextState = Q "q1"; writeSymbol = One; move = L }

    // State B (Q "q1")
    { currentState = Q "q1"; readSymbol = Blank; nextState = Q "q0"; writeSymbol = One; move = L }
    { currentState = Q "q1"; readSymbol = One; nextState = Accept; writeSymbol = One; move = N } // Halt and accept
]


// --- Example Runs ---

// Run Example 1: Binary Incrementer
runTM "Binary Incrementer (+1)" "101" tmIncrementerRules 100 // 5 -> 6
runTM "Binary Incrementer (+1)" "111" tmIncrementerRules 100 // 7 -> 8 (requires tape expansion)


// Run Example 2: Busy Beaver 2-State
// Note: Busy Beaver starts on a completely blank tape ("").
runTM "Busy Beaver 2-State (BB-2)" "" tmBusyBeaver2Rules 10