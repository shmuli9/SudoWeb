package main

import (
	"flag"
	"fmt"
	"math/rand"
	"runtime"
	"time"

	"github.com/shmuli/sudoweb/pkg/sudoku"
)

func init() {
	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())
}

func printBoard(g *sudoku.Grid) {
	fmt.Println("┌───────┬───────┬───────┐")
	for row := range 9 {
		fmt.Print("│")
		for col := range 9 {
			if val := g.Get(row, col); val != 0 {
				fmt.Printf(" %d", val)
			} else {
				fmt.Print(" ·")
			}
			if (col+1)%3 == 0 {
				fmt.Print(" │")
			}
		}
		fmt.Println()
		if (row+1)%3 == 0 && row < 8 {
			fmt.Println("├───────┼───────┼───────┤")
		}
	}
	fmt.Println("└───────┴───────┴───────┘")
}

func main() {
	count := flag.Int("n", 1, "Number of boards to generate")
	flag.Parse()

	if *count > 1 {
		fmt.Printf("Generating %d boards using %d CPU cores...\n", *count, runtime.NumCPU())
		boards, duration := sudoku.GenerateBoards(*count)
		fmt.Printf("Generated %d boards in %v (%.0f boards/second)\n", *count, duration, float64(*count)/duration.Seconds())

		if *count <= 10 {
			fmt.Println("\nGenerated boards:")
			for i, board := range boards {
				fmt.Printf("\nBoard %d:\n", i+1)
				printBoard(board)
			}
		}
	} else {
		gen := sudoku.NewGenerator(9)
		if gen.GenerateBoard() {
			fmt.Println("Generated Sudoku board:")
			printBoard(gen.Grid)
		} else {
			fmt.Println("Failed to generate board")
		}
	}
}
