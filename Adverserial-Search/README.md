# Minimax and Alpha-Beta Pruning Algorithm

Implementation of Minimax and Alpha-Beta Pruning Algorithm in Python for the Game of Nim.

## Features
- Implements the Minimax algorithm for determining the best move in a two-player game
- Uses Alpha-Beta pruning to significantly reduce the number of nodes evaluated by the algorithm
- Customizable depth limit for the search
- Provides a user-friendly interface for configuring and running the algorithm
- Can handle games with variable number of players and different game states
- Can handle games with different evaluation function
- Can handle games with different rules 
- Provides the flexibility to use different strategies for evaluation function
- Provide the flexibility to set the value of the heuristic function



## Usage

1. `SolveGame("Minimax", "nim1.txt", "MAX")` or
    `SolveGame("AlphaBeta", "nim1.txt" ,"MAX")`

2. `nim1.txt` should be in form `[1,3,5]`. It means there are 3 piles and 1,3 and 5 is the number of objects.

## Contributing

1. Fork the repository
2. Create a new branch for your changes (`git checkout -b new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin new-feature`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
