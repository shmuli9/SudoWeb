package sudoku

import (
	"testing"
)

func TestGenerateBoard(t *testing.T) {
	gen := NewGenerator(9)
	if !gen.GenerateBoard() {
		t.Error("Failed to generate board")
	}

	if !gen.ValidateBoard() {
		t.Error("Generated board is not valid")
	}

	// Check that board is complete (no zeros)
	for row := 0; row < 9; row++ {
		for col := 0; col < 9; col++ {
			if gen.Get(row, col) == 0 {
				t.Errorf("Board has empty cell at row %d, col %d", row, col)
			}
		}
	}
}

func TestPossibleDigits(t *testing.T) {
	g := NewGrid(9)

	// Empty board should have all digits possible
	digits := g.PossibleDigits(0, 0)
	if len(digits) != 9 {
		t.Errorf("Expected 9 possible digits for empty board, got %d", len(digits))
	}

	// Set some values and check conflicts
	g.Set(0, 1, 1) // Same row
	g.Set(1, 0, 2) // Same column
	g.Set(1, 1, 3) // Same box

	digits = g.PossibleDigits(0, 0)
	if len(digits) != 6 {
		t.Errorf("Expected 6 possible digits after setting conflicts, got %d", len(digits))
	}

	// Check that conflicting digits are not in possible digits
	for _, d := range []int{1, 2, 3} {
		for _, possible := range digits {
			if possible == d {
				t.Errorf("Digit %d should not be possible but was found in possible digits", d)
			}
		}
	}
}

// BenchmarkGenerateBoard measures the performance of generating a single board
func BenchmarkGenerateBoard(b *testing.B) {
	b.ReportAllocs() // Report memory allocations
	for i := 0; i < b.N; i++ {
		gen := NewGenerator(9)
		if !gen.GenerateBoard() {
			b.Error("Failed to generate board")
		}
	}
}

// BenchmarkGenerateBoardParallel measures the performance of generating boards in parallel
func BenchmarkGenerateBoardParallel(b *testing.B) {
	b.ReportAllocs() // Report memory allocations
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			gen := NewGenerator(9)
			if !gen.GenerateBoard() {
				b.Error("Failed to generate board")
			}
		}
	})
}

// BenchmarkPossibleDigits measures the performance of finding possible digits
func BenchmarkPossibleDigits(b *testing.B) {
	g := NewGrid(9)
	// Fill some cells to create a realistic scenario
	g.Set(0, 1, 1)
	g.Set(1, 0, 2)
	g.Set(1, 1, 3)

	b.ResetTimer() // Reset timer after setup
	b.ReportAllocs()

	for i := 0; i < b.N; i++ {
		g.PossibleDigits(0, 0)
	}
}

// BenchmarkValidateBoard measures the performance of board validation
func BenchmarkValidateBoard(b *testing.B) {
	gen := NewGenerator(9)
	if !gen.GenerateBoard() {
		b.Fatal("Failed to generate board for benchmark")
	}

	b.ResetTimer() // Reset timer after setup
	b.ReportAllocs()

	for i := 0; i < b.N; i++ {
		gen.ValidateBoard()
	}
}
